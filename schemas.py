from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: Literal["student", "recruiter"] = "student"


class SkillCreate(BaseModel):
    skill_name: str = Field(min_length=1, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    proficiency_level: Literal["beginner", "intermediate", "advanced", "expert"] = "beginner"


class ResumeGenerateRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    target_role: str = Field(min_length=2, max_length=120)
    years_experience: int = Field(ge=0, le=50)
    skills: list[str] = Field(default_factory=list, max_length=30)
    education: str = Field(min_length=2, max_length=300)
    achievements: list[str] = Field(default_factory=list, max_length=20)


class ResumeGenerateResponse(BaseModel):
    resume_text: str
    generated_at: str


class MeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["student", "recruiter", "admin"]
    subscription_type: str


class JobCreateRequest(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    company_name: str = Field(min_length=2, max_length=150)
    location: str = Field(default="Remote", min_length=2, max_length=120)
    employment_type: Literal["full-time", "part-time", "internship", "contract"] = "full-time"
    description: str = Field(min_length=20, max_length=3000)
    required_skills: list[str] = Field(default_factory=list, max_length=30)
    salary_range: str | None = Field(default=None, max_length=80)


class JobApplyRequest(BaseModel):
    cover_letter: str | None = Field(default=None, max_length=2000)


class PremiumUpgradeRequest(BaseModel):
    provider: str = Field(min_length=2, max_length=50)
    payment_reference: str = Field(min_length=3, max_length=150)
    payment_signature: str = Field(min_length=20, max_length=256)
    amount_cents: int | None = Field(default=None, ge=1, le=1_000_000_000)
    currency: str | None = Field(default=None, min_length=3, max_length=10)


class DevSignatureRequest(BaseModel):
    provider: str = Field(min_length=2, max_length=50)
    payment_reference: str = Field(min_length=3, max_length=150)


class JobApplicationStatusUpdateRequest(BaseModel):
    status: Literal["applied", "shortlisted", "interview", "rejected", "hired"]


class MessageCreateRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
