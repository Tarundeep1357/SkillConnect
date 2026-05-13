# Exact Live MySQL Schema

This file contains the exact `SHOW CREATE TABLE` output from the current live database.

Important:
- This matches the database as it exists right now.
- The `AUTO_INCREMENT=...` values are the current counters and may change after new inserts.
- This version is for exact matching, not simplified learning.

## 1. `users`

```sql
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('student','recruiter','admin') DEFAULT 'student',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `subscription_type` varchar(20) DEFAULT 'free',
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_users_role` (`role`),
  KEY `idx_users_subscription_type` (`subscription_type`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
```

## 2. `skills`

```sql
CREATE TABLE `skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `skill_name` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `skill_name` (`skill_name`),
  UNIQUE KEY `uniq_skills_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1;
```

## 3. `user_skills`

```sql
CREATE TABLE `user_skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `skill_id` int(11) DEFAULT NULL,
  `proficiency_level` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_skills_user_id` (`user_id`),
  KEY `idx_user_skills_skill_id` (`skill_id`),
  KEY `idx_user_skills_proficiency` (`proficiency_level`),
  CONSTRAINT `fk_user_skills_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_skills_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_skills_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
```

## 4. `jobs`

```sql
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recruiter_id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `location` varchar(120) NOT NULL DEFAULT 'Remote',
  `employment_type` varchar(60) NOT NULL DEFAULT 'full-time',
  `description` text NOT NULL,
  `required_skills` text,
  `salary_range` varchar(80) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_jobs_recruiter_id` (`recruiter_id`),
  KEY `idx_jobs_created_at` (`created_at`),
  KEY `idx_jobs_is_active` (`is_active`),
  CONSTRAINT `fk_jobs_recruiter` FOREIGN KEY (`recruiter_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
```

## 5. `job_required_skills`

```sql
CREATE TABLE `job_required_skills` (
  `job_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`job_id`,`skill_id`),
  KEY `fk_job_required_skills_skill` (`skill_id`),
  CONSTRAINT `fk_job_required_skills_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_job_required_skills_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## 6. `job_applications`

```sql
CREATE TABLE `job_applications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `cover_letter` text,
  `status` varchar(30) NOT NULL DEFAULT 'applied',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_job_student` (`job_id`,`student_id`),
  KEY `idx_job_app_student` (`student_id`),
  KEY `idx_job_app_job` (`job_id`),
  KEY `idx_job_applications_job_id` (`job_id`),
  KEY `idx_job_applications_student_id` (`student_id`),
  KEY `idx_job_applications_status` (`status`),
  CONSTRAINT `fk_job_applications_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_job_applications_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
```

## 7. `ai_resumes`

```sql
CREATE TABLE `ai_resumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `target_role` varchar(150) NOT NULL,
  `resume_text` longtext NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ai_resumes_user_id` (`user_id`),
  KEY `idx_ai_resumes_created_at` (`created_at`),
  CONSTRAINT `fk_ai_resumes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## 8. `premium_payments`

```sql
CREATE TABLE `premium_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(50) NOT NULL,
  `payment_reference` varchar(150) NOT NULL,
  `payment_signature` varchar(256) NOT NULL,
  `amount_cents` int(11) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'verified',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `verified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_provider_reference` (`provider`,`payment_reference`),
  KEY `idx_premium_payments_user_id` (`user_id`),
  KEY `idx_premium_payments_created_at` (`created_at`),
  CONSTRAINT `fk_premium_payments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## 9. `projects`

```sql
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `description` text,
  `tech_stack` varchar(255) DEFAULT NULL,
  `project_link` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## 10. `certifications`

```sql
CREATE TABLE `certifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `certificate_name` varchar(255) NOT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `certifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
