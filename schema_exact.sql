-- SkillConnect authoritative schema
-- Import into a fresh MySQL 8+ database, for example: DBMS_project
-- This schema matches the current application structure and includes
-- the real-time messaging table used by the app.

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'student',
  `subscription_type` VARCHAR(20) NOT NULL DEFAULT 'free',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_users_email` (`email`),
  KEY `idx_users_role` (`role`),
  KEY `idx_users_subscription_type` (`subscription_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `skills` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `skill_name` VARCHAR(100) NOT NULL,
  `category` VARCHAR(100) DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_skills_name` (`skill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_skills` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  `proficiency_level` VARCHAR(20) NOT NULL DEFAULT 'beginner',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_skill` (`user_id`, `skill_id`),
  KEY `idx_user_skills_user_id` (`user_id`),
  KEY `idx_user_skills_skill_id` (`skill_id`),
  KEY `idx_user_skills_proficiency` (`proficiency_level`),
  CONSTRAINT `fk_user_skills_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_skills_skill`
    FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `jobs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `recruiter_id` INT NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `company_name` VARCHAR(150) NOT NULL,
  `location` VARCHAR(120) NOT NULL DEFAULT 'Remote',
  `employment_type` VARCHAR(60) NOT NULL DEFAULT 'full-time',
  `description` TEXT NOT NULL,
  `required_skills` TEXT DEFAULT NULL,
  `salary_range` VARCHAR(80) DEFAULT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_jobs_recruiter_id` (`recruiter_id`),
  KEY `idx_jobs_created_at` (`created_at`),
  KEY `idx_jobs_is_active` (`is_active`),
  CONSTRAINT `fk_jobs_recruiter`
    FOREIGN KEY (`recruiter_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_required_skills` (
  `job_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`job_id`, `skill_id`),
  KEY `idx_job_required_skills_skill_id` (`skill_id`),
  CONSTRAINT `fk_job_required_skills_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_job_required_skills_skill`
    FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_applications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `job_id` INT NOT NULL,
  `student_id` INT NOT NULL,
  `cover_letter` TEXT DEFAULT NULL,
  `status` VARCHAR(30) NOT NULL DEFAULT 'applied',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_job_student` (`job_id`, `student_id`),
  KEY `idx_job_applications_job_id` (`job_id`),
  KEY `idx_job_applications_student_id` (`student_id`),
  KEY `idx_job_applications_status` (`status`),
  CONSTRAINT `fk_job_applications_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_job_applications_student`
    FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_application_messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `application_id` INT NOT NULL,
  `sender_id` INT NOT NULL,
  `recipient_id` INT NOT NULL,
  `message_text` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `read_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_jam_application_id` (`application_id`),
  KEY `idx_jam_sender_id` (`sender_id`),
  KEY `idx_jam_recipient_id` (`recipient_id`),
  KEY `idx_jam_created_at` (`created_at`),
  KEY `idx_jam_recipient_read` (`recipient_id`, `read_at`),
  CONSTRAINT `fk_jam_application`
    FOREIGN KEY (`application_id`) REFERENCES `job_applications` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jam_sender`
    FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jam_recipient`
    FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ai_resumes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `target_role` VARCHAR(150) NOT NULL,
  `resume_text` LONGTEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ai_resumes_user_id` (`user_id`),
  KEY `idx_ai_resumes_created_at` (`created_at`),
  CONSTRAINT `fk_ai_resumes_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `premium_payments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `provider` VARCHAR(50) NOT NULL,
  `payment_reference` VARCHAR(150) NOT NULL,
  `payment_signature` VARCHAR(256) NOT NULL,
  `amount_cents` INT DEFAULT NULL,
  `currency` VARCHAR(10) DEFAULT NULL,
  `status` VARCHAR(30) NOT NULL DEFAULT 'verified',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `verified_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_provider_reference` (`provider`, `payment_reference`),
  KEY `idx_premium_payments_user_id` (`user_id`),
  KEY `idx_premium_payments_created_at` (`created_at`),
  CONSTRAINT `fk_premium_payments_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional extension tables used by the project data files.
CREATE TABLE IF NOT EXISTS `projects` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT DEFAULT NULL,
  `tech_stack` VARCHAR(255) DEFAULT NULL,
  `project_link` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_projects_user_id` (`user_id`),
  KEY `idx_projects_created_at` (`created_at`),
  CONSTRAINT `fk_projects_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `certifications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `certificate_name` VARCHAR(255) NOT NULL,
  `organization` VARCHAR(255) DEFAULT NULL,
  `issue_date` DATE DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_certifications_user_id` (`user_id`),
  CONSTRAINT `fk_certifications_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
