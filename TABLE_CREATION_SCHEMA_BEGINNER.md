# Beginner-Friendly Table Creation Schema

This file gives a simpler version of the current backend table schema.

For readability, the optional MySQL storage line such as
`ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci`
has been removed.

Goal:
- keep the same main table structure the app currently expects
- avoid disturbing existing data by using `CREATE TABLE IF NOT EXISTS`
- keep the SQL easy to read for beginners

Important:
- These queries create tables only if they do not already exist.
- They do not delete old values.
- They also do not change an already existing table structure.
- If a table already exists and has the wrong columns, you would need `ALTER TABLE`, not `CREATE TABLE`.

The schema below follows the current backend initialization logic in `main.py`.

## 1. `users`

Stores all users of the system: students, recruiters, and admins.

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    subscription_type VARCHAR(20) NOT NULL DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL,
    INDEX idx_users_role (role),
    INDEX idx_users_subscription_type (subscription_type)
);
```

## 2. `skills`

Stores the list of skills such as Python, MySQL, React, and so on.

```sql
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_skills_name (skill_name)
);
```

## 3. `user_skills`

Connects a user with a skill and stores the user's proficiency level.

```sql
CREATE TABLE IF NOT EXISTS user_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level VARCHAR(20) NOT NULL DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_user_skill (user_id, skill_id),
    INDEX idx_user_skills_user_id (user_id),
    INDEX idx_user_skills_skill_id (skill_id),
    INDEX idx_user_skills_proficiency (proficiency_level),
    CONSTRAINT fk_user_skills_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_skills_skill
        FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
```

## 4. `jobs`

Stores jobs posted by recruiters.

```sql
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
    updated_at TIMESTAMP NULL DEFAULT NULL,
    INDEX idx_jobs_recruiter_id (recruiter_id),
    INDEX idx_jobs_created_at (created_at),
    INDEX idx_jobs_is_active (is_active),
    CONSTRAINT fk_jobs_recruiter
        FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 5. `job_required_skills`

Connects jobs with the skills required for them.

```sql
CREATE TABLE IF NOT EXISTS job_required_skills (
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id, skill_id),
    INDEX idx_job_required_skills_skill_id (skill_id),
    CONSTRAINT fk_job_required_skills_job
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    CONSTRAINT fk_job_required_skills_skill
        FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
```

## 6. `job_applications`

Stores applications submitted by students for jobs.

```sql
CREATE TABLE IF NOT EXISTS job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    student_id INT NOT NULL,
    cover_letter TEXT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'applied',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL,
    UNIQUE KEY uniq_job_student (job_id, student_id),
    INDEX idx_job_applications_job_id (job_id),
    INDEX idx_job_applications_student_id (student_id),
    INDEX idx_job_applications_status (status),
    CONSTRAINT fk_job_applications_job
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    CONSTRAINT fk_job_applications_student
        FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 7. `ai_resumes`

Stores resumes generated for users.

```sql
CREATE TABLE IF NOT EXISTS ai_resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_role VARCHAR(150) NOT NULL,
    resume_text LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ai_resumes_user_id (user_id),
    INDEX idx_ai_resumes_created_at (created_at),
    CONSTRAINT fk_ai_resumes_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 8. `premium_payments`

Stores premium upgrade payment records.

```sql
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
    UNIQUE KEY uniq_provider_reference (provider, payment_reference),
    INDEX idx_premium_payments_user_id (user_id),
    INDEX idx_premium_payments_created_at (created_at),
    CONSTRAINT fk_premium_payments_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Simple Notes

- `PRIMARY KEY` means the main unique ID of the table.
- `FOREIGN KEY` means one table is connected to another table.
- `UNIQUE` means duplicate values are not allowed for that column or pair of columns.
- `NOT NULL` means the field must have a value.
- `DEFAULT` means MySQL uses that value automatically if you do not give one.
- `ON DELETE CASCADE` means if the parent row is deleted, related child rows are also deleted.

## Small Note

Because that storage line is removed here, MySQL will use the database or server default engine and character set.
