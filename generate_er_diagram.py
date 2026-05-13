from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont


@dataclass
class Entity:
    name: str
    attrs: List[str]
    x: int
    y: int
    w: int


@dataclass
class Relationship:
    left: str
    right: str
    left_side: str
    right_side: str
    card_left: str
    card_right: str
    label: str


CANVAS_W = 3200
CANVAS_H = 2000
HEADER_H = 58
LINE_H = 30
TOP_PAD = 16
BOTTOM_PAD = 16


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if bold:
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def entity_height(entity: Entity) -> int:
    return HEADER_H + TOP_PAD + (len(entity.attrs) * LINE_H) + BOTTOM_PAD


def anchor(box: Tuple[int, int, int, int], side: str) -> Tuple[int, int]:
    x, y, w, h = box
    if side == "left":
        return (x, y + h // 2)
    if side == "right":
        return (x + w, y + h // 2)
    if side == "top":
        return (x + w // 2, y)
    if side == "bottom":
        return (x + w // 2, y + h)
    raise ValueError(f"Unsupported side: {side}")


def draw_multiline_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: int,
    cy: int,
    font: ImageFont.ImageFont,
    fill: Tuple[int, int, int],
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=fill)


def main() -> None:
    title_font = load_font(44, bold=True)
    entity_title_font = load_font(24, bold=True)
    attr_font = load_font(18)
    rel_font = load_font(16, bold=True)
    card_font = load_font(20, bold=True)
    rule_title_font = load_font(24, bold=True)
    rule_font = load_font(17)

    entities = [
        Entity(
            name="USERS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "name : VARCHAR(100) NOT NULL",
                "UK email : VARCHAR(255) NOT NULL",
                "password : VARCHAR(255) NOT NULL",
                "role : VARCHAR(20) DEFAULT 'student'",
                "subscription_type : VARCHAR(20) DEFAULT 'free'",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at : TIMESTAMP NULL",
            ],
            x=60,
            y=120,
            w=980,
        ),
        Entity(
            name="SKILLS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "UK skill_name : VARCHAR(100) NOT NULL",
                "category : VARCHAR(100) NULL",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            ],
            x=1120,
            y=120,
            w=960,
        ),
        Entity(
            name="USER_SKILLS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK user_id -> users.id",
                "FK skill_id -> skills.id",
                "proficiency_level : VARCHAR(20) DEFAULT 'beginner'",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "UK (user_id, skill_id)",
            ],
            x=60,
            y=640,
            w=980,
        ),
        Entity(
            name="JOBS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK recruiter_id -> users.id",
                "title : VARCHAR(150) NOT NULL",
                "company_name : VARCHAR(150) NOT NULL",
                "location : VARCHAR(120) DEFAULT 'Remote'",
                "employment_type : VARCHAR(60) DEFAULT 'full-time'",
                "description : TEXT NOT NULL",
                "required_skills : TEXT NULL",
                "salary_range : VARCHAR(80) NULL",
                "is_active : TINYINT(1) DEFAULT 1",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at : TIMESTAMP NULL",
            ],
            x=1120,
            y=470,
            w=1220,
        ),
        Entity(
            name="JOB_REQUIRED_SKILLS",
            attrs=[
                "PK,FK job_id -> jobs.id",
                "PK,FK skill_id -> skills.id",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            ],
            x=2420,
            y=640,
            w=720,
        ),
        Entity(
            name="JOB_APPLICATIONS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK job_id -> jobs.id",
                "FK student_id -> users.id",
                "cover_letter : TEXT NULL",
                "status : VARCHAR(30) DEFAULT 'applied'",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at : TIMESTAMP NULL",
                "UK (job_id, student_id)",
            ],
            x=60,
            y=1290,
            w=1100,
        ),
        Entity(
            name="AI_RESUMES",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK user_id -> users.id",
                "target_role : VARCHAR(150) NOT NULL",
                "resume_text : LONGTEXT NOT NULL",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            ],
            x=1240,
            y=1360,
            w=900,
        ),
        Entity(
            name="PREMIUM_PAYMENTS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK user_id -> users.id",
                "provider : VARCHAR(50) NOT NULL",
                "payment_reference : VARCHAR(150) NOT NULL",
                "payment_signature : VARCHAR(256) NOT NULL",
                "amount_cents : INT NULL",
                "currency : VARCHAR(10) NULL",
                "status : VARCHAR(30) DEFAULT 'verified'",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "verified_at : TIMESTAMP NULL",
                "UK (provider, payment_reference)",
            ],
            x=2220,
            y=1220,
            w=920,
        ),
        Entity(
            name="PROJECTS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK user_id -> users.id",
                "title : VARCHAR(200) NOT NULL",
                "description : TEXT NULL",
                "tech_stack : VARCHAR(255) NULL",
                "project_link : VARCHAR(255) NULL",
                "created_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            ],
            x=1120,
            y=1640,
            w=980,
        ),
        Entity(
            name="CERTIFICATIONS",
            attrs=[
                "PK id : INT AUTO_INCREMENT",
                "FK user_id -> users.id",
                "certificate_name : VARCHAR(255) NOT NULL",
                "organization : VARCHAR(255) NULL",
                "issue_date : DATE NULL",
            ],
            x=2140,
            y=1640,
            w=1000,
        ),
    ]

    relations = [
        Relationship("USERS", "USER_SKILLS", "bottom", "top", "1", "N", "has"),
        Relationship("SKILLS", "USER_SKILLS", "left", "right", "1", "N", "appears_in"),
        Relationship("USERS", "JOBS", "bottom", "top", "1", "N", "posts"),
        Relationship("JOBS", "JOB_REQUIRED_SKILLS", "right", "left", "1", "N", "requires"),
        Relationship("SKILLS", "JOB_REQUIRED_SKILLS", "bottom", "top", "1", "N", "mapped_to"),
        Relationship("JOBS", "JOB_APPLICATIONS", "left", "right", "1", "N", "receives"),
        Relationship("USERS", "JOB_APPLICATIONS", "bottom", "top", "1", "N", "submits"),
        Relationship("USERS", "AI_RESUMES", "right", "left", "1", "N", "owns"),
        Relationship("USERS", "PREMIUM_PAYMENTS", "right", "left", "1", "N", "makes"),
        Relationship("USERS", "PROJECTS", "bottom", "top", "1", "N", "builds"),
        Relationship("USERS", "CERTIFICATIONS", "bottom", "top", "1", "N", "earns"),
    ]

    image = Image.new("RGB", (CANVAS_W, CANVAS_H), (250, 252, 255))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (20, 20, CANVAS_W - 20, CANVAS_H - 20),
        radius=18,
        outline=(208, 214, 226),
        width=3,
        fill=(250, 252, 255),
    )

    draw_multiline_centered(
        draw,
        "SkillConnect ER Diagram (Attributes + Relationships + Rules)",
        CANVAS_W // 2,
        56,
        title_font,
        (25, 34, 57),
    )

    palette = {
        "header": (35, 79, 145),
        "body": (239, 245, 255),
        "border": (48, 90, 156),
        "text": (25, 31, 45),
        "line": (60, 71, 92),
        "line_label_bg": (255, 255, 255),
        "rule_bg": (245, 249, 240),
        "rule_border": (104, 139, 85),
    }

    entity_boxes: Dict[str, Tuple[int, int, int, int]] = {}
    for entity in entities:
        h = entity_height(entity)
        entity_boxes[entity.name] = (entity.x, entity.y, entity.w, h)

        # Body
        draw.rounded_rectangle(
            (entity.x, entity.y, entity.x + entity.w, entity.y + h),
            radius=12,
            outline=palette["border"],
            width=3,
            fill=palette["body"],
        )
        # Header
        draw.rounded_rectangle(
            (entity.x, entity.y, entity.x + entity.w, entity.y + HEADER_H),
            radius=12,
            outline=palette["border"],
            width=3,
            fill=palette["header"],
        )
        # Hide lower header curve for clean divider
        draw.rectangle(
            (entity.x, entity.y + HEADER_H - 12, entity.x + entity.w, entity.y + HEADER_H),
            fill=palette["header"],
        )
        draw.line(
            (entity.x, entity.y + HEADER_H, entity.x + entity.w, entity.y + HEADER_H),
            fill=palette["border"],
            width=3,
        )

        draw_multiline_centered(
            draw,
            entity.name,
            entity.x + entity.w // 2,
            entity.y + HEADER_H // 2 + 2,
            entity_title_font,
            (255, 255, 255),
        )

        ay = entity.y + HEADER_H + TOP_PAD
        for attr in entity.attrs:
            draw.text((entity.x + 16, ay), attr, font=attr_font, fill=palette["text"])
            ay += LINE_H

    for rel in relations:
        left_box = entity_boxes[rel.left]
        right_box = entity_boxes[rel.right]
        p1 = anchor(left_box, rel.left_side)
        p2 = anchor(right_box, rel.right_side)

        draw.line((p1, p2), fill=palette["line"], width=4)

        # Relationship label with white capsule.
        mx = (p1[0] + p2[0]) // 2
        my = (p1[1] + p2[1]) // 2
        lb = draw.textbbox((0, 0), rel.label, font=rel_font)
        l_w = (lb[2] - lb[0]) + 16
        l_h = (lb[3] - lb[1]) + 10
        draw.rounded_rectangle(
            (mx - l_w // 2, my - l_h // 2, mx + l_w // 2, my + l_h // 2),
            radius=8,
            fill=palette["line_label_bg"],
            outline=(175, 184, 201),
            width=2,
        )
        draw.text((mx - (l_w // 2) + 8, my - (l_h // 2) + 4), rel.label, font=rel_font, fill=(32, 42, 65))

        # Cardinalities near endpoints.
        draw.text((p1[0] + 8, p1[1] - 26), rel.card_left, font=card_font, fill=(139, 0, 0))
        draw.text((p2[0] - 26, p2[1] - 26), rel.card_right, font=card_font, fill=(139, 0, 0))

    # Rules panel
    panel_x, panel_y, panel_w, panel_h = 2140, 70, 1000, 470
    draw.rounded_rectangle(
        (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
        radius=14,
        fill=palette["rule_bg"],
        outline=palette["rule_border"],
        width=3,
    )
    draw.text((panel_x + 16, panel_y + 14), "Core Rules", font=rule_title_font, fill=(44, 78, 28))

    rules = [
        "1. All listed FKs use ON DELETE CASCADE.",
        "2. M:N via USER_SKILLS and JOB_REQUIRED_SKILLS.",
        "3. UK users.email and skills.skill_name.",
        "4. UK (user_id, skill_id) in USER_SKILLS.",
        "5. UK (job_id, student_id) in JOB_APPLICATIONS.",
        "6. UK (provider, payment_reference) in PREMIUM_PAYMENTS.",
        "7. JOB_REQUIRED_SKILLS uses composite PK (job_id, skill_id).",
        "8. USERS has 1:N with PROJECTS and CERTIFICATIONS.",
    ]
    ry = panel_y + 60
    for line in rules:
        draw.text((panel_x + 18, ry), line, font=rule_font, fill=(31, 54, 21))
        ry += 54

    # Notation legend
    # Keep legend below upper-right entities so it does not cover JOB_REQUIRED_SKILLS.
    legend_x, legend_y, legend_w, legend_h = 2140, 860, 1000, 170
    draw.rounded_rectangle(
        (legend_x, legend_y, legend_x + legend_w, legend_y + legend_h),
        radius=14,
        fill=(255, 247, 236),
        outline=(170, 122, 66),
        width=3,
    )
    draw.text((legend_x + 16, legend_y + 12), "Notation", font=rule_title_font, fill=(126, 74, 15))
    draw.text((legend_x + 18, legend_y + 62), "PK = Primary Key, FK = Foreign Key, UK = Unique Key", font=rule_font, fill=(75, 45, 8))
    draw.text((legend_x + 18, legend_y + 104), "Cardinality labels near lines: 1 and N", font=rule_font, fill=(75, 45, 8))

    out_path = Path("ER_DIAGRAM.png")
    image.save(out_path)
    print(f"Generated: {out_path.resolve()}")


if __name__ == "__main__":
    main()
