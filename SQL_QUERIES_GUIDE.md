# Easy SQL Queries for SkillConnect Project

This file contains simple SQL queries for your college project.

It is based on the live tables in `main.py`:
- `users`
- `skills`
- `user_skills`
- `jobs`
- `job_required_skills`
- `job_applications`
- `ai_resumes`
- `premium_payments`

This guide covers:
- `INSERT`
- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `UPDATE`
- `DELETE`
- aggregate functions
- `GROUP BY`
- `HAVING`
- `JOIN`
- subqueries

Not included:
- triggers
- stored procedures
- views
- transactions
- window functions
- other advanced SQL topics

## 1. Check Tables

```sql
SHOW TABLES;
```

```sql
DESC users;
DESC skills;
DESC user_skills;
DESC jobs;
DESC job_required_skills;
DESC job_applications;
DESC ai_resumes;
DESC premium_payments;
```

## 2. Insert 20 Rows for Required Tables

Run in this order:
- `users`
- `skills`
- `user_skills`
- `jobs`

Note:
- All sample users below use password `pass123`
- The password is already stored as a bcrypt hash, so it matches your project style
- The `users` and `skills` inserts below skip rows that already exist
- If `Python` or any email already exists, MySQL will not insert that same row again

### Insert 20 rows into `users`

```sql
INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Aarav Sharma', 'aarav.sharma@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'recruiter', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'aarav.sharma@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Riya Verma', 'riya.verma@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'recruiter', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'riya.verma@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Karan Mehta', 'karan.mehta@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'recruiter', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'karan.mehta@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Neha Kapoor', 'neha.kapoor@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'recruiter', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'neha.kapoor@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Vikram Nair', 'vikram.nair@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'recruiter', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'vikram.nair@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Priya Singh', 'priya.singh@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'priya.singh@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Rahul Gupta', 'rahul.gupta@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'rahul.gupta@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Ananya Iyer', 'ananya.iyer@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'ananya.iyer@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Aditya Rao', 'aditya.rao@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'aditya.rao@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Sneha Patil', 'sneha.patil@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'sneha.patil@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Rohit Jain', 'rohit.jain@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'rohit.jain@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Pooja Reddy', 'pooja.reddy@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'pooja.reddy@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Arjun Malhotra', 'arjun.malhotra@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'arjun.malhotra@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Kavya Menon', 'kavya.menon@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'kavya.menon@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Yash Thakur', 'yash.thakur@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'yash.thakur@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Nisha Bansal', 'nisha.bansal@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'premium'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'nisha.bansal@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Siddharth Kulkarni', 'siddharth.kulkarni@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'siddharth.kulkarni@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Meera Joshi', 'meera.joshi@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'meera.joshi@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Devansh Choudhary', 'devansh.choudhary@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'devansh.choudhary@skillconnect.in');

INSERT INTO users (name, email, password, role, subscription_type)
SELECT 'Ishita Desai', 'ishita.desai@skillconnect.in', '$2b$12$KlijIAhEDQKaanLSw02Yk.fx1xENfAHQquZhE8i7xIByDSahlMPim', 'student', 'free'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'ishita.desai@skillconnect.in');
```

### Insert 20 rows into `skills`

```sql
INSERT INTO skills (skill_name, category)
SELECT 'Python', 'Programming'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Python');

INSERT INTO skills (skill_name, category)
SELECT 'MySQL', 'Database'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'MySQL');

INSERT INTO skills (skill_name, category)
SELECT 'Java', 'Programming'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Java');

INSERT INTO skills (skill_name, category)
SELECT 'C', 'Programming'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'C');

INSERT INTO skills (skill_name, category)
SELECT 'C++', 'Programming'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'C++');

INSERT INTO skills (skill_name, category)
SELECT 'JavaScript', 'Web'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'JavaScript');

INSERT INTO skills (skill_name, category)
SELECT 'HTML', 'Web'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'HTML');

INSERT INTO skills (skill_name, category)
SELECT 'CSS', 'Web'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'CSS');

INSERT INTO skills (skill_name, category)
SELECT 'React', 'Web'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'React');

INSERT INTO skills (skill_name, category)
SELECT 'Node.js', 'Backend'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Node.js');

INSERT INTO skills (skill_name, category)
SELECT 'Django', 'Backend'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Django');

INSERT INTO skills (skill_name, category)
SELECT 'Flask', 'Backend'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Flask');

INSERT INTO skills (skill_name, category)
SELECT 'MongoDB', 'Database'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'MongoDB');

INSERT INTO skills (skill_name, category)
SELECT 'SQL', 'Database'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'SQL');

INSERT INTO skills (skill_name, category)
SELECT 'Git', 'Tools'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Git');

INSERT INTO skills (skill_name, category)
SELECT 'Excel', 'Analytics'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Excel');

INSERT INTO skills (skill_name, category)
SELECT 'Power BI', 'Analytics'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Power BI');

INSERT INTO skills (skill_name, category)
SELECT 'Machine Learning', 'AI'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Machine Learning');

INSERT INTO skills (skill_name, category)
SELECT 'Data Analysis', 'Analytics'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Data Analysis');

INSERT INTO skills (skill_name, category)
SELECT 'DBMS', 'Database'
WHERE NOT EXISTS (SELECT 1 FROM skills WHERE skill_name = 'DBMS');
```

### Insert 20 rows into `user_skills`

```sql
INSERT IGNORE INTO user_skills (user_id, skill_id, proficiency_level)
VALUES
((SELECT id FROM users WHERE email = 'priya.singh@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Python'), 'advanced'),
((SELECT id FROM users WHERE email = 'priya.singh@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'MySQL'), 'intermediate'),
((SELECT id FROM users WHERE email = 'rahul.gupta@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Java'), 'intermediate'),
((SELECT id FROM users WHERE email = 'rahul.gupta@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Git'), 'advanced'),
((SELECT id FROM users WHERE email = 'ananya.iyer@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'HTML'), 'advanced'),
((SELECT id FROM users WHERE email = 'ananya.iyer@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'DBMS'), 'expert'),
((SELECT id FROM users WHERE email = 'aditya.rao@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'CSS'), 'intermediate'),
((SELECT id FROM users WHERE email = 'aditya.rao@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'C++'), 'intermediate'),
((SELECT id FROM users WHERE email = 'sneha.patil@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'JavaScript'), 'advanced'),
((SELECT id FROM users WHERE email = 'sneha.patil@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'C'), 'beginner'),
((SELECT id FROM users WHERE email = 'rohit.jain@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'React'), 'intermediate'),
((SELECT id FROM users WHERE email = 'pooja.reddy@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Node.js'), 'beginner'),
((SELECT id FROM users WHERE email = 'arjun.malhotra@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Django'), 'advanced'),
((SELECT id FROM users WHERE email = 'kavya.menon@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Flask'), 'intermediate'),
((SELECT id FROM users WHERE email = 'yash.thakur@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'MongoDB'), 'beginner'),
((SELECT id FROM users WHERE email = 'nisha.bansal@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'SQL'), 'advanced'),
((SELECT id FROM users WHERE email = 'siddharth.kulkarni@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Excel'), 'intermediate'),
((SELECT id FROM users WHERE email = 'meera.joshi@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Power BI'), 'advanced'),
((SELECT id FROM users WHERE email = 'devansh.choudhary@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Machine Learning'), 'beginner'),
((SELECT id FROM users WHERE email = 'ishita.desai@skillconnect.in'), (SELECT id FROM skills WHERE skill_name = 'Data Analysis'), 'advanced');
```

### Insert 20 rows into `jobs`

```sql
INSERT INTO jobs (
    recruiter_id,
    title,
    company_name,
    location,
    employment_type,
    description,
    required_skills,
    salary_range,
    is_active
)
VALUES
((SELECT id FROM users WHERE email = 'aarav.sharma@skillconnect.in'), 'Backend Developer Intern', 'Infosys', 'Bengaluru', 'internship', 'Build backend APIs and support database operations for web products.', 'Python, MySQL', '250000-400000', 1),
((SELECT id FROM users WHERE email = 'aarav.sharma@skillconnect.in'), 'API Developer Intern', 'Razorpay', 'Bengaluru', 'internship', 'Work on REST APIs and backend integration tasks for payment systems.', 'Python, Flask', '300000-450000', 1),
((SELECT id FROM users WHERE email = 'aarav.sharma@skillconnect.in'), 'SQL Developer Intern', 'Cognizant', 'Chennai', 'internship', 'Write SQL queries and support reporting and database maintenance work.', 'SQL, MySQL', '240000-380000', 1),
((SELECT id FROM users WHERE email = 'aarav.sharma@skillconnect.in'), 'Cloud Support Intern', 'Wipro', 'Hyderabad', 'internship', 'Assist the cloud team with support tickets and system monitoring tasks.', 'Git, SQL', '220000-360000', 1),
((SELECT id FROM users WHERE email = 'riya.verma@skillconnect.in'), 'Frontend Developer Intern', 'TCS', 'Pune', 'internship', 'Develop user interface pages and improve frontend responsiveness.', 'HTML, CSS, JavaScript', '240000-350000', 1),
((SELECT id FROM users WHERE email = 'riya.verma@skillconnect.in'), 'UI Developer Intern', 'Zensar', 'Pune', 'internship', 'Create clean user interfaces and update reusable frontend components.', 'React, CSS', '260000-390000', 1),
((SELECT id FROM users WHERE email = 'riya.verma@skillconnect.in'), 'React Developer Intern', 'Freshworks', 'Chennai', 'internship', 'Build React pages and connect them with backend APIs.', 'React, JavaScript', '280000-420000', 1),
((SELECT id FROM users WHERE email = 'riya.verma@skillconnect.in'), 'Web Developer Intern', 'Mindtree', 'Bengaluru', 'internship', 'Work on website features, forms, layouts, and browser compatibility.', 'HTML, CSS', '230000-340000', 1),
((SELECT id FROM users WHERE email = 'karan.mehta@skillconnect.in'), 'Data Analyst Intern', 'Wipro', 'Hyderabad', 'internship', 'Prepare reports, clean data, and support business analysis tasks.', 'SQL, Data Analysis', '250000-400000', 1),
((SELECT id FROM users WHERE email = 'karan.mehta@skillconnect.in'), 'Business Analyst Intern', 'Paytm', 'Noida', 'internship', 'Analyze business data and help teams prepare useful dashboards.', 'Excel, Data Analysis', '260000-410000', 1),
((SELECT id FROM users WHERE email = 'karan.mehta@skillconnect.in'), 'Power BI Intern', 'LTIMindtree', 'Mumbai', 'internship', 'Create Power BI dashboards and support data reporting tasks.', 'Power BI, Excel', '250000-390000', 1),
((SELECT id FROM users WHERE email = 'karan.mehta@skillconnect.in'), 'Excel Reporting Intern', 'HCLTech', 'Noida', 'internship', 'Work on MIS reports and organize business data in Excel sheets.', 'Excel, SQL', '220000-330000', 1),
((SELECT id FROM users WHERE email = 'neha.kapoor@skillconnect.in'), 'Java Developer Intern', 'Tech Mahindra', 'Mumbai', 'internship', 'Support Java application modules and fix simple backend issues.', 'Java, Git', '260000-420000', 1),
((SELECT id FROM users WHERE email = 'neha.kapoor@skillconnect.in'), 'Software Engineer Intern', 'Infosys', 'Mysuru', 'internship', 'Assist in coding, debugging, and testing software features.', 'Java, SQL', '250000-400000', 1),
((SELECT id FROM users WHERE email = 'neha.kapoor@skillconnect.in'), 'C++ Developer Intern', 'Mphasis', 'Pune', 'internship', 'Work on basic C++ modules and debugging of existing code.', 'C++, Git', '240000-370000', 1),
((SELECT id FROM users WHERE email = 'neha.kapoor@skillconnect.in'), 'Testing Intern', 'TCS', 'Kolkata', 'internship', 'Perform manual testing and prepare defect reports for applications.', 'Java, DBMS', '220000-340000', 1),
((SELECT id FROM users WHERE email = 'vikram.nair@skillconnect.in'), 'Python Developer Intern', 'Zoho', 'Chennai', 'internship', 'Develop small backend features using Python and database queries.', 'Python, MySQL', '280000-430000', 1),
((SELECT id FROM users WHERE email = 'vikram.nair@skillconnect.in'), 'Django Developer Intern', 'Flipkart', 'Bengaluru', 'internship', 'Build Django modules and improve API and admin features.', 'Python, Django', '300000-450000', 1),
((SELECT id FROM users WHERE email = 'vikram.nair@skillconnect.in'), 'Machine Learning Intern', 'Reliance Jio', 'Mumbai', 'internship', 'Support basic machine learning models and data preparation tasks.', 'Machine Learning, Python', '320000-480000', 1),
((SELECT id FROM users WHERE email = 'vikram.nair@skillconnect.in'), 'Database Intern', 'ICICI Bank', 'Mumbai', 'internship', 'Help in database support, SQL work, and data handling tasks.', 'MySQL, DBMS', '240000-380000', 1);
```

### Insert into `job_required_skills`

```sql
INSERT IGNORE INTO job_required_skills (job_id, skill_id)
VALUES
(
    (SELECT id FROM jobs WHERE title = 'Backend Developer Intern' AND company_name = 'Infosys' LIMIT 1),
    (SELECT id FROM skills WHERE skill_name = 'Python' LIMIT 1)
),
(
    (SELECT id FROM jobs WHERE title = 'Backend Developer Intern' AND company_name = 'Infosys' LIMIT 1),
    (SELECT id FROM skills WHERE skill_name = 'MySQL' LIMIT 1)
);
```

### Insert into `job_applications`

```sql
INSERT IGNORE INTO job_applications (job_id, student_id, cover_letter, status)
VALUES
(
    (SELECT id FROM jobs WHERE title = 'Backend Developer Intern' AND company_name = 'Infosys' LIMIT 1),
    (SELECT id FROM users WHERE email = 'priya.singh@skillconnect.in' LIMIT 1),
    'I am interested in this internship and have worked on Python projects.',
    'applied'
);
```

### Insert into `ai_resumes`

```sql
INSERT INTO ai_resumes (user_id, target_role, resume_text)
VALUES
(
    (SELECT id FROM users WHERE email = 'priya.singh@skillconnect.in' LIMIT 1),
    'Backend Developer',
    'Priya Singh knows Python, MySQL and basic backend development.'
);
```

### Insert into `premium_payments`

```sql
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
VALUES
(
    (SELECT id FROM users WHERE email = 'priya.singh@skillconnect.in' LIMIT 1),
    'razorpay',
    'pay_001',
    'signature_001',
    99900,
    'INR',
    'verified',
    NOW()
);
```

## 3. Simple SELECT Queries

```sql
SELECT * FROM users;
SELECT * FROM skills;
SELECT * FROM user_skills;
SELECT * FROM jobs;
SELECT * FROM job_required_skills;
SELECT * FROM job_applications;
SELECT * FROM ai_resumes;
SELECT * FROM premium_payments;
```

```sql
SELECT name, email, role FROM users;
```

```sql
SELECT title, company_name, location FROM jobs;
```

## 4. WHERE Clause

```sql
SELECT * FROM users
WHERE role = 'student';
```

```sql
SELECT * FROM jobs
WHERE location = 'Bengaluru';
```

```sql
SELECT * FROM premium_payments
WHERE status = 'verified';
```

## 5. AND, OR, IN, LIKE

```sql
SELECT * FROM users
WHERE role = 'student' AND subscription_type = 'free';
```

```sql
SELECT * FROM jobs
WHERE location = 'Bengaluru' OR location = 'Remote';
```

```sql
SELECT * FROM job_applications
WHERE status IN ('applied', 'shortlisted');
```

```sql
SELECT * FROM skills
WHERE skill_name LIKE 'P%';
```

## 6. ORDER BY and LIMIT

```sql
SELECT * FROM jobs
ORDER BY created_at DESC;
```

```sql
SELECT * FROM skills
ORDER BY skill_name ASC;
```

```sql
SELECT * FROM ai_resumes
ORDER BY created_at DESC
LIMIT 3;
```

## 7. DISTINCT

```sql
SELECT DISTINCT role
FROM users;
```

```sql
SELECT DISTINCT category
FROM skills;
```

## 8. Aggregate Functions

### Count

```sql
SELECT COUNT(*) AS total_users
FROM users;
```

```sql
SELECT COUNT(*) AS total_jobs
FROM jobs;
```

### Maximum

```sql
SELECT MAX(amount_cents) AS highest_payment
FROM premium_payments;
```

### Minimum

```sql
SELECT MIN(amount_cents) AS lowest_payment
FROM premium_payments;
```

### Average

```sql
SELECT AVG(amount_cents) AS average_payment
FROM premium_payments;
```

### Sum

```sql
SELECT SUM(amount_cents) AS total_payment
FROM premium_payments;
```

## 9. GROUP BY

```sql
SELECT role, COUNT(*) AS total_users
FROM users
GROUP BY role;
```

```sql
SELECT status, COUNT(*) AS total_applications
FROM job_applications
GROUP BY status;
```

```sql
SELECT category, COUNT(*) AS total_skills
FROM skills
GROUP BY category;
```

## 10. HAVING

```sql
SELECT role, COUNT(*) AS total_users
FROM users
GROUP BY role
HAVING COUNT(*) >= 1;
```

```sql
SELECT status, COUNT(*) AS total_applications
FROM job_applications
GROUP BY status
HAVING COUNT(*) >= 1;
```

## 11. UPDATE Queries

```sql
UPDATE users
SET subscription_type = 'premium'
WHERE email = 'priya.singh@skillconnect.in';
```

```sql
UPDATE jobs
SET location = 'Remote'
WHERE title = 'Backend Developer Intern'
  AND company_name = 'Infosys';
```

```sql
UPDATE job_applications
SET status = 'shortlisted'
WHERE job_id = (
    SELECT id
    FROM jobs
    WHERE title = 'Backend Developer Intern'
      AND company_name = 'Infosys'
    LIMIT 1
)
AND student_id = (
    SELECT id
    FROM users
    WHERE email = 'priya.singh@skillconnect.in'
    LIMIT 1
);
```

## 12. DELETE Queries

```sql
DELETE FROM ai_resumes
WHERE user_id = (
    SELECT id
    FROM users
    WHERE email = 'priya.singh@skillconnect.in'
    LIMIT 1
)
AND target_role = 'Backend Developer';
```

```sql
DELETE FROM job_applications
WHERE job_id = (
    SELECT id
    FROM jobs
    WHERE title = 'Backend Developer Intern'
      AND company_name = 'Infosys'
    LIMIT 1
)
AND student_id = (
    SELECT id
    FROM users
    WHERE email = 'priya.singh@skillconnect.in'
    LIMIT 1
);
```

```sql
DELETE FROM user_skills
WHERE user_id = (
    SELECT id
    FROM users
    WHERE email = 'ishita.desai@skillconnect.in'
    LIMIT 1
)
AND skill_id = (
    SELECT id
    FROM skills
    WHERE skill_name = 'Data Analysis'
    LIMIT 1
);
```

## 13. JOIN Queries

### Inner Join: users and their skills

```sql
SELECT
    users.name,
    skills.skill_name,
    user_skills.proficiency_level
FROM user_skills
INNER JOIN users ON user_skills.user_id = users.id
INNER JOIN skills ON user_skills.skill_id = skills.id;
```

### Join jobs with recruiter details

```sql
SELECT
    jobs.title,
    jobs.company_name,
    users.name AS recruiter_name
FROM jobs
INNER JOIN users ON jobs.recruiter_id = users.id;
```

### Join applications with student and job details

```sql
SELECT
    job_applications.id,
    users.name AS student_name,
    jobs.title,
    job_applications.status
FROM job_applications
INNER JOIN users ON job_applications.student_id = users.id
INNER JOIN jobs ON job_applications.job_id = jobs.id;
```

### Join jobs with required skills

```sql
SELECT
    jobs.title,
    skills.skill_name
FROM job_required_skills
INNER JOIN jobs ON job_required_skills.job_id = jobs.id
INNER JOIN skills ON job_required_skills.skill_id = skills.id;
```

## 14. Left Join Queries

### Show all users with their skills

```sql
SELECT
    users.name,
    skills.skill_name
FROM users
LEFT JOIN user_skills ON users.id = user_skills.user_id
LEFT JOIN skills ON user_skills.skill_id = skills.id;
```

### Show all jobs with applications

```sql
SELECT
    jobs.title,
    job_applications.status
FROM jobs
LEFT JOIN job_applications ON jobs.id = job_applications.job_id;
```

## 15. Subqueries

### Students who have applied for jobs

```sql
SELECT name, email
FROM users
WHERE id IN (
    SELECT student_id
    FROM job_applications
);
```

### Jobs posted by recruiters

```sql
SELECT title, company_name
FROM jobs
WHERE recruiter_id IN (
    SELECT id
    FROM users
    WHERE role = 'recruiter'
);
```

### Skills used by a particular student

```sql
SELECT skill_name
FROM skills
WHERE id IN (
    SELECT skill_id
    FROM user_skills
    WHERE user_id = (
        SELECT id
        FROM users
        WHERE email = 'priya.singh@skillconnect.in'
        LIMIT 1
    )
);
```

### Job titles that require Python

```sql
SELECT title
FROM jobs
WHERE id IN (
    SELECT job_id
    FROM job_required_skills
    WHERE skill_id = (
        SELECT id
        FROM skills
        WHERE skill_name = 'Python'
    )
);
```

### Users who generated resumes

```sql
SELECT name
FROM users
WHERE id IN (
    SELECT user_id
    FROM ai_resumes
);
```

## 16. Simple Project-Based Queries for Viva

```sql
SELECT * FROM users WHERE role = 'student';
```

```sql
SELECT * FROM jobs WHERE is_active = 1;
```

```sql
SELECT name, email FROM users;
```

```sql
SELECT role, COUNT(*) FROM users GROUP BY role;
```

```sql
SELECT jobs.title, users.name
FROM jobs
INNER JOIN users ON jobs.recruiter_id = users.id;
```

```sql
SELECT users.name, skills.skill_name
FROM user_skills
INNER JOIN users ON user_skills.user_id = users.id
INNER JOIN skills ON user_skills.skill_id = skills.id;
```

```sql
SELECT title
FROM jobs
WHERE id IN (
    SELECT job_id
    FROM job_applications
);
```

## 17. Important Note

Most of the sample inserts above use `email`, `skill_name`, and `job title` lookups, so they are safer than fixed IDs.

For best results:
- first run the inserts in the given order
- run the `jobs` insert only once
- if you already have old demo data, check it first with `SELECT * FROM users;`
