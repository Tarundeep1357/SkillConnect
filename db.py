import os
from functools import lru_cache

import mysql.connector
from mysql.connector import pooling


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=1)
def _read_local_env_map() -> dict[str, str]:
    values: dict[str, str] = {}
    for filename in (".env", ".env.local"):
        path = os.path.join(PROJECT_ROOT, filename)
        if not os.path.isfile(path):
            continue

        with open(path, encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.lower().startswith("export "):
                    line = line[7:].strip()
                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue

                if len(value) >= 2 and (
                    (value[0] == '"' and value[-1] == '"')
                    or (value[0] == "'" and value[-1] == "'")
                ):
                    value = value[1:-1]

                values[key] = value

    return values


def _read_setting(name: str, fallback: str | None = None) -> str | None:
    env_value = os.getenv(name)
    if env_value is not None and str(env_value).strip():
        return str(env_value).strip()

    file_value = _read_local_env_map().get(name)
    if file_value is not None and str(file_value).strip():
        return str(file_value).strip()

    return fallback


def _read_env(name: str, fallback: str | None = None) -> str:
    value = _read_setting(name, fallback)
    if value is None or not str(value).strip():
        raise RuntimeError(f"Missing required environment variable: {name}")
    return str(value).strip()


def _read_db_config() -> dict:
    app_env = _read_setting("APP_ENV", "development").strip().lower()
    is_production = app_env == "production"

    if is_production:
        host = _read_env("DB_HOST")
        user = _read_env("DB_USER")
        password = _read_env("DB_PASSWORD")
        database = _read_env("DB_NAME")
        port = int(_read_env("DB_PORT", "3306"))
    else:
        host = _read_setting("DB_HOST", "localhost")
        user = _read_setting("DB_USER", "root")
        password = _read_setting("DB_PASSWORD", "")
        database = _read_setting("DB_NAME", "DBMS_project")
        port = int(_read_setting("DB_PORT", "3306"))

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "charset": _read_setting("DB_CHARSET", "utf8"),
        "use_pure": True,
        "use_unicode": True,
        "autocommit": False,
    }


@lru_cache(maxsize=1)
def _get_pool() -> pooling.MySQLConnectionPool:
    config = _read_db_config()
    pool_size = int(_read_setting("DB_POOL_SIZE", "10"))
    return pooling.MySQLConnectionPool(
        pool_name="skillconnect_pool",
        pool_size=max(1, pool_size),
        pool_reset_session=True,
        **config,
    )


def get_db_connection():
    return _get_pool().get_connection()
