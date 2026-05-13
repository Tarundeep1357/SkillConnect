# ER Diagram (SkillConnect DB)

```mermaid
erDiagram
    USERS {
        INT id PK
        VARCHAR(100) name
        VARCHAR(255) email UK
        VARCHAR(255) password
        VARCHAR(20) role
        VARCHAR(20) subscription_type
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    SKILLS {
        INT id PK
        VARCHAR(100) skill_name UK
        VARCHAR(100) category
        TIMESTAMP created_at
    }

    USER_SKILLS {
        INT id PK
        INT user_id FK
        INT skill_id FK
        VARCHAR(20) proficiency_level
        TIMESTAMP created_at
    }

    JOBS {
        INT id PK
        INT recruiter_id FK
        VARCHAR(150) title
        VARCHAR(150) company_name
        VARCHAR(120) location
        VARCHAR(60) employment_type
        TEXT description
        TEXT required_skills
        VARCHAR(80) salary_range
        TINYINT is_active
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    JOB_REQUIRED_SKILLS {
        INT job_id PK
        INT skill_id PK
        TIMESTAMP created_at
    }

    JOB_APPLICATIONS {
        INT id PK
        INT job_id FK
        INT student_id FK
        TEXT cover_letter
        VARCHAR(30) status
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    AI_RESUMES {
        INT id PK
        INT user_id FK
        VARCHAR(150) target_role
        LONGTEXT resume_text
        TIMESTAMP created_at
    }

    PROJECTS {
        INT id PK
        INT user_id FK
        VARCHAR(200) title
        TEXT description
        VARCHAR(255) tech_stack
        VARCHAR(255) project_link
        TIMESTAMP created_at
    }

    CERTIFICATIONS {
        INT id PK
        INT user_id FK
        VARCHAR(255) certificate_name
        VARCHAR(255) organization
        DATE issue_date
    }

    PREMIUM_PAYMENTS {
        INT id PK
        INT user_id FK
        VARCHAR(50) provider
        VARCHAR(150) payment_reference
        VARCHAR(256) payment_signature
        INT amount_cents
        VARCHAR(10) currency
        VARCHAR(30) status
        TIMESTAMP created_at
        TIMESTAMP verified_at
    }

    USERS ||--o{ USER_SKILLS : has
    SKILLS ||--o{ USER_SKILLS : appears_in

    USERS ||--o{ JOBS : posts

    JOBS ||--o{ JOB_REQUIRED_SKILLS : requires
    SKILLS ||--o{ JOB_REQUIRED_SKILLS : mapped_to

    JOBS ||--o{ JOB_APPLICATIONS : receives
    USERS ||--o{ JOB_APPLICATIONS : submits

    USERS ||--o{ AI_RESUMES : owns
    USERS ||--o{ PROJECTS : builds
    USERS ||--o{ CERTIFICATIONS : earns
    USERS ||--o{ PREMIUM_PAYMENTS : makes
```

## Relationship and Integrity Rules

1. `users` to `jobs` is `1:N` via `jobs.recruiter_id -> users.id` (`ON DELETE CASCADE`).
2. `users` to `skills` is `M:N` via associative table `user_skills`.
3. `jobs` to `skills` is `M:N` via associative table `job_required_skills`.
4. `jobs` to `job_applications` is `1:N` via `job_applications.job_id -> jobs.id` (`ON DELETE CASCADE`).
5. `users` to `job_applications` is `1:N` via `job_applications.student_id -> users.id` (`ON DELETE CASCADE`).
6. `users` to `ai_resumes` is `1:N` via `ai_resumes.user_id -> users.id` (`ON DELETE CASCADE`).
7. `users` to `projects` is `1:N` via `projects.user_id -> users.id` (`ON DELETE CASCADE`).
8. `users` to `certifications` is `1:N` via `certifications.user_id -> users.id` (`ON DELETE CASCADE`).
9. `users` to `premium_payments` is `1:N` via `premium_payments.user_id -> users.id` (`ON DELETE CASCADE`).

## Key Rules

1. Primary keys: all base entities use single-column PK `id`, except `job_required_skills` which uses composite PK `(job_id, skill_id)`.
2. Unique constraints:
   - `users.email`
   - `skills.skill_name`
   - `user_skills (user_id, skill_id)` (no duplicate skill per user)
   - `job_applications (job_id, student_id)` (one application per student per job)
   - `premium_payments (provider, payment_reference)` (no duplicate payment reference per provider)
3. Mandatory foreign keys (`NOT NULL`) enforce total participation on child side in core relationship tables; note `projects.user_id` is nullable in the live schema.

## Attribute and Domain Rules

1. Default values:
   - `users.role = 'student'`
   - `users.subscription_type = 'free'`
   - `user_skills.proficiency_level = 'beginner'`
   - `jobs.location = 'Remote'`
   - `jobs.employment_type = 'full-time'`
   - `jobs.is_active = 1`
   - `job_applications.status = 'applied'`
   - `premium_payments.status = 'verified'`
2. Application-level allowed values:
   - `role in {student, recruiter, admin}` (registration allows `{student, recruiter}`)
   - `subscription_type in {free, premium}`
   - `proficiency_level in {beginner, intermediate, advanced, expert}`
   - `job_applications.status in {applied, shortlisted, interview, rejected, hired}`
   - `jobs.employment_type in {full-time, part-time, internship, contract}`
3. Optional attributes (`NULL` allowed):
    - `skills.category`
    - `jobs.required_skills` (legacy denormalized storage)
    - `jobs.salary_range`
    - `job_applications.cover_letter`
    - `projects.user_id`, `projects.description`, `projects.tech_stack`, `projects.project_link`
    - `certifications.organization`, `certifications.issue_date`
    - `premium_payments.amount_cents`, `premium_payments.currency`, `premium_payments.verified_at`
    - `users.updated_at`, `jobs.updated_at`, `job_applications.updated_at`
