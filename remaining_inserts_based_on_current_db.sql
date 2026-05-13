-- Remaining simple inserts based on your current database state
-- Checked against the live DB state in DBMS_project
--
-- Current counts found:
-- users = 18
-- skills = 20
-- user_skills = 20
-- jobs = 20
-- job_required_skills = 42
-- job_applications = 3
-- ai_resumes = 0
-- premium_payments = 0
-- projects = 0
-- certifications = 0
--
-- So this file adds only the missing rows:
-- users: 2 rows
-- job_applications: 17 rows
-- ai_resumes: 20 rows
-- premium_payments: 20 rows
-- projects: 20 rows
-- certifications: 20 rows
--
-- Password for new users is 123456
-- Bcrypt hash:
-- $2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2

-- 1. users: already 18 rows, so add 2 more
INSERT INTO users (
    id, name, email, password, role, created_at, subscription_type, updated_at
) VALUES
    (23, 'Aditi Sharma', 'aditi.sharma@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-04-05 09:00:00', 'free', '2026-04-05 09:00:00'),
    (24, 'Mohit Arora', 'mohit.arora@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-04-05 09:05:00', 'premium', '2026-04-05 09:05:00');

-- 2. skills: already 20 rows, no insert needed

-- 3. user_skills: already 20 rows, no insert needed

-- 4. jobs: already 20 rows, no insert needed

-- 5. job_required_skills: already 42 rows, no insert needed

-- 6. job_applications: already 3 rows, so add 17 more
INSERT INTO job_applications (
    id, job_id, student_id, cover_letter, status, created_at, updated_at
) VALUES
    (4, 3, 3, 'I have worked with Python and MySQL in my academic projects and want backend internship experience.', 'applied', '2026-04-05 09:10:00', '2026-04-05 09:10:00'),
    (5, 4, 5, 'I am interested in frontend development and can contribute to responsive web pages and UI updates.', 'applied', '2026-04-05 09:15:00', '2026-04-05 09:15:00'),
    (6, 5, 8, 'I want to improve my SQL skills further by working on real database tasks and reports.', 'applied', '2026-04-05 09:20:00', '2026-04-05 09:20:00'),
    (7, 6, 9, 'I have used React in college practice projects and would like to learn from production work.', 'applied', '2026-04-05 09:25:00', '2026-04-05 09:25:00'),
    (8, 7, 10, 'Python development interests me and I would like to contribute to backend features and APIs.', 'applied', '2026-04-05 09:30:00', '2026-04-05 09:30:00'),
    (9, 8, 13, 'I enjoy working with data and dashboards and would like to grow as a data analyst intern.', 'applied', '2026-04-05 09:35:00', '2026-04-05 09:35:00'),
    (10, 9, 14, 'I am building my Java fundamentals and want practical exposure through internship work.', 'applied', '2026-04-05 09:40:00', '2026-04-05 09:40:00'),
    (11, 10, 15, 'I have basic HTML, CSS, and Django knowledge and want to contribute to backend modules.', 'applied', '2026-04-05 09:45:00', '2026-04-05 09:45:00'),
    (12, 11, 17, 'Database work interests me and I can support SQL queries, reports, and maintenance tasks.', 'applied', '2026-04-05 09:50:00', '2026-04-05 09:50:00'),
    (13, 12, 18, 'I am interested in Node.js development and eager to work on APIs and backend services.', 'applied', '2026-04-05 09:55:00', '2026-04-05 09:55:00'),
    (14, 13, 19, 'Frontend development is my area of interest and I would like to build UI components and pages.', 'applied', '2026-04-05 10:00:00', '2026-04-05 10:00:00'),
    (15, 14, 20, 'I want to work as a software intern and improve my coding and debugging skills in a team.', 'applied', '2026-04-05 10:05:00', '2026-04-05 10:05:00'),
    (16, 15, 21, 'Machine learning is a field I want to explore further with hands-on internship experience.', 'applied', '2026-04-05 10:10:00', '2026-04-05 10:10:00'),
    (17, 16, 23, 'I have practiced Flask basics and want to contribute to backend route development.', 'applied', '2026-04-05 10:15:00', '2026-04-05 10:15:00'),
    (18, 17, 24, 'Django backend development interests me and I would like to contribute to real features.', 'applied', '2026-04-05 10:20:00', '2026-04-05 10:20:00'),
    (19, 18, 5, 'I enjoy analytics and dashboard work and would like to learn Power BI in a company setting.', 'applied', '2026-04-05 10:25:00', '2026-04-05 10:25:00'),
    (20, 19, 8, 'Testing and QA work will help me improve my software understanding and attention to detail.', 'applied', '2026-04-05 10:30:00', '2026-04-05 10:30:00');

-- 7. ai_resumes: currently 0 rows, so add 20
INSERT INTO ai_resumes (
    id, user_id, target_role, resume_text, created_at
) VALUES
    (1, 3, 'Python Developer Intern', 'Student profile focused on Python, MySQL, and backend project experience.', '2026-04-05 10:35:00'),
    (2, 4, 'Frontend Developer Intern', 'Student profile with interest in JavaScript, web development, and responsive UI design.', '2026-04-05 10:40:00'),
    (3, 5, 'Java Developer Intern', 'Student profile interested in Java programming, software development, and problem solving.', '2026-04-05 10:45:00'),
    (4, 8, 'React Developer Intern', 'Student profile with growing experience in React and modern frontend development.', '2026-04-05 10:50:00'),
    (5, 9, 'Web Developer Intern', 'Student profile focused on HTML, CSS, JavaScript, and frontend practice projects.', '2026-04-05 10:55:00'),
    (6, 10, 'Software Engineer Intern', 'Student profile interested in general software engineering and learning production workflows.', '2026-04-05 11:00:00'),
    (7, 11, 'Technical Recruiter', 'Recruiter profile with focus on sourcing, hiring coordination, and internship hiring support.', '2026-04-05 11:05:00'),
    (8, 12, 'System Administrator', 'Admin profile with oversight of platform management, reporting, and monitoring tasks.', '2026-04-05 11:10:00'),
    (9, 13, 'Full Stack Developer Intern', 'Student profile with interest in frontend and backend development using web technologies.', '2026-04-05 11:15:00'),
    (10, 14, 'Database Intern', 'Student profile interested in SQL, DBMS, and practical database support roles.', '2026-04-05 11:20:00'),
    (11, 15, 'Backend Developer Intern', 'Student profile focused on backend development, APIs, and database-backed applications.', '2026-04-05 11:25:00'),
    (12, 16, 'Recruitment Specialist', 'Recruiter profile with interest in technical hiring and candidate management.', '2026-04-05 11:30:00'),
    (13, 17, 'Software Engineer Intern', 'Student profile with beginner software skills and willingness to grow through hands-on work.', '2026-04-05 11:35:00'),
    (14, 18, 'Junior Developer', 'Student profile with foundational programming knowledge and interest in software projects.', '2026-04-05 11:40:00'),
    (15, 19, 'QA Intern', 'Student profile interested in testing, debugging, and reliable software delivery.', '2026-04-05 11:45:00'),
    (16, 20, 'Backend Intern', 'Student profile with interest in backend systems and API development.', '2026-04-05 11:50:00'),
    (17, 21, 'Python Intern', 'Student profile focused on Python learning, coding practice, and database basics.', '2026-04-05 11:55:00'),
    (18, 22, 'Technical Recruiter', 'Recruiter profile with interest in hiring students and screening technical candidates.', '2026-04-05 12:00:00'),
    (19, 23, 'Flask Developer Intern', 'Student profile with beginner Flask knowledge and backend development interest.', '2026-04-05 12:05:00'),
    (20, 24, 'Django Developer Intern', 'Student profile with beginner Django knowledge and interest in backend web development.', '2026-04-05 12:10:00');

-- 8. premium_payments: currently 0 rows, so add 20
INSERT INTO premium_payments (
    id, user_id, provider, payment_reference, payment_signature, amount_cents, currency, status, created_at, verified_at
) VALUES
    (1, 3, 'razorpay', 'rzp_current_0001', 'sig_current_0001', 99900, 'INR', 'verified', '2026-04-05 12:15:00', '2026-04-05 12:16:00'),
    (2, 4, 'stripe', 'stp_current_0002', 'sig_current_0002', 149900, 'INR', 'verified', '2026-04-05 12:17:00', '2026-04-05 12:18:00'),
    (3, 5, 'razorpay', 'rzp_current_0003', 'sig_current_0003', 99900, 'INR', 'pending', '2026-04-05 12:19:00', NULL),
    (4, 8, 'stripe', 'stp_current_0004', 'sig_current_0004', 99900, 'INR', 'failed', '2026-04-05 12:20:00', NULL),
    (5, 9, 'razorpay', 'rzp_current_0005', 'sig_current_0005', 149900, 'INR', 'verified', '2026-04-05 12:21:00', '2026-04-05 12:22:00'),
    (6, 10, 'stripe', 'stp_current_0006', 'sig_current_0006', 99900, 'INR', 'verified', '2026-04-05 12:23:00', '2026-04-05 12:24:00'),
    (7, 11, 'razorpay', 'rzp_current_0007', 'sig_current_0007', 99900, 'INR', 'pending', '2026-04-05 12:25:00', NULL),
    (8, 12, 'stripe', 'stp_current_0008', 'sig_current_0008', 199900, 'INR', 'verified', '2026-04-05 12:26:00', '2026-04-05 12:27:00'),
    (9, 13, 'razorpay', 'rzp_current_0009', 'sig_current_0009', 149900, 'INR', 'verified', '2026-04-05 12:28:00', '2026-04-05 12:29:00'),
    (10, 14, 'stripe', 'stp_current_0010', 'sig_current_0010', 99900, 'INR', 'failed', '2026-04-05 12:30:00', NULL),
    (11, 15, 'razorpay', 'rzp_current_0011', 'sig_current_0011', 99900, 'INR', 'verified', '2026-04-05 12:31:00', '2026-04-05 12:32:00'),
    (12, 16, 'stripe', 'stp_current_0012', 'sig_current_0012', 149900, 'INR', 'verified', '2026-04-05 12:33:00', '2026-04-05 12:34:00'),
    (13, 17, 'razorpay', 'rzp_current_0013', 'sig_current_0013', 99900, 'INR', 'pending', '2026-04-05 12:35:00', NULL),
    (14, 18, 'stripe', 'stp_current_0014', 'sig_current_0014', 99900, 'INR', 'verified', '2026-04-05 12:36:00', '2026-04-05 12:37:00'),
    (15, 19, 'razorpay', 'rzp_current_0015', 'sig_current_0015', 99900, 'INR', 'failed', '2026-04-05 12:38:00', NULL),
    (16, 20, 'stripe', 'stp_current_0016', 'sig_current_0016', 149900, 'INR', 'verified', '2026-04-05 12:39:00', '2026-04-05 12:40:00'),
    (17, 21, 'razorpay', 'rzp_current_0017', 'sig_current_0017', 99900, 'INR', 'pending', '2026-04-05 12:41:00', NULL),
    (18, 22, 'stripe', 'stp_current_0018', 'sig_current_0018', 149900, 'INR', 'verified', '2026-04-05 12:42:00', '2026-04-05 12:43:00'),
    (19, 23, 'razorpay', 'rzp_current_0019', 'sig_current_0019', 99900, 'INR', 'verified', '2026-04-05 12:44:00', '2026-04-05 12:45:00'),
    (20, 24, 'stripe', 'stp_current_0020', 'sig_current_0020', 149900, 'INR', 'verified', '2026-04-05 12:46:00', '2026-04-05 12:47:00');

-- 9. projects: currently 0 rows, so add 20
INSERT INTO projects (
    id, user_id, title, description, tech_stack, project_link, created_at
) VALUES
    (1, 3, 'Student Task Tracker', 'Task tracking project made to manage study tasks and deadlines.', 'Python, MySQL', 'https://example.com/project1', '2026-04-05 12:48:00'),
    (2, 4, 'Portfolio Website', 'Simple personal portfolio website showing skills and projects.', 'HTML, CSS, JavaScript', 'https://example.com/project2', '2026-04-05 12:49:00'),
    (3, 5, 'Library System', 'Basic library management system for issue and return tracking.', 'Java, MySQL', 'https://example.com/project3', '2026-04-05 12:50:00'),
    (4, 8, 'React Notes App', 'Frontend notes application with create, update, and delete features.', 'React, CSS', 'https://example.com/project4', '2026-04-05 12:51:00'),
    (5, 9, 'Job Portal UI', 'Frontend UI project for browsing jobs and viewing details.', 'HTML, CSS, JavaScript', 'https://example.com/project5', '2026-04-05 12:52:00'),
    (6, 10, 'Code Practice App', 'Simple app for tracking daily coding practice sessions.', 'Python, SQL', 'https://example.com/project6', '2026-04-05 12:53:00'),
    (7, 11, 'Recruitment Dashboard', 'Recruiter dashboard for viewing applicants and shortlisting candidates.', 'React, MySQL', 'https://example.com/project7', '2026-04-05 12:54:00'),
    (8, 12, 'Admin Monitor Panel', 'Admin panel for checking platform users and system activity.', 'Python, MySQL', 'https://example.com/project8', '2026-04-05 12:55:00'),
    (9, 13, 'Blog Platform', 'Mini blog platform with posting and editing functionality.', 'Node.js, MongoDB', 'https://example.com/project9', '2026-04-05 12:56:00'),
    (10, 14, 'SQL Report Tool', 'Project for generating reports from student and placement data.', 'MySQL, Excel', 'https://example.com/project10', '2026-04-05 12:57:00'),
    (11, 15, 'Backend API Demo', 'Practice backend API project using Flask and database integration.', 'Flask, MySQL', 'https://example.com/project11', '2026-04-05 12:58:00'),
    (12, 16, 'Hiring Management App', 'Recruitment workflow application for opening and managing job posts.', 'Django, MySQL', 'https://example.com/project12', '2026-04-05 12:59:00'),
    (13, 17, 'Student Attendance Tool', 'Tool for maintaining attendance records and viewing reports.', 'Python, SQL', 'https://example.com/project13', '2026-04-05 13:00:00'),
    (14, 18, 'Resume Builder', 'Project for generating resumes using form-based user input.', 'HTML, CSS, JavaScript', 'https://example.com/project14', '2026-04-05 13:01:00'),
    (15, 19, 'Testing Tracker', 'Simple testing tracker for recording bugs and test status.', 'Java, MySQL', 'https://example.com/project15', '2026-04-05 13:02:00'),
    (16, 20, 'Placement Portal', 'Placement portal for students to view jobs and apply online.', 'React, Node.js', 'https://example.com/project16', '2026-04-05 13:03:00'),
    (17, 21, 'Python Quiz App', 'Quiz application for practicing Python basics and scoring.', 'Python, HTML', 'https://example.com/project17', '2026-04-05 13:04:00'),
    (18, 22, 'Recruiter CRM', 'Simple recruiter CRM for maintaining candidate and company details.', 'Node.js, MySQL', 'https://example.com/project18', '2026-04-05 13:05:00'),
    (19, 23, 'Flask Blog App', 'Beginner Flask project with routing, templates, and database storage.', 'Flask, SQLite', 'https://example.com/project19', '2026-04-05 13:06:00'),
    (20, 24, 'Django Task App', 'Beginner Django task manager project with models and CRUD operations.', 'Django, MySQL', 'https://example.com/project20', '2026-04-05 13:07:00');

-- 10. certifications: currently 0 rows, so add 20
INSERT INTO certifications (
    id, user_id, certificate_name, organization, issue_date
) VALUES
    (1, 3, 'Python Basics', 'Coursera', '2025-06-10'),
    (2, 4, 'Frontend Web Development', 'Udemy', '2025-06-15'),
    (3, 5, 'Java Programming', 'Coursera', '2025-06-20'),
    (4, 8, 'React Basics', 'Meta', '2025-06-25'),
    (5, 9, 'JavaScript Essentials', 'Cisco', '2025-07-01'),
    (6, 10, 'Software Engineering Basics', 'Infosys Springboard', '2025-07-05'),
    (7, 11, 'Technical Recruitment Fundamentals', 'LinkedIn Learning', '2025-07-10'),
    (8, 12, 'System Administration Basics', 'Oracle Academy', '2025-07-15'),
    (9, 13, 'Full Stack Development', 'Great Learning', '2025-07-20'),
    (10, 14, 'SQL Intermediate', 'HackerRank', '2025-07-25'),
    (11, 15, 'Flask for Beginners', 'Udemy', '2025-08-01'),
    (12, 16, 'Hiring Process Management', 'Coursera', '2025-08-05'),
    (13, 17, 'Python for Everybody', 'Coursera', '2025-08-10'),
    (14, 18, 'Resume Writing Basics', 'Great Learning', '2025-08-15'),
    (15, 19, 'Software Testing Basics', 'Udemy', '2025-08-20'),
    (16, 20, 'Backend Development Basics', 'Infosys Springboard', '2025-08-25'),
    (17, 21, 'Problem Solving Basics', 'HackerRank', '2025-09-01'),
    (18, 22, 'Talent Sourcing Essentials', 'Coursera', '2025-09-05'),
    (19, 23, 'Flask Crash Course', 'Udemy', '2025-09-10'),
    (20, 24, 'Django Application Development', 'Udemy', '2025-09-15');
