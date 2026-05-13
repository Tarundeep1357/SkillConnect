
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import logging
import os
import threading

from fastapi import Depends, FastAPI, HTTPException, Query, Request, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from mysql.connector import Error as MySQLError
from mysql.connector.errors import IntegrityError
from passlib.context import CryptContext

from db import get_db_connection
from models import (
    VALID_APPLICATION_STATUSES,
    VALID_PROFICIENCY_LEVELS,
    VALID_REGISTRATION_ROLES,
    VALID_SYSTEM_ROLES,
)
from schemas import (
    DevSignatureRequest,
    JobApplicationStatusUpdateRequest,
    JobApplyRequest,
    JobCreateRequest,
    MessageCreateRequest,
    MeResponse,
    PremiumUpgradeRequest,
    ResumeGenerateRequest,
    ResumeGenerateResponse,
    SkillCreate,
    UserRegister,
)

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("skillconnect")

# =====================================================
# App / Environment
# =====================================================

APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
IS_PRODUCTION = APP_ENV == "production"

SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
if not SECRET_KEY:
    if IS_PRODUCTION:
        raise RuntimeError("SECRET_KEY is required in production")
    SECRET_KEY = "dev_only_secret_key_change_me"
    logger.warning("Using development SECRET_KEY. Set SECRET_KEY for secure environments.")

PAYMENT_SIGNING_SECRET = os.getenv("PAYMENT_SIGNING_SECRET", "").strip()
if not PAYMENT_SIGNING_SECRET:
    if IS_PRODUCTION:
        raise RuntimeError("PAYMENT_SIGNING_SECRET is required in production")
    PAYMENT_SIGNING_SECRET = "dev_payment_signing_secret_change_me"
    logger.warning(
        "Using development PAYMENT_SIGNING_SECRET. Set PAYMENT_SIGNING_SECRET in non-dev environments."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
MAX_FAILED_LOGIN_ATTEMPTS = int(os.getenv("MAX_FAILED_LOGIN_ATTEMPTS", "5"))
LOGIN_ATTEMPT_WINDOW_SECONDS = int(os.getenv("LOGIN_ATTEMPT_WINDOW_SECONDS", "600"))
LOGIN_BLOCK_SECONDS = int(os.getenv("LOGIN_BLOCK_SECONDS", "900"))

AI_SYSTEM_PROMPT = (
    "You are an expert resume writer. Produce ATS-friendly resumes in plain text. "
    "Adapt structure to each candidate instead of forcing a rigid template. "
    "Use strong action verbs, concise bullets, and quantifiable outcomes when possible. "
    "Do not output markdown code fences."
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title="SkillConnect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# =====================================================
# Rate Limit Store (In-Memory)
# =====================================================

_LOGIN_TRACKER_LOCK = threading.Lock()
_LOGIN_TRACKER: dict[str, dict] = {}


class MessageConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.setdefault(user_id, set()).add(websocket)

    async def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            sockets = self._connections.get(user_id)
            if not sockets:
                return
            sockets.discard(websocket)
            if not sockets:
                self._connections.pop(user_id, None)

    async def send_to_users(self, user_ids: set[int], payload: dict) -> None:
        async with self._lock:
            targets = [
                (user_id, websocket)
                for user_id in user_ids
                for websocket in list(self._connections.get(user_id, set()))
            ]

        stale_connections: list[tuple[int, WebSocket]] = []
        for user_id, websocket in targets:
            try:
                await websocket.send_json(payload)
            except Exception:
                stale_connections.append((user_id, websocket))

        for user_id, websocket in stale_connections:
            await self.disconnect(user_id, websocket)


message_connections = MessageConnectionManager()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        return str(value)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.isoformat().replace("+00:00", "Z")


def _normalize_csv_skills(skills: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for raw in skills:
        candidate = " ".join(raw.strip().split())
        if not candidate:
            continue
        key = candidate.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(candidate)
    return cleaned


def _build_login_key(username: str, client_ip: str) -> str:
    return f"{username.strip().lower()}|{client_ip}"


def _purge_login_tracker(now: datetime) -> None:
    to_delete = []
    for key, item in _LOGIN_TRACKER.items():
        blocked_until = item.get("blocked_until")
        window_start = item.get("window_start")
        if blocked_until and blocked_until < now and window_start and (now - window_start).total_seconds() > LOGIN_ATTEMPT_WINDOW_SECONDS:
            to_delete.append(key)
    for key in to_delete:
        _LOGIN_TRACKER.pop(key, None)


def _get_login_block_seconds(login_key: str) -> int:
    now = _utc_now()
    with _LOGIN_TRACKER_LOCK:
        _purge_login_tracker(now)
        item = _LOGIN_TRACKER.get(login_key)
        if not item:
            return 0
        blocked_until = item.get("blocked_until")
        if not blocked_until or blocked_until <= now:
            return 0
        return int((blocked_until - now).total_seconds())


def _record_failed_login(login_key: str) -> None:
    now = _utc_now()
    with _LOGIN_TRACKER_LOCK:
        _purge_login_tracker(now)
        item = _LOGIN_TRACKER.get(login_key)
        if not item:
            item = {
                "count": 0,
                "window_start": now,
                "blocked_until": None,
            }
            _LOGIN_TRACKER[login_key] = item

        window_start = item["window_start"]
        if (now - window_start).total_seconds() > LOGIN_ATTEMPT_WINDOW_SECONDS:
            item["count"] = 0
            item["window_start"] = now
            item["blocked_until"] = None

        item["count"] += 1
        if item["count"] >= MAX_FAILED_LOGIN_ATTEMPTS:
            item["blocked_until"] = now + timedelta(seconds=LOGIN_BLOCK_SECONDS)


def _clear_failed_login(login_key: str) -> None:
    with _LOGIN_TRACKER_LOCK:
        _LOGIN_TRACKER.pop(login_key, None)


# =====================================================
# Schema Setup / Migrations
# =====================================================


def _constraint_exists(cursor, table: str, constraint_name: str) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM information_schema.table_constraints
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND constraint_name = %s
        LIMIT 1
        """,
        (table, constraint_name),
    )
    return cursor.fetchone() is not None


def _index_exists(cursor, table: str, index_name: str) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND index_name = %s
        LIMIT 1
        """,
        (table, index_name),
    )
    return cursor.fetchone() is not None


def _column_exists(cursor, table: str, column_name: str) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND column_name = %s
        LIMIT 1
        """,
        (table, column_name),
    )
    return cursor.fetchone() is not None


def _safe_schema_change(cursor, sql: str) -> None:
    try:
        cursor.execute(sql)
    except MySQLError:
        logger.exception("Schema change failed: %s", sql)
        if IS_PRODUCTION:
            raise


def _ensure_foreign_key(cursor, table: str, constraint_name: str, definition_sql: str) -> None:
    if _constraint_exists(cursor, table, constraint_name):
        return
    _safe_schema_change(
        cursor,
        f"ALTER TABLE {table} ADD CONSTRAINT {constraint_name} {definition_sql}",
    )


def _ensure_index(cursor, table: str, index_name: str, columns_sql: str, unique: bool = False) -> None:
    if _index_exists(cursor, table, index_name):
        return
    prefix = "CREATE UNIQUE INDEX" if unique else "CREATE INDEX"
    _safe_schema_change(cursor, f"{prefix} {index_name} ON {table} ({columns_sql})")


def _ensure_column(cursor, table: str, column_name: str, definition_sql: str) -> None:
    if _column_exists(cursor, table, column_name):
        return
    _safe_schema_change(cursor, f"ALTER TABLE {table} ADD COLUMN {column_name} {definition_sql}")


def _get_or_create_skill_id(cursor, skill_name: str, category: str | None = None) -> int:
    cursor.execute(
        """
        INSERT INTO skills (skill_name, category)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
        """,
        (skill_name, category),
    )
    return int(cursor.lastrowid)


def _replace_job_skills(cursor, job_id: int, skills: list[str]) -> None:
    cursor.execute("DELETE FROM job_required_skills WHERE job_id=%s", (job_id,))
    for skill_name in _normalize_csv_skills(skills):
        skill_id = _get_or_create_skill_id(cursor, skill_name)
        cursor.execute(
            """
            INSERT IGNORE INTO job_required_skills (job_id, skill_id)
            VALUES (%s, %s)
            """,
            (job_id, skill_id),
        )


def _backfill_job_required_skills(connection) -> None:
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                j.id,
                j.required_skills
            FROM jobs j
            LEFT JOIN job_required_skills jrs ON jrs.job_id = j.id
            GROUP BY j.id, j.required_skills
            HAVING COUNT(jrs.job_id) = 0
               AND COALESCE(j.required_skills, '') <> ''
            """
        )
        rows = cursor.fetchall()
        if not rows:
            return

        for row in rows:
            job_id = int(row["id"])
            skills = [item.strip() for item in (row.get("required_skills") or "").split(",") if item.strip()]
            _replace_job_skills(cursor, job_id, skills)

        connection.commit()
        logger.info("Backfilled normalized required skills for %s jobs", len(rows))
    except MySQLError:
        connection.rollback()
        logger.exception("Backfill for job_required_skills failed")
        if IS_PRODUCTION:
            raise
    finally:
        cursor.close()


def init_database_objects() -> None:
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'student',
                subscription_type VARCHAR(20) NOT NULL DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                skill_name VARCHAR(100) NOT NULL,
                category VARCHAR(100) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                skill_id INT NOT NULL,
                proficiency_level VARCHAR(20) NOT NULL DEFAULT 'beginner',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uniq_user_skill (user_id, skill_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                recruiter_id INT NOT NULL,
                title VARCHAR(150) NOT NULL,
                company_name VARCHAR(150) NOT NULL,
                location VARCHAR(120) NOT NULL DEFAULT 'Remote',
                employment_type VARCHAR(60) NOT NULL DEFAULT 'full-time',
                description TEXT NOT NULL,
                required_skills TEXT NULL,
                salary_range VARCHAR(80) NULL,
                is_active TINYINT(1) NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_required_skills (
                job_id INT NOT NULL,
                skill_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (job_id, skill_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_id INT NOT NULL,
                student_id INT NOT NULL,
                cover_letter TEXT NULL,
                status VARCHAR(30) NOT NULL DEFAULT 'applied',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL DEFAULT NULL,
                UNIQUE KEY uniq_job_student (job_id, student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_resumes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                target_role VARCHAR(150) NOT NULL,
                resume_text LONGTEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS premium_payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                provider VARCHAR(50) NOT NULL,
                payment_reference VARCHAR(150) NOT NULL,
                payment_signature VARCHAR(256) NOT NULL,
                amount_cents INT NULL,
                currency VARCHAR(10) NULL,
                status VARCHAR(30) NOT NULL DEFAULT 'verified',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified_at TIMESTAMP NULL,
                UNIQUE KEY uniq_provider_reference (provider, payment_reference)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_application_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                application_id INT NOT NULL,
                sender_id INT NOT NULL,
                recipient_id INT NOT NULL,
                message_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            """
        )

        # Backward-compatible column migrations for pre-upgrade schemas.
        _ensure_column(cursor, "users", "role", "VARCHAR(20) NOT NULL DEFAULT 'student'")
        _ensure_column(cursor, "users", "subscription_type", "VARCHAR(20) NOT NULL DEFAULT 'free'")
        _ensure_column(cursor, "users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "users", "updated_at", "TIMESTAMP NULL DEFAULT NULL")

        _ensure_column(cursor, "skills", "category", "VARCHAR(100) NULL")
        _ensure_column(cursor, "skills", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        _ensure_column(cursor, "user_skills", "proficiency_level", "VARCHAR(20) NOT NULL DEFAULT 'beginner'")
        _ensure_column(cursor, "user_skills", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        _ensure_column(cursor, "jobs", "location", "VARCHAR(120) NOT NULL DEFAULT 'Remote'")
        _ensure_column(cursor, "jobs", "employment_type", "VARCHAR(60) NOT NULL DEFAULT 'full-time'")
        _ensure_column(cursor, "jobs", "required_skills", "TEXT NULL")
        _ensure_column(cursor, "jobs", "salary_range", "VARCHAR(80) NULL")
        _ensure_column(cursor, "jobs", "is_active", "TINYINT(1) NOT NULL DEFAULT 1")
        _ensure_column(cursor, "jobs", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "jobs", "updated_at", "TIMESTAMP NULL DEFAULT NULL")

        _ensure_column(cursor, "job_applications", "cover_letter", "TEXT NULL")
        _ensure_column(cursor, "job_applications", "status", "VARCHAR(30) NOT NULL DEFAULT 'applied'")
        _ensure_column(cursor, "job_applications", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "job_applications", "updated_at", "TIMESTAMP NULL DEFAULT NULL")

        _ensure_column(cursor, "ai_resumes", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        _ensure_column(cursor, "premium_payments", "amount_cents", "INT NULL")
        _ensure_column(cursor, "premium_payments", "currency", "VARCHAR(10) NULL")
        _ensure_column(cursor, "premium_payments", "status", "VARCHAR(30) NOT NULL DEFAULT 'verified'")
        _ensure_column(cursor, "premium_payments", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "premium_payments", "verified_at", "TIMESTAMP NULL")

        _ensure_column(cursor, "job_application_messages", "application_id", "INT NOT NULL")
        _ensure_column(cursor, "job_application_messages", "sender_id", "INT NOT NULL")
        _ensure_column(cursor, "job_application_messages", "recipient_id", "INT NOT NULL")
        _ensure_column(cursor, "job_application_messages", "message_text", "TEXT NOT NULL")
        _ensure_column(cursor, "job_application_messages", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "job_application_messages", "read_at", "TIMESTAMP NULL DEFAULT NULL")

        _ensure_index(cursor, "users", "idx_users_role", "role")
        _ensure_index(cursor, "users", "idx_users_subscription_type", "subscription_type")
        _ensure_index(cursor, "skills", "uniq_skills_name", "skill_name", unique=True)
        _ensure_index(cursor, "user_skills", "idx_user_skills_user_id", "user_id")
        _ensure_index(cursor, "user_skills", "idx_user_skills_skill_id", "skill_id")
        _ensure_index(cursor, "user_skills", "idx_user_skills_proficiency", "proficiency_level")
        _ensure_index(cursor, "jobs", "idx_jobs_recruiter_id", "recruiter_id")
        _ensure_index(cursor, "jobs", "idx_jobs_created_at", "created_at")
        _ensure_index(cursor, "jobs", "idx_jobs_is_active", "is_active")
        _ensure_index(cursor, "job_applications", "idx_job_applications_job_id", "job_id")
        _ensure_index(cursor, "job_applications", "idx_job_applications_student_id", "student_id")
        _ensure_index(cursor, "job_applications", "idx_job_applications_status", "status")
        _ensure_index(cursor, "ai_resumes", "idx_ai_resumes_user_id", "user_id")
        _ensure_index(cursor, "ai_resumes", "idx_ai_resumes_created_at", "created_at")
        _ensure_index(cursor, "premium_payments", "idx_premium_payments_user_id", "user_id")
        _ensure_index(cursor, "premium_payments", "idx_premium_payments_created_at", "created_at")
        _ensure_index(cursor, "job_application_messages", "idx_jam_application_id", "application_id")
        _ensure_index(cursor, "job_application_messages", "idx_jam_sender_id", "sender_id")
        _ensure_index(cursor, "job_application_messages", "idx_jam_recipient_id", "recipient_id")
        _ensure_index(cursor, "job_application_messages", "idx_jam_created_at", "created_at")
        _ensure_index(cursor, "job_application_messages", "idx_jam_recipient_read", "recipient_id, read_at")

        _ensure_foreign_key(
            cursor,
            "user_skills",
            "fk_user_skills_user",
            "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "user_skills",
            "fk_user_skills_skill",
            "FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "jobs",
            "fk_jobs_recruiter",
            "FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_required_skills",
            "fk_job_required_skills_job",
            "FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_required_skills",
            "fk_job_required_skills_skill",
            "FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_applications",
            "fk_job_applications_job",
            "FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_applications",
            "fk_job_applications_student",
            "FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "ai_resumes",
            "fk_ai_resumes_user",
            "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "premium_payments",
            "fk_premium_payments_user",
            "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_application_messages",
            "fk_jam_application",
            "FOREIGN KEY (application_id) REFERENCES job_applications(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_application_messages",
            "fk_jam_sender",
            "FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE",
        )
        _ensure_foreign_key(
            cursor,
            "job_application_messages",
            "fk_jam_recipient",
            "FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE",
        )

        connection.commit()
        _backfill_job_required_skills(connection)
    except MySQLError:
        connection.rollback()
        logger.exception("Database initialization failed")
        raise
    finally:
        cursor.close()
        connection.close()


@app.on_event("startup")
def on_startup() -> None:
    init_database_objects()


# =====================================================
# Security / Auth Utilities
# =====================================================


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    now = _utc_now()
    expire_at = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": int(expire_at.timestamp()),
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "jti": hashlib.sha256(os.urandom(32)).hexdigest()[:24],
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _decode_access_token(token: str) -> tuple[str, str | None]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc

    email = payload.get("sub")
    role = payload.get("role")

    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=401, detail="Invalid token payload")

    if role is not None and role not in VALID_SYSTEM_ROLES:
        raise HTTPException(status_code=401, detail="Invalid token role")

    return email.strip().lower(), role


def _serialize_user_times(user: dict) -> dict:
    cloned = dict(user)
    if "created_at" in cloned:
        cloned["created_at"] = _to_utc_iso(cloned.get("created_at"))
    if "updated_at" in cloned:
        cloned["updated_at"] = _to_utc_iso(cloned.get("updated_at"))
    return cloned


def _load_user_from_token(token: str) -> dict:
    email, _ = _decode_access_token(token)
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                role,
                COALESCE(subscription_type, 'free') AS subscription_type,
                created_at,
                updated_at
            FROM users
            WHERE email=%s
            LIMIT 1
            """,
            (email,),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return _serialize_user_times(user)
    finally:
        cursor.close()
        connection.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return _load_user_from_token(token)


def ensure_premium(current_user: dict) -> None:
    if current_user.get("subscription_type") != "premium":
        raise HTTPException(
            status_code=403,
            detail="Premium membership required for AI Resume Creator",
        )


def ensure_recruiter_or_admin(current_user: dict) -> None:
    if current_user.get("role") not in {"recruiter", "admin"}:
        raise HTTPException(
            status_code=403,
            detail="Recruiter or admin access required",
        )


def ensure_student(current_user: dict) -> None:
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )


def ensure_admin(current_user: dict) -> None:
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )


def ensure_student_or_recruiter(current_user: dict) -> None:
    if current_user.get("role") not in {"student", "recruiter"}:
        raise HTTPException(
            status_code=403,
            detail="Student or recruiter access required",
        )


def _normalize_message_body(message: str) -> str:
    normalized = message.strip()
    if not normalized:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    return normalized


def _get_message_thread_context(cursor, application_id: int) -> dict | None:
    cursor.execute(
        """
        SELECT
            ja.id AS application_id,
            ja.job_id,
            ja.status AS application_status,
            ja.created_at AS application_created_at,
            ja.updated_at AS application_updated_at,
            j.title AS job_title,
            j.company_name,
            student.id AS student_id,
            student.name AS student_name,
            student.email AS student_email,
            recruiter.id AS recruiter_id,
            recruiter.name AS recruiter_name,
            recruiter.email AS recruiter_email
        FROM job_applications ja
        JOIN jobs j ON j.id = ja.job_id
        JOIN users student ON student.id = ja.student_id
        JOIN users recruiter ON recruiter.id = j.recruiter_id
        WHERE ja.id=%s
        LIMIT 1
        """,
        (application_id,),
    )
    return cursor.fetchone()


def _ensure_message_thread_access(thread_row: dict, current_user: dict) -> None:
    ensure_student_or_recruiter(current_user)

    current_user_id = int(current_user["id"])
    if current_user.get("role") == "student" and current_user_id != int(thread_row["student_id"]):
        raise HTTPException(status_code=403, detail="Not allowed to access this conversation")

    if current_user.get("role") == "recruiter" and current_user_id != int(thread_row["recruiter_id"]):
        raise HTTPException(status_code=403, detail="Not allowed to access this conversation")


def _serialize_message_row(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "application_id": int(row["application_id"]),
        "sender_id": int(row["sender_id"]),
        "recipient_id": int(row["recipient_id"]),
        "sender_name": row["sender_name"],
        "message": row["message_text"],
        "created_at": _to_utc_iso(row.get("created_at")),
        "read_at": _to_utc_iso(row.get("read_at")),
    }


def _serialize_message_thread(row: dict, current_user: dict) -> dict:
    current_user_id = int(current_user["id"])
    is_student_view = current_user_id == int(row["student_id"])

    counterpart = {
        "id": int(row["recruiter_id"] if is_student_view else row["student_id"]),
        "name": row["recruiter_name"] if is_student_view else row["student_name"],
        "email": row["recruiter_email"] if is_student_view else row["student_email"],
        "role": "recruiter" if is_student_view else "student",
    }

    last_message = None
    if row.get("last_message_id"):
        last_message = {
            "id": int(row["last_message_id"]),
            "text": row.get("last_message_text"),
            "created_at": _to_utc_iso(row.get("last_message_at")),
            "sender_name": row.get("last_message_sender_name"),
        }

    latest_activity = row.get("latest_activity_at") or row.get("application_updated_at") or row.get("application_created_at")

    return {
        "application_id": int(row["application_id"]),
        "job_id": int(row["job_id"]),
        "job_title": row["job_title"],
        "company_name": row["company_name"],
        "application_status": row["application_status"],
        "created_at": _to_utc_iso(row.get("application_created_at")),
        "latest_activity_at": _to_utc_iso(latest_activity),
        "unread_count": int(row.get("unread_count") or 0),
        "counterpart": counterpart,
        "last_message": last_message,
    }


def _thread_summary_from_context(
    thread_row: dict,
    current_user: dict,
    unread_count: int = 0,
    last_message_row: dict | None = None,
) -> dict:
    normalized_row = dict(thread_row)
    normalized_row["unread_count"] = unread_count
    if last_message_row:
        normalized_row["last_message_id"] = last_message_row["id"]
        normalized_row["last_message_text"] = last_message_row["message_text"]
        normalized_row["last_message_at"] = last_message_row.get("created_at")
        normalized_row["last_message_sender_name"] = last_message_row["sender_name"]
        normalized_row["latest_activity_at"] = last_message_row.get("created_at")
    return _serialize_message_thread(normalized_row, current_user)


def _mark_thread_messages_as_read(cursor, application_id: int, user_id: int) -> int:
    cursor.execute(
        """
        UPDATE job_application_messages
        SET read_at = CURRENT_TIMESTAMP
        WHERE application_id=%s
          AND recipient_id=%s
          AND read_at IS NULL
        """,
        (application_id, user_id),
    )
    return int(cursor.rowcount or 0)


def _fetch_message_threads(cursor, current_user: dict, limit: int) -> list[dict]:
    ensure_student_or_recruiter(current_user)

    where_sql = "ja.student_id = %s"
    if current_user.get("role") == "recruiter":
        where_sql = "j.recruiter_id = %s"

    query = f"""
        SELECT
            ja.id AS application_id,
            ja.job_id,
            ja.status AS application_status,
            ja.created_at AS application_created_at,
            ja.updated_at AS application_updated_at,
            j.title AS job_title,
            j.company_name,
            student.id AS student_id,
            student.name AS student_name,
            student.email AS student_email,
            recruiter.id AS recruiter_id,
            recruiter.name AS recruiter_name,
            recruiter.email AS recruiter_email,
            last_message.id AS last_message_id,
            last_message.message_text AS last_message_text,
            last_message.created_at AS last_message_at,
            last_sender.name AS last_message_sender_name,
            COALESCE(unread_counts.unread_count, 0) AS unread_count,
            COALESCE(last_message.created_at, ja.updated_at, ja.created_at) AS latest_activity_at
        FROM job_applications ja
        JOIN jobs j ON j.id = ja.job_id
        JOIN users student ON student.id = ja.student_id
        JOIN users recruiter ON recruiter.id = j.recruiter_id
        LEFT JOIN job_application_messages last_message
            ON last_message.id = (
                SELECT jam_last.id
                FROM job_application_messages jam_last
                WHERE jam_last.application_id = ja.id
                ORDER BY jam_last.created_at DESC, jam_last.id DESC
                LIMIT 1
            )
        LEFT JOIN users last_sender ON last_sender.id = last_message.sender_id
        LEFT JOIN (
            SELECT
                application_id,
                COUNT(*) AS unread_count
            FROM job_application_messages
            WHERE recipient_id = %s
              AND read_at IS NULL
            GROUP BY application_id
        ) unread_counts ON unread_counts.application_id = ja.id
        WHERE {where_sql}
        ORDER BY latest_activity_at DESC, ja.id DESC
        LIMIT %s
    """

    cursor.execute(
        query,
        (
            current_user["id"],
            current_user["id"],
            limit,
        ),
    )
    return [_serialize_message_thread(row, current_user) for row in cursor.fetchall()]

def _payment_payload(user_id: int, provider: str, payment_reference: str) -> str:
    return f"{user_id}:{provider}:{payment_reference}"


def _payment_signature(payload: str) -> str:
    return hmac.new(
        PAYMENT_SIGNING_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _verify_payment_signature(user_id: int, provider: str, reference: str, signature: str) -> bool:
    normalized_signature = signature.strip().lower()
    expected_signature = _payment_signature(_payment_payload(user_id, provider, reference))
    return hmac.compare_digest(expected_signature, normalized_signature)

# =====================================================
# Resume Utilities
# =====================================================


def _build_resume_prompt(payload: ResumeGenerateRequest) -> str:
    skills_line = ", ".join(payload.skills) if payload.skills else "No skills provided"
    achievement_lines = (
        "\n".join([f"- {item}" for item in payload.achievements])
        if payload.achievements
        else "- Add measurable achievements from projects/internships."
    )

    return f"""
Create a one-page ATS-friendly resume tailored to this candidate.
Do not force a fixed section template.
Choose section names and order based on target role and experience.
Keep the writing concise, specific, and impact-focused.
If details are missing, use safe neutral wording and do not invent fake employers or dates.

Candidate Profile:
- Full Name: {payload.full_name}
- Target Role: {payload.target_role}
- Years of Experience: {payload.years_experience}
- Skills: {skills_line}
- Education: {payload.education}
- Achievements:
{achievement_lines}

Output Rules:
- Plain text only
- Use bullets where useful
- Keep total length under ~450 words
"""


def _generate_resume_with_openai(prompt: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    if api_key.lower() in {"your_openai_api_key", "your_api_key_here", "replace_me"}:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        max_tokens = int(os.getenv("OPENAI_RESUME_MAX_TOKENS", "900"))
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": AI_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=max_tokens,
        )
        message = completion.choices[0].message.content
        if isinstance(message, str) and message.strip():
            return message.strip()
    except Exception:
        logger.exception("OpenAI resume generation failed")
        return None

    return None


def _generate_resume_fallback(payload: ResumeGenerateRequest) -> str:
    skills_line = ", ".join(payload.skills) if payload.skills else "Problem Solving, Communication"
    achievement_lines = (
        "\n".join([f"- {item}" for item in payload.achievements])
        if payload.achievements
        else "- Built and delivered projects with measurable impact."
    )

    return (
        f"{payload.full_name}\n"
        f"Target Role: {payload.target_role}\n\n"
        "PROFESSIONAL SUMMARY\n"
        f"Result-driven candidate with {payload.years_experience} years of experience, "
        "strong ownership mindset, and a focus on high-quality execution.\n\n"
        "SKILLS\n"
        f"{skills_line}\n\n"
        "EXPERIENCE HIGHLIGHTS\n"
        "- Delivered features/projects from planning to deployment.\n"
        "- Collaborated with cross-functional teams and improved reliability/performance.\n"
        "- Used data/feedback to iterate and improve outcomes.\n\n"
        "EDUCATION\n"
        f"{payload.education}\n\n"
        "KEY ACHIEVEMENTS\n"
        f"{achievement_lines}\n"
    )


def generate_resume_text(payload: ResumeGenerateRequest) -> str:
    prompt = _build_resume_prompt(payload)
    ai_text = _generate_resume_with_openai(prompt)
    if ai_text:
        return ai_text
    return _generate_resume_fallback(payload)


def _parse_skills_csv(skills_csv: str | None) -> list[str]:
    if not skills_csv:
        return []
    return [skill.strip() for skill in skills_csv.split(",") if skill.strip()]


# =====================================================
# Routes
# =====================================================


@app.get("/")
def home():
    return {"message": "SkillConnect API is running"}


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": _to_utc_iso(_utc_now()), "env": APP_ENV}


@app.get("/me", response_model=MeResponse)
def me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.post("/register", status_code=201)
def register_user(user: UserRegister):
    if user.role not in VALID_REGISTRATION_ROLES:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Only student and recruiter registration is allowed.",
        )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email=%s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_pw = hash_password(user.password)
        cursor.execute(
            """
            INSERT INTO users (name, email, password, role, subscription_type)
            VALUES (%s, %s, %s, %s, 'free')
            """,
            (user.name.strip(), user.email, hashed_pw, user.role),
        )
        connection.commit()
        return {"message": "User registered successfully"}
    finally:
        cursor.close()
        connection.close()


@app.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    client_ip = request.client.host if request.client else "unknown"
    normalized_username = form_data.username.strip().lower()
    login_key = _build_login_key(normalized_username, client_ip)

    blocked_seconds = _get_login_block_seconds(login_key)
    if blocked_seconds > 0:
        raise HTTPException(
            status_code=429,
            detail=f"Too many failed attempts. Try again in {blocked_seconds} seconds.",
        )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email=%s
            LIMIT 1
            """,
            (normalized_username,),
        )
        db_user = cursor.fetchone()
        if not db_user or not verify_password(form_data.password, db_user["password"]):
            _record_failed_login(login_key)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        _clear_failed_login(login_key)
        access_token = create_access_token(
            data={
                "sub": db_user["email"],
                "role": db_user["role"],
            }
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": db_user["role"],
            "name": db_user["name"],
        }
    finally:
        cursor.close()
        connection.close()


@app.post("/billing/dev-signature")
def generate_dev_payment_signature(
    payload: DevSignatureRequest,
    current_user: dict = Depends(get_current_user),
):
    if IS_PRODUCTION:
        raise HTTPException(status_code=404, detail="Not found")

    signature = _payment_signature(
        _payment_payload(
            current_user["id"],
            payload.provider.strip(),
            payload.payment_reference.strip(),
        )
    )
    return {
        "provider": payload.provider.strip(),
        "payment_reference": payload.payment_reference.strip(),
        "payment_signature": signature,
    }


@app.post("/upgrade-to-premium")
def upgrade_to_premium(
    payload: PremiumUpgradeRequest,
    current_user: dict = Depends(get_current_user),
):
    provider = payload.provider.strip().lower()
    reference = payload.payment_reference.strip()
    signature = payload.payment_signature.strip()

    if not _verify_payment_signature(current_user["id"], provider, reference, signature):
        raise HTTPException(status_code=400, detail="Payment verification failed")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO premium_payments (
                user_id,
                provider,
                payment_reference,
                payment_signature,
                amount_cents,
                currency,
                status,
                verified_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'verified', CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE
                payment_signature = VALUES(payment_signature),
                amount_cents = VALUES(amount_cents),
                currency = VALUES(currency),
                status = 'verified',
                verified_at = CURRENT_TIMESTAMP
            """,
            (
                current_user["id"],
                provider,
                reference,
                signature,
                payload.amount_cents,
                payload.currency.upper().strip() if payload.currency else None,
            ),
        )
        cursor.execute(
            "UPDATE users SET subscription_type='premium', updated_at=CURRENT_TIMESTAMP WHERE id=%s",
            (current_user["id"],),
        )
        connection.commit()
        return {"message": "Premium upgraded successfully", "subscription_type": "premium"}
    except MySQLError:
        connection.rollback()
        logger.exception("Premium upgrade failed for user_id=%s", current_user["id"])
        raise HTTPException(status_code=500, detail="Failed to process premium upgrade")
    finally:
        cursor.close()
        connection.close()


@app.post("/add-skill")
def add_skill(
    skill: SkillCreate | None = None,
    skill_name: str | None = Query(default=None),
    proficiency_level: str = Query(default="beginner"),
    category: str | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    if skill is not None:
        resolved_skill_name = skill.skill_name.strip()
        resolved_proficiency = skill.proficiency_level
        resolved_category = skill.category.strip() if skill.category else None
    else:
        if skill_name is None or not skill_name.strip():
            raise HTTPException(
                status_code=422,
                detail="Provide skill_name in body or query parameter",
            )
        resolved_skill_name = skill_name.strip()
        resolved_proficiency = proficiency_level.lower().strip()
        resolved_category = category.strip() if category else None

    if resolved_proficiency not in VALID_PROFICIENCY_LEVELS:
        raise HTTPException(
            status_code=400,
            detail="Invalid proficiency level. Use beginner, intermediate, advanced, or expert.",
        )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if current_user["subscription_type"] == "free":
            cursor.execute(
                "SELECT COUNT(*) as count FROM user_skills WHERE user_id=%s",
                (current_user["id"],),
            )
            count = int(cursor.fetchone()["count"])
            if count >= 5:
                raise HTTPException(
                    status_code=403,
                    detail="Free users can add maximum 5 skills. Upgrade to Premium.",
                )

        cursor.execute("START TRANSACTION")
        skill_id = _get_or_create_skill_id(cursor, resolved_skill_name, resolved_category)
        cursor.execute(
            """
            INSERT INTO user_skills (user_id, skill_id, proficiency_level)
            VALUES (%s, %s, %s)
            """,
            (current_user["id"], skill_id, resolved_proficiency),
        )
        connection.commit()
        return {"message": "Skill added successfully"}
    except IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=409, detail="Skill already added")
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception("Failed to add skill for user_id=%s", current_user["id"])
        raise HTTPException(status_code=500, detail="Failed to add skill")
    finally:
        cursor.close()
        connection.close()


@app.get("/my-skills")
def my_skills(current_user: dict = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                us.id,
                s.skill_name AS name,
                s.skill_name,
                s.category,
                us.proficiency_level,
                us.created_at
            FROM user_skills us
            JOIN skills s ON us.skill_id = s.id
            WHERE us.user_id=%s
            ORDER BY s.skill_name ASC
            """,
            (current_user["id"],),
        )
        rows = cursor.fetchall()
        for row in rows:
            row["created_at"] = _to_utc_iso(row.get("created_at"))
        return rows
    finally:
        cursor.close()
        connection.close()


@app.post("/ai-resume/generate", response_model=ResumeGenerateResponse)
def ai_resume_generate(
    payload: ResumeGenerateRequest,
    current_user: dict = Depends(get_current_user),
):
    ensure_student(current_user)
    ensure_premium(current_user)

    resume_text = generate_resume_text(payload)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO ai_resumes (user_id, target_role, resume_text)
            VALUES (%s, %s, %s)
            """,
            (current_user["id"], payload.target_role.strip(), resume_text),
        )
        resume_id = int(cursor.lastrowid)
        connection.commit()

        cursor.execute(
            """
            SELECT created_at
            FROM ai_resumes
            WHERE id=%s
            LIMIT 1
            """,
            (resume_id,),
        )
        row = cursor.fetchone() or {}
        generated_at = _to_utc_iso(row.get("created_at")) or _to_utc_iso(_utc_now())

        return {"resume_text": resume_text, "generated_at": generated_at}
    except MySQLError:
        connection.rollback()
        logger.exception("Failed to generate/store AI resume for user_id=%s", current_user["id"])
        raise HTTPException(status_code=500, detail="Failed to generate resume")
    finally:
        cursor.close()
        connection.close()


@app.get("/ai-resume/history")
def ai_resume_history(
    limit: int = Query(default=20, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    ensure_student(current_user)
    ensure_premium(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                id,
                target_role,
                resume_text,
                created_at
            FROM ai_resumes
            WHERE user_id=%s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (current_user["id"], limit),
        )
        rows = cursor.fetchall()
        for row in rows:
            row["created_at"] = _to_utc_iso(row.get("created_at"))
        return rows
    finally:
        cursor.close()
        connection.close()


@app.get("/jobs")
def list_jobs(
    skill: str | None = Query(default=None),
    company: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    ensure_student(current_user)

    skill_filter = skill.strip() if isinstance(skill, str) and skill.strip() else None
    company_filter = company.strip() if isinstance(company, str) and company.strip() else None

    where_clauses = ["j.is_active = 1"]
    params: list = [current_user["id"]]

    if company_filter:
        where_clauses.append("j.company_name LIKE %s")
        params.append(f"%{company_filter}%")

    if skill_filter:
        where_clauses.append(
            """
            EXISTS (
                SELECT 1
                FROM job_required_skills jrs_filter
                JOIN skills s_filter ON s_filter.id = jrs_filter.skill_id
                WHERE jrs_filter.job_id = j.id
                  AND s_filter.skill_name LIKE %s
            )
            """
        )
        params.append(f"%{skill_filter}%")

    where_sql = " AND ".join(where_clauses)

    query = f"""
        SELECT
            j.id,
            j.title,
            j.company_name,
            j.location,
            j.employment_type,
            j.description,
            j.salary_range,
            j.required_skills AS required_skills_legacy,
            recruiter.name AS recruiter_name,
            COUNT(DISTINCT ja_all.id) AS applicant_count,
            MAX(CASE WHEN ja_mine.id IS NULL THEN 0 ELSE 1 END) AS already_applied,
            GROUP_CONCAT(DISTINCT s.skill_name ORDER BY s.skill_name SEPARATOR ',') AS required_skills_csv,
            j.created_at
        FROM jobs j
        JOIN users recruiter ON recruiter.id = j.recruiter_id
        LEFT JOIN job_required_skills jrs ON jrs.job_id = j.id
        LEFT JOIN skills s ON s.id = jrs.skill_id
        LEFT JOIN job_applications ja_all ON ja_all.job_id = j.id
        LEFT JOIN job_applications ja_mine
            ON ja_mine.job_id = j.id
           AND ja_mine.student_id = %s
        WHERE {where_sql}
        GROUP BY
            j.id,
            j.title,
            j.company_name,
            j.location,
            j.employment_type,
            j.description,
            j.salary_range,
            j.required_skills,
            recruiter.name,
            j.created_at
        ORDER BY j.created_at DESC
        LIMIT %s
    """

    params.append(limit)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        for row in rows:
            skills_csv = row.get("required_skills_csv")
            legacy_skills = row.get("required_skills_legacy")
            row["required_skills"] = _parse_skills_csv(skills_csv or legacy_skills)
            row["applicant_count"] = int(row.get("applicant_count") or 0)
            row["already_applied"] = bool(row.get("already_applied"))
            row["created_at"] = _to_utc_iso(row.get("created_at"))
            row.pop("required_skills_csv", None)
            row.pop("required_skills_legacy", None)
        return rows
    finally:
        cursor.close()
        connection.close()


@app.post("/jobs/{job_id}/apply", status_code=201)
def apply_to_job(
    job_id: int,
    payload: JobApplyRequest,
    current_user: dict = Depends(get_current_user),
):
    ensure_student(current_user)

    cover_letter = payload.cover_letter.strip() if payload.cover_letter else None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id
            FROM jobs
            WHERE id=%s
              AND is_active=1
            LIMIT 1
            """,
            (job_id,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job not found or inactive")

        cursor.execute(
            """
            INSERT INTO job_applications (job_id, student_id, cover_letter, status)
            VALUES (%s, %s, %s, 'applied')
            """,
            (job_id, current_user["id"], cover_letter),
        )
        connection.commit()
        return {"message": "Application submitted successfully"}
    except IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=409, detail="You already applied to this job")
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception("Failed to apply for job_id=%s by user_id=%s", job_id, current_user["id"])
        raise HTTPException(status_code=500, detail="Failed to submit application")
    finally:
        cursor.close()
        connection.close()


@app.get("/student/applications")
def student_applications(current_user: dict = Depends(get_current_user)):
    ensure_student(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                ja.id,
                ja.job_id,
                j.title,
                j.company_name,
                ja.status,
                ja.cover_letter,
                ja.created_at,
                ja.updated_at
            FROM job_applications ja
            JOIN jobs j ON j.id = ja.job_id
            WHERE ja.student_id=%s
            ORDER BY ja.created_at DESC
            """,
            (current_user["id"],),
        )
        rows = cursor.fetchall()
        for row in rows:
            row["created_at"] = _to_utc_iso(row.get("created_at"))
            row["updated_at"] = _to_utc_iso(row.get("updated_at"))
        return rows
    finally:
        cursor.close()
        connection.close()


@app.get("/messages/threads")
def list_message_threads(
    limit: int = Query(default=100, ge=1, le=300),
    current_user: dict = Depends(get_current_user),
):
    ensure_student_or_recruiter(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        return _fetch_message_threads(cursor, current_user, limit)
    finally:
        cursor.close()
        connection.close()


@app.get("/messages/threads/{application_id}")
def get_message_thread(
    application_id: int,
    current_user: dict = Depends(get_current_user),
):
    ensure_student_or_recruiter(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        thread_row = _get_message_thread_context(cursor, application_id)
        if not thread_row:
            raise HTTPException(status_code=404, detail="Conversation not found")

        _ensure_message_thread_access(thread_row, current_user)
        _mark_thread_messages_as_read(cursor, application_id, int(current_user["id"]))
        connection.commit()

        cursor.execute(
            """
            SELECT
                jam.id,
                jam.application_id,
                jam.sender_id,
                jam.recipient_id,
                jam.message_text,
                jam.created_at,
                jam.read_at,
                sender.name AS sender_name
            FROM job_application_messages jam
            JOIN users sender ON sender.id = jam.sender_id
            WHERE jam.application_id=%s
            ORDER BY jam.created_at ASC, jam.id ASC
            LIMIT 500
            """,
            (application_id,),
        )
        message_rows = cursor.fetchall()
        last_message_row = message_rows[-1] if message_rows else None

        return {
            "thread": _thread_summary_from_context(
                thread_row,
                current_user,
                unread_count=0,
                last_message_row=last_message_row,
            ),
            "messages": [_serialize_message_row(row) for row in message_rows],
        }
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception(
            "Failed to load message thread application_id=%s for user_id=%s",
            application_id,
            current_user["id"],
        )
        raise HTTPException(status_code=500, detail="Failed to load conversation")
    finally:
        cursor.close()
        connection.close()


@app.post("/messages/threads/{application_id}")
async def send_message_to_thread(
    application_id: int,
    payload: MessageCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    ensure_student_or_recruiter(current_user)

    message_text = _normalize_message_body(payload.message)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        thread_row = _get_message_thread_context(cursor, application_id)
        if not thread_row:
            raise HTTPException(status_code=404, detail="Conversation not found")

        _ensure_message_thread_access(thread_row, current_user)

        current_user_id = int(current_user["id"])
        recipient_id = (
            int(thread_row["recruiter_id"])
            if current_user_id == int(thread_row["student_id"])
            else int(thread_row["student_id"])
        )

        cursor.execute(
            """
            INSERT INTO job_application_messages (
                application_id,
                sender_id,
                recipient_id,
                message_text
            )
            VALUES (%s, %s, %s, %s)
            """,
            (application_id, current_user_id, recipient_id, message_text),
        )
        message_id = int(cursor.lastrowid)

        cursor.execute(
            """
            SELECT
                jam.id,
                jam.application_id,
                jam.sender_id,
                jam.recipient_id,
                jam.message_text,
                jam.created_at,
                jam.read_at,
                sender.name AS sender_name
            FROM job_application_messages jam
            JOIN users sender ON sender.id = jam.sender_id
            WHERE jam.id=%s
            LIMIT 1
            """,
            (message_id,),
        )
        message_row = cursor.fetchone()
        connection.commit()

        serialized_message = _serialize_message_row(message_row)
        await message_connections.send_to_users(
            {current_user_id, recipient_id},
            {
                "type": "message.created",
                "application_id": application_id,
                "message": serialized_message,
            },
        )
        return {
            "thread": _thread_summary_from_context(
                thread_row,
                current_user,
                unread_count=0,
                last_message_row=message_row,
            ),
            "message": serialized_message,
        }
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception(
            "Failed to send message for application_id=%s by user_id=%s",
            application_id,
            current_user["id"],
        )
        raise HTTPException(status_code=500, detail="Failed to send message")
    finally:
        cursor.close()
        connection.close()


@app.post("/messages/threads/{application_id}/read")
def mark_thread_as_read(
    application_id: int,
    current_user: dict = Depends(get_current_user),
):
    ensure_student_or_recruiter(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        thread_row = _get_message_thread_context(cursor, application_id)
        if not thread_row:
            raise HTTPException(status_code=404, detail="Conversation not found")

        _ensure_message_thread_access(thread_row, current_user)
        updated_count = _mark_thread_messages_as_read(cursor, application_id, int(current_user["id"]))
        connection.commit()
        return {
            "application_id": application_id,
            "marked_read": updated_count,
        }
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception(
            "Failed to mark conversation as read application_id=%s for user_id=%s",
            application_id,
            current_user["id"],
        )
        raise HTTPException(status_code=500, detail="Failed to update read status")
    finally:
        cursor.close()
        connection.close()


@app.websocket("/ws/messages")
async def messages_websocket(websocket: WebSocket):
    token = websocket.query_params.get("token", "").strip()
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        current_user = _load_user_from_token(token)
        ensure_student_or_recruiter(current_user)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    current_user_id = int(current_user["id"])
    await message_connections.connect(current_user_id, websocket)
    await websocket.send_json(
        {
            "type": "connection.ready",
            "user_id": current_user_id,
        }
    )

    try:
        while True:
            payload = await websocket.receive_json()
            if isinstance(payload, dict) and payload.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("Messages websocket disconnected unexpectedly for user_id=%s", current_user_id)
    finally:
        await message_connections.disconnect(current_user_id, websocket)


@app.get("/recruiter/candidates")
def recruiter_candidates(
    skill: str | None = Query(default=None),
    name: str | None = Query(default=None),
    proficiency: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    ensure_recruiter_or_admin(current_user)

    skill_filter = skill.strip() if isinstance(skill, str) and skill.strip() else None
    name_filter = name.strip() if isinstance(name, str) and name.strip() else None
    proficiency_filter = (
        proficiency.strip().lower()
        if isinstance(proficiency, str) and proficiency.strip()
        else None
    )
    if proficiency_filter == "all":
        proficiency_filter = None
    if proficiency_filter and proficiency_filter not in VALID_PROFICIENCY_LEVELS:
        raise HTTPException(
            status_code=400,
            detail="Invalid proficiency level. Use beginner, intermediate, advanced, or expert.",
        )

    where_clauses = ["u.role = 'student'"]
    params: list = []

    if name_filter:
        where_clauses.append("u.name LIKE %s")
        params.append(f"%{name_filter}%")

    if skill_filter:
        skill_exists_sql = """
            EXISTS (
                SELECT 1
                FROM user_skills us_filter
                JOIN skills s_filter ON s_filter.id = us_filter.skill_id
                WHERE us_filter.user_id = u.id
                  AND s_filter.skill_name LIKE %s
        """
        params.append(f"%{skill_filter}%")
        if proficiency_filter:
            skill_exists_sql += " AND us_filter.proficiency_level = %s"
            params.append(proficiency_filter)
        skill_exists_sql += ")"
        where_clauses.append(skill_exists_sql)
    elif proficiency_filter:
        where_clauses.append(
            """
            EXISTS (
                SELECT 1
                FROM user_skills us_filter
                WHERE us_filter.user_id = u.id
                  AND us_filter.proficiency_level = %s
            )
            """
        )
        params.append(proficiency_filter)

    where_sql = " AND ".join(where_clauses)
    query = f"""
        SELECT
            u.id,
            u.name,
            u.email,
            COALESCE(u.subscription_type, 'free') AS subscription_type,
            COUNT(DISTINCT us.skill_id) AS total_skills
        FROM users u
        LEFT JOIN user_skills us ON us.user_id = u.id
        WHERE {where_sql}
        GROUP BY u.id, u.name, u.email, u.subscription_type
        ORDER BY u.id DESC
        LIMIT %s
    """

    params.append(limit)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, tuple(params))
        candidates = cursor.fetchall()
        if not candidates:
            return []

        candidate_ids = [int(item["id"]) for item in candidates]
        placeholders = ", ".join(["%s"] * len(candidate_ids))
        cursor.execute(
            f"""
            SELECT
                us.user_id,
                s.skill_name AS name,
                us.proficiency_level
            FROM user_skills us
            JOIN skills s ON s.id = us.skill_id
            WHERE us.user_id IN ({placeholders})
            ORDER BY s.skill_name ASC
            """,
            tuple(candidate_ids),
        )
        skill_rows = cursor.fetchall()

        skills_by_user: dict[int, list[dict]] = {}
        for item in skill_rows:
            user_id = int(item["user_id"])
            skills_by_user.setdefault(user_id, []).append(
                {
                    "name": item["name"],
                    "proficiency_level": item["proficiency_level"],
                }
            )

        for item in candidates:
            user_id = int(item["id"])
            item["total_skills"] = int(item.get("total_skills") or 0)
            item["skills"] = skills_by_user.get(user_id, [])

        return candidates
    finally:
        cursor.close()
        connection.close()


@app.post("/recruiter/jobs", status_code=201)
def create_recruiter_job(
    payload: JobCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    ensure_recruiter_or_admin(current_user)

    normalized_skills = _normalize_csv_skills(payload.required_skills)
    required_skills_csv = ", ".join(normalized_skills) if normalized_skills else None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO jobs (
                recruiter_id,
                title,
                company_name,
                location,
                employment_type,
                description,
                required_skills,
                salary_range
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                current_user["id"],
                payload.title.strip(),
                payload.company_name.strip(),
                payload.location.strip(),
                payload.employment_type,
                payload.description.strip(),
                required_skills_csv,
                payload.salary_range.strip() if payload.salary_range else None,
            ),
        )
        job_id = int(cursor.lastrowid)
        _replace_job_skills(cursor, job_id, normalized_skills)
        connection.commit()
        return {"message": "Job posted successfully", "job_id": job_id}
    except MySQLError:
        connection.rollback()
        logger.exception("Failed to create job by user_id=%s", current_user["id"])
        raise HTTPException(status_code=500, detail="Failed to post job")
    finally:
        cursor.close()
        connection.close()


@app.get("/recruiter/jobs")
def recruiter_jobs(
    limit: int = Query(default=100, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
):
    ensure_recruiter_or_admin(current_user)

    where_sql = "j.recruiter_id = %s"
    params: list = [current_user["id"]]
    if current_user.get("role") == "admin":
        where_sql = "1 = 1"
        params = []

    query = f"""
        SELECT
            j.id,
            j.recruiter_id,
            recruiter.name AS recruiter_name,
            j.title,
            j.company_name,
            j.location,
            j.employment_type,
            j.description,
            j.salary_range,
            j.is_active,
            j.required_skills AS required_skills_legacy,
            GROUP_CONCAT(DISTINCT s.skill_name ORDER BY s.skill_name SEPARATOR ',') AS required_skills_csv,
            COUNT(DISTINCT ja.id) AS applicant_count,
            j.created_at,
            j.updated_at
        FROM jobs j
        LEFT JOIN users recruiter ON recruiter.id = j.recruiter_id
        LEFT JOIN job_required_skills jrs ON jrs.job_id = j.id
        LEFT JOIN skills s ON s.id = jrs.skill_id
        LEFT JOIN job_applications ja ON ja.job_id = j.id
        WHERE {where_sql}
        GROUP BY
            j.id,
            j.recruiter_id,
            recruiter.name,
            j.title,
            j.company_name,
            j.location,
            j.employment_type,
            j.description,
            j.salary_range,
            j.is_active,
            j.required_skills,
            j.created_at,
            j.updated_at
        ORDER BY j.created_at DESC
        LIMIT %s
    """

    params.append(limit)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        for row in rows:
            skills_csv = row.get("required_skills_csv")
            legacy_skills = row.get("required_skills_legacy")
            row["required_skills"] = _parse_skills_csv(skills_csv or legacy_skills)
            row["applicant_count"] = int(row.get("applicant_count") or 0)
            row["is_active"] = bool(row.get("is_active"))
            row["created_at"] = _to_utc_iso(row.get("created_at"))
            row["updated_at"] = _to_utc_iso(row.get("updated_at"))
            row.pop("required_skills_csv", None)
            row.pop("required_skills_legacy", None)
        return rows
    finally:
        cursor.close()
        connection.close()


@app.get("/recruiter/jobs/{job_id}/applications")
def recruiter_job_applications(
    job_id: int,
    current_user: dict = Depends(get_current_user),
):
    ensure_recruiter_or_admin(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, recruiter_id
            FROM jobs
            WHERE id=%s
            LIMIT 1
            """,
            (job_id,),
        )
        job_row = cursor.fetchone()
        if not job_row:
            raise HTTPException(status_code=404, detail="Job not found")

        if current_user.get("role") != "admin" and int(job_row["recruiter_id"]) != int(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not allowed to access this job")

        cursor.execute(
            """
            SELECT
                ja.id,
                ja.job_id,
                ja.status,
                ja.cover_letter,
                ja.created_at,
                ja.updated_at,
                student.id AS student_id,
                student.name AS student_name,
                student.email AS student_email
            FROM job_applications ja
            JOIN users student ON student.id = ja.student_id
            WHERE ja.job_id=%s
            ORDER BY ja.created_at DESC
            """,
            (job_id,),
        )
        rows = cursor.fetchall()
        for row in rows:
            row["created_at"] = _to_utc_iso(row.get("created_at"))
            row["updated_at"] = _to_utc_iso(row.get("updated_at"))
        return rows
    finally:
        cursor.close()
        connection.close()


@app.patch("/recruiter/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    payload: JobApplicationStatusUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    ensure_recruiter_or_admin(current_user)
    normalized_status = payload.status.lower().strip()

    if normalized_status not in VALID_APPLICATION_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid application status",
        )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                ja.id,
                j.recruiter_id
            FROM job_applications ja
            JOIN jobs j ON j.id = ja.job_id
            WHERE ja.id=%s
            LIMIT 1
            """,
            (application_id,),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Application not found")

        if current_user.get("role") != "admin" and int(row["recruiter_id"]) != int(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not allowed to update this application")

        cursor.execute(
            """
            UPDATE job_applications
            SET status=%s,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=%s
            """,
            (normalized_status, application_id),
        )
        connection.commit()
        return {"message": "Application status updated", "status": normalized_status}
    except HTTPException:
        connection.rollback()
        raise
    except MySQLError:
        connection.rollback()
        logger.exception(
            "Failed to update application status application_id=%s by user_id=%s",
            application_id,
            current_user["id"],
        )
        raise HTTPException(status_code=500, detail="Failed to update application status")
    finally:
        cursor.close()
        connection.close()


@app.get("/admin/overview")
def admin_overview(
    limit: int = Query(default=300, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
):
    ensure_admin(current_user)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_users,
                COALESCE(SUM(CASE WHEN role = 'student' THEN 1 ELSE 0 END), 0) AS students,
                COALESCE(SUM(CASE WHEN role = 'recruiter' THEN 1 ELSE 0 END), 0) AS recruiters,
                COALESCE(SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END), 0) AS admins,
                COALESCE(SUM(CASE WHEN subscription_type = 'premium' THEN 1 ELSE 0 END), 0) AS premium_users
            FROM users
            """
        )
        summary = cursor.fetchone() or {}

        cursor.execute("SELECT COUNT(*) AS total_skills FROM user_skills")
        summary["total_skills"] = int((cursor.fetchone() or {}).get("total_skills") or 0)

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_jobs,
                COALESCE(SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END), 0) AS active_jobs
            FROM jobs
            """
        )
        jobs_count = cursor.fetchone() or {}
        summary["total_jobs"] = int(jobs_count.get("total_jobs") or 0)
        summary["active_jobs"] = int(jobs_count.get("active_jobs") or 0)

        cursor.execute("SELECT COUNT(*) AS total_applications FROM job_applications")
        summary["total_applications"] = int((cursor.fetchone() or {}).get("total_applications") or 0)

        cursor.execute("SELECT COUNT(*) AS total_ai_resumes FROM ai_resumes")
        summary["total_ai_resumes"] = int((cursor.fetchone() or {}).get("total_ai_resumes") or 0)

        summary["total_users"] = int(summary.get("total_users") or 0)
        summary["students"] = int(summary.get("students") or 0)
        summary["recruiters"] = int(summary.get("recruiters") or 0)
        summary["admins"] = int(summary.get("admins") or 0)
        summary["premium_users"] = int(summary.get("premium_users") or 0)

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                role,
                COALESCE(subscription_type, 'free') AS subscription_type,
                created_at,
                updated_at
            FROM users
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,),
        )
        users = cursor.fetchall()
        for row in users:
            row["created_at"] = _to_utc_iso(row.get("created_at"))
            row["updated_at"] = _to_utc_iso(row.get("updated_at"))

        cursor.execute(
            """
            SELECT
                us.id,
                us.user_id,
                u.name AS user_name,
                u.email AS user_email,
                us.skill_id,
                s.skill_name,
                s.category,
                us.proficiency_level,
                us.created_at
            FROM user_skills us
            JOIN users u ON u.id = us.user_id
            JOIN skills s ON s.id = us.skill_id
            ORDER BY us.id DESC
            LIMIT %s
            """,
            (limit,),
        )
        user_skills = cursor.fetchall()
        for row in user_skills:
            row["created_at"] = _to_utc_iso(row.get("created_at"))

        cursor.execute(
            """
            SELECT
                j.id,
                j.recruiter_id,
                recruiter.name AS recruiter_name,
                j.title,
                j.company_name,
                j.location,
                j.employment_type,
                j.salary_range,
                j.is_active,
                j.created_at,
                COUNT(DISTINCT ja.id) AS applicant_count
            FROM jobs j
            LEFT JOIN users recruiter ON recruiter.id = j.recruiter_id
            LEFT JOIN job_applications ja ON ja.job_id = j.id
            GROUP BY
                j.id,
                j.recruiter_id,
                recruiter.name,
                j.title,
                j.company_name,
                j.location,
                j.employment_type,
                j.salary_range,
                j.is_active,
                j.created_at
            ORDER BY j.id DESC
            LIMIT %s
            """,
            (limit,),
        )
        jobs = cursor.fetchall()
        for row in jobs:
            row["is_active"] = bool(row.get("is_active"))
            row["applicant_count"] = int(row.get("applicant_count") or 0)
            row["created_at"] = _to_utc_iso(row.get("created_at"))

        cursor.execute(
            """
            SELECT
                ja.id,
                ja.job_id,
                j.title AS job_title,
                ja.student_id,
                student.name AS student_name,
                student.email AS student_email,
                ja.status,
                ja.cover_letter,
                ja.created_at
            FROM job_applications ja
            JOIN jobs j ON j.id = ja.job_id
            JOIN users student ON student.id = ja.student_id
            ORDER BY ja.id DESC
            LIMIT %s
            """,
            (limit,),
        )
        applications = cursor.fetchall()
        for row in applications:
            row["created_at"] = _to_utc_iso(row.get("created_at"))

        cursor.execute(
            """
            SELECT
                ar.id,
                ar.user_id,
                u.name AS user_name,
                u.email AS user_email,
                ar.target_role,
                LEFT(ar.resume_text, 300) AS resume_preview,
                ar.created_at
            FROM ai_resumes ar
            JOIN users u ON u.id = ar.user_id
            ORDER BY ar.id DESC
            LIMIT %s
            """,
            (limit,),
        )
        ai_resumes = cursor.fetchall()
        for row in ai_resumes:
            row["created_at"] = _to_utc_iso(row.get("created_at"))

        return {
            "summary": summary,
            "users": users,
            "user_skills": user_skills,
            "jobs": jobs,
            "applications": applications,
            "ai_resumes": ai_resumes,
        }
    finally:
        cursor.close()
        connection.close()
