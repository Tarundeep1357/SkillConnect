-- Seed data for a fresh SkillConnect database
-- Run this after creating the tables from schema_exact.sql
-- Password for every inserted user is: 123456
-- Bcrypt hash used by the project for 123456:
-- $2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2

START TRANSACTION;

INSERT INTO users (
    id, name, email, password, role, created_at, subscription_type, updated_at
) VALUES
    (1, 'Aarav Sharma', 'aarav.sharma@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', '2026-01-05 09:00:00', 'premium', '2026-01-05 09:00:00'),
    (2, 'Riya Verma', 'riya.verma@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', '2026-01-05 09:05:00', 'free', '2026-01-05 09:05:00'),
    (3, 'Karan Mehta', 'karan.mehta@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', '2026-01-05 09:10:00', 'premium', '2026-01-05 09:10:00'),
    (4, 'Neha Kapoor', 'neha.kapoor@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', '2026-01-05 09:15:00', 'free', '2026-01-05 09:15:00'),
    (5, 'Vikram Nair', 'vikram.nair@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', '2026-01-05 09:20:00', 'premium', '2026-01-05 09:20:00'),
    (6, 'Admin User', 'admin@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'admin', '2026-01-05 09:25:00', 'premium', '2026-01-05 09:25:00'),
    (7, 'Priya Singh', 'priya.singh@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:30:00', 'free', '2026-01-05 09:30:00'),
    (8, 'Rahul Gupta', 'rahul.gupta@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:35:00', 'free', '2026-01-05 09:35:00'),
    (9, 'Ananya Iyer', 'ananya.iyer@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:40:00', 'premium', '2026-01-05 09:40:00'),
    (10, 'Aditya Rao', 'aditya.rao@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:45:00', 'free', '2026-01-05 09:45:00'),
    (11, 'Sneha Patil', 'sneha.patil@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:50:00', 'free', '2026-01-05 09:50:00'),
    (12, 'Rohit Jain', 'rohit.jain@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 09:55:00', 'free', '2026-01-05 09:55:00'),
    (13, 'Pooja Reddy', 'pooja.reddy@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:00:00', 'premium', '2026-01-05 10:00:00'),
    (14, 'Arjun Malhotra', 'arjun.malhotra@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:05:00', 'free', '2026-01-05 10:05:00'),
    (15, 'Kavya Menon', 'kavya.menon@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:10:00', 'free', '2026-01-05 10:10:00'),
    (16, 'Yash Thakur', 'yash.thakur@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:15:00', 'free', '2026-01-05 10:15:00'),
    (17, 'Nisha Bansal', 'nisha.bansal@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:20:00', 'premium', '2026-01-05 10:20:00'),
    (18, 'Siddharth Kulkarni', 'siddharth.kulkarni@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:25:00', 'free', '2026-01-05 10:25:00'),
    (19, 'Meera Joshi', 'meera.joshi@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:30:00', 'free', '2026-01-05 10:30:00'),
    (20, 'Devansh Choudhary', 'devansh.choudhary@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', '2026-01-05 10:35:00', 'free', '2026-01-05 10:35:00');

INSERT INTO skills (
    id, skill_name, category, created_at
) VALUES
    (1, 'Python', 'Programming', '2026-01-06 08:00:00'),
    (2, 'MySQL', 'Database', '2026-01-06 08:05:00'),
    (3, 'Java', 'Programming', '2026-01-06 08:10:00'),
    (4, 'C', 'Programming', '2026-01-06 08:15:00'),
    (5, 'C++', 'Programming', '2026-01-06 08:20:00'),
    (6, 'JavaScript', 'Web', '2026-01-06 08:25:00'),
    (7, 'HTML', 'Web', '2026-01-06 08:30:00'),
    (8, 'CSS', 'Web', '2026-01-06 08:35:00'),
    (9, 'React', 'Web', '2026-01-06 08:40:00'),
    (10, 'Node.js', 'Backend', '2026-01-06 08:45:00'),
    (11, 'Django', 'Backend', '2026-01-06 08:50:00'),
    (12, 'Flask', 'Backend', '2026-01-06 08:55:00'),
    (13, 'MongoDB', 'Database', '2026-01-06 09:00:00'),
    (14, 'SQL', 'Database', '2026-01-06 09:05:00'),
    (15, 'Git', 'Tools', '2026-01-06 09:10:00'),
    (16, 'Excel', 'Analytics', '2026-01-06 09:15:00'),
    (17, 'Power BI', 'Analytics', '2026-01-06 09:20:00'),
    (18, 'Machine Learning', 'AI', '2026-01-06 09:25:00'),
    (19, 'FastAPI', 'Backend', '2026-01-06 09:30:00'),
    (20, 'Data Structures', 'Computer Science', '2026-01-06 09:35:00');

INSERT INTO user_skills (
    id, user_id, skill_id, proficiency_level, created_at
) VALUES
    (1, 7, 1, 'Advanced', '2026-01-07 10:00:00'),
    (2, 7, 14, 'Intermediate', '2026-01-07 10:05:00'),
    (3, 8, 6, 'Advanced', '2026-01-07 10:10:00'),
    (4, 8, 9, 'Intermediate', '2026-01-07 10:15:00'),
    (5, 9, 1, 'Expert', '2026-01-07 10:20:00'),
    (6, 9, 11, 'Advanced', '2026-01-07 10:25:00'),
    (7, 10, 3, 'Intermediate', '2026-01-07 10:30:00'),
    (8, 11, 7, 'Advanced', '2026-01-07 10:35:00'),
    (9, 11, 8, 'Advanced', '2026-01-07 10:40:00'),
    (10, 12, 2, 'Advanced', '2026-01-07 10:45:00'),
    (11, 12, 14, 'Advanced', '2026-01-07 10:50:00'),
    (12, 13, 18, 'Intermediate', '2026-01-07 10:55:00'),
    (13, 13, 17, 'Intermediate', '2026-01-07 11:00:00'),
    (14, 14, 4, 'Intermediate', '2026-01-07 11:05:00'),
    (15, 15, 5, 'Intermediate', '2026-01-07 11:10:00'),
    (16, 16, 10, 'Advanced', '2026-01-07 11:15:00'),
    (17, 17, 13, 'Intermediate', '2026-01-07 11:20:00'),
    (18, 18, 19, 'Advanced', '2026-01-07 11:25:00'),
    (19, 19, 16, 'Advanced', '2026-01-07 11:30:00'),
    (20, 20, 20, 'Intermediate', '2026-01-07 11:35:00');

INSERT INTO jobs (
    id, recruiter_id, title, company_name, location, employment_type, description,
    required_skills, salary_range, is_active, created_at, updated_at
) VALUES
    (1, 1, 'Backend Developer Intern', 'TechNova Labs', 'Bengaluru', 'internship', 'Build backend APIs and optimize database queries for client platforms.', 'Python, MySQL', '300000-450000', 1, '2026-01-08 09:00:00', '2026-01-08 09:00:00'),
    (2, 1, 'SQL Developer Trainee', 'DataBridge Solutions', 'Pune', 'full-time', 'Write efficient SQL queries and support reporting workflows.', 'SQL, MySQL', '420000-600000', 1, '2026-01-08 09:10:00', '2026-01-08 09:10:00'),
    (3, 1, 'Junior FastAPI Developer', 'CloudAxis Systems', 'Remote', 'full-time', 'Develop REST APIs using Python and maintain service integrations.', 'Python, FastAPI', '500000-700000', 1, '2026-01-08 09:20:00', '2026-01-08 09:20:00'),
    (4, 1, 'Data Analyst Intern', 'InsightHive Analytics', 'Hyderabad', 'internship', 'Create reports and dashboards for business and product teams.', 'Excel, Power BI', '280000-400000', 1, '2026-01-08 09:30:00', '2026-01-08 09:30:00'),
    (5, 2, 'Frontend Developer Intern', 'PixelCraft Studio', 'Mumbai', 'internship', 'Build responsive interfaces and improve landing page components.', 'HTML, CSS, JavaScript', '260000-380000', 1, '2026-01-08 09:40:00', '2026-01-08 09:40:00'),
    (6, 2, 'React Developer Intern', 'WebNest Technologies', 'Chennai', 'internship', 'Create React screens and connect them to backend APIs.', 'React, JavaScript', '300000-430000', 1, '2026-01-08 09:50:00', '2026-01-08 09:50:00'),
    (7, 2, 'UI Engineer Trainee', 'BrightLayer Digital', 'Remote', 'full-time', 'Improve web UI quality and implement reusable interface modules.', 'HTML, CSS, React', '450000-650000', 1, '2026-01-08 10:00:00', '2026-01-08 10:00:00'),
    (8, 2, 'Node.js Developer Intern', 'RapidStack Labs', 'Noida', 'internship', 'Support backend services and API integrations in Node.js.', 'Node.js, Git', '310000-440000', 1, '2026-01-08 10:10:00', '2026-01-08 10:10:00'),
    (9, 3, 'Java Developer Intern', 'FinEdge Software', 'Bengaluru', 'internship', 'Assist with Java module development and debugging tasks.', 'Java, Git', '300000-450000', 1, '2026-01-08 10:20:00', '2026-01-08 10:20:00'),
    (10, 3, 'Django Backend Intern', 'SecureNet Apps', 'Kolkata', 'internship', 'Develop secure backend features and database integrations.', 'Python, Django', '320000-470000', 1, '2026-01-08 10:30:00', '2026-01-08 10:30:00'),
    (11, 3, 'Machine Learning Intern', 'VisionAI Research', 'Pune', 'internship', 'Prepare data, train prototype models, and evaluate results.', 'Machine Learning, Python', '350000-500000', 1, '2026-01-08 10:40:00', '2026-01-08 10:40:00'),
    (12, 3, 'Database Support Engineer', 'QueryWorks Pvt Ltd', 'Hyderabad', 'full-time', 'Monitor database performance and support SQL issue resolution.', 'MySQL, SQL', '480000-680000', 1, '2026-01-08 10:50:00', '2026-01-08 10:50:00'),
    (13, 4, 'Full Stack Developer Trainee', 'NextGen Portal', 'Indore', 'full-time', 'Contribute to frontend and backend features for internal platforms.', 'React, Node.js', '500000-720000', 1, '2026-01-08 11:00:00', '2026-01-08 11:00:00'),
    (14, 4, 'Flask Developer Intern', 'APIForge Technologies', 'Remote', 'internship', 'Build backend endpoints and connect services using Flask.', 'Python, Flask', '300000-430000', 1, '2026-01-08 11:10:00', '2026-01-08 11:10:00'),
    (15, 4, 'Software Testing Intern', 'QualityFirst Systems', 'Jaipur', 'internship', 'Test web applications and document reproducible defects.', 'Git, SQL', '250000-360000', 1, '2026-01-08 11:20:00', '2026-01-08 11:20:00'),
    (16, 4, 'C++ Developer Trainee', 'CoreCompute Labs', 'Bengaluru', 'full-time', 'Work on system level modules and optimize performance critical code.', 'C++, Data Structures', '520000-750000', 1, '2026-01-08 11:30:00', '2026-01-08 11:30:00'),
    (17, 5, 'Power BI Analyst Intern', 'MetricMind Solutions', 'Gurugram', 'internship', 'Create dashboard reports and analyze business trends.', 'Power BI, Excel', '280000-410000', 1, '2026-01-08 11:40:00', '2026-01-08 11:40:00'),
    (18, 5, 'MongoDB Developer Intern', 'DocuScale Systems', 'Chennai', 'internship', 'Support document database models and backend integration work.', 'MongoDB, Node.js', '290000-420000', 1, '2026-01-08 11:50:00', '2026-01-08 11:50:00'),
    (19, 5, 'Junior Web Developer', 'HorizonStack Media', 'Kochi', 'full-time', 'Maintain company websites and improve page speed and styling.', 'HTML, CSS, JavaScript', '400000-580000', 1, '2026-01-08 12:00:00', '2026-01-08 12:00:00'),
    (20, 5, 'Data Engineer Intern', 'StreamForge Data', 'Pune', 'internship', 'Prepare datasets and support data pipeline development tasks.', 'Python, SQL', '330000-470000', 1, '2026-01-08 12:10:00', '2026-01-08 12:10:00');

INSERT INTO job_required_skills (
    job_id, skill_id, created_at
) VALUES
    (1, 1, '2026-01-08 12:20:00'),
    (2, 14, '2026-01-08 12:21:00'),
    (3, 19, '2026-01-08 12:22:00'),
    (4, 17, '2026-01-08 12:23:00'),
    (5, 6, '2026-01-08 12:24:00'),
    (6, 9, '2026-01-08 12:25:00'),
    (7, 9, '2026-01-08 12:26:00'),
    (8, 10, '2026-01-08 12:27:00'),
    (9, 3, '2026-01-08 12:28:00'),
    (10, 11, '2026-01-08 12:29:00'),
    (11, 18, '2026-01-08 12:30:00'),
    (12, 2, '2026-01-08 12:31:00'),
    (13, 10, '2026-01-08 12:32:00'),
    (14, 12, '2026-01-08 12:33:00'),
    (15, 15, '2026-01-08 12:34:00'),
    (16, 5, '2026-01-08 12:35:00'),
    (17, 17, '2026-01-08 12:36:00'),
    (18, 13, '2026-01-08 12:37:00'),
    (19, 7, '2026-01-08 12:38:00'),
    (20, 14, '2026-01-08 12:39:00');

INSERT INTO job_applications (
    id, job_id, student_id, cover_letter, status, created_at, updated_at
) VALUES
    (1, 1, 7, 'I have built Python and MySQL projects in college and would like to contribute to backend work.', 'applied', '2026-01-09 09:00:00', '2026-01-09 09:00:00'),
    (2, 2, 12, 'My coursework includes SQL optimization and database design, which fits this trainee role well.', 'reviewed', '2026-01-09 09:10:00', '2026-01-09 10:00:00'),
    (3, 3, 9, 'I enjoy building APIs with Python and have practiced service development in academic projects.', 'shortlisted', '2026-01-09 09:20:00', '2026-01-09 11:00:00'),
    (4, 4, 19, 'I am comfortable with Excel reporting and want to learn business analytics in a real team.', 'applied', '2026-01-09 09:30:00', '2026-01-09 09:30:00'),
    (5, 5, 11, 'I have created responsive websites using HTML, CSS, and JavaScript and can contribute quickly.', 'reviewed', '2026-01-09 09:40:00', '2026-01-09 10:40:00'),
    (6, 6, 8, 'I have worked on React components and API integration in my mini project work.', 'shortlisted', '2026-01-09 09:50:00', '2026-01-09 11:10:00'),
    (7, 7, 15, 'I enjoy frontend development and can support reusable UI work with clean code.', 'applied', '2026-01-09 10:00:00', '2026-01-09 10:00:00'),
    (8, 8, 16, 'My Node.js practice projects have prepared me for API and service development tasks.', 'reviewed', '2026-01-09 10:10:00', '2026-01-09 11:20:00'),
    (9, 9, 10, 'I am improving my Java skills and would like exposure to enterprise style development.', 'rejected', '2026-01-09 10:20:00', '2026-01-09 11:30:00'),
    (10, 10, 9, 'I have experience with Python frameworks and want to deepen my backend knowledge.', 'applied', '2026-01-09 10:30:00', '2026-01-09 10:30:00'),
    (11, 11, 13, 'I am interested in machine learning workflows and have completed beginner model training exercises.', 'shortlisted', '2026-01-09 10:40:00', '2026-01-09 11:40:00'),
    (12, 12, 12, 'Database administration and SQL troubleshooting are areas I want to build professionally.', 'reviewed', '2026-01-09 10:50:00', '2026-01-09 11:50:00'),
    (13, 13, 18, 'I can contribute to full stack work and adapt quickly across frontend and backend modules.', 'applied', '2026-01-09 11:00:00', '2026-01-09 11:00:00'),
    (14, 14, 20, 'I have built small Flask apps and would like to work on production style APIs.', 'reviewed', '2026-01-09 11:10:00', '2026-01-09 12:00:00'),
    (15, 15, 14, 'I pay attention to detail and can support testing, defect logging, and SQL validation tasks.', 'rejected', '2026-01-09 11:20:00', '2026-01-09 12:10:00'),
    (16, 16, 15, 'I have strong interest in C++ and problem solving using data structures.', 'shortlisted', '2026-01-09 11:30:00', '2026-01-09 12:20:00'),
    (17, 17, 17, 'I enjoy dashboard creation and data storytelling using Power BI and Excel.', 'applied', '2026-01-09 11:40:00', '2026-01-09 11:40:00'),
    (18, 18, 16, 'I have explored MongoDB and would like practical backend database experience.', 'reviewed', '2026-01-09 11:50:00', '2026-01-09 12:30:00'),
    (19, 19, 11, 'I can support website maintenance and frontend fixes with solid HTML and CSS basics.', 'shortlisted', '2026-01-09 12:00:00', '2026-01-09 12:40:00'),
    (20, 20, 7, 'I have worked with Python and SQL together and want to learn data engineering practices.', 'applied', '2026-01-09 12:10:00', '2026-01-09 12:10:00');

INSERT INTO ai_resumes (
    id, user_id, target_role, resume_text, created_at
) VALUES
    (1, 1, 'Technical Recruiter', 'Recruiter with experience in campus hiring, profile screening, and employer branding initiatives.', '2026-01-10 09:00:00'),
    (2, 2, 'Talent Acquisition Specialist', 'Recruiter focused on candidate sourcing, interview coordination, and communication with hiring managers.', '2026-01-10 09:05:00'),
    (3, 3, 'Technical Recruiter', 'Recruitment professional experienced in matching engineering talent with fast growing product teams.', '2026-01-10 09:10:00'),
    (4, 4, 'Recruitment Coordinator', 'Organized recruiter skilled in interview scheduling, applicant tracking, and candidate follow-up.', '2026-01-10 09:15:00'),
    (5, 5, 'Campus Hiring Lead', 'Recruiter with strong focus on internship drives, student outreach, and employer engagement.', '2026-01-10 09:20:00'),
    (6, 6, 'System Administrator', 'Administrative user profile with oversight of user management, reporting, and system level operations.', '2026-01-10 09:25:00'),
    (7, 7, 'Backend Developer Intern', 'Student with Python and SQL skills, interested in API development and database backed applications.', '2026-01-10 09:30:00'),
    (8, 8, 'React Developer Intern', 'Student with JavaScript and React experience from academic and personal frontend projects.', '2026-01-10 09:35:00'),
    (9, 9, 'Django Developer Intern', 'Student with strong Python fundamentals and hands on practice building backend features with Django.', '2026-01-10 09:40:00'),
    (10, 10, 'Java Developer Intern', 'Student with Java basics, version control knowledge, and interest in scalable software systems.', '2026-01-10 09:45:00'),
    (11, 11, 'Frontend Developer Intern', 'Student with solid HTML and CSS skills and a growing interest in responsive UI development.', '2026-01-10 09:50:00'),
    (12, 12, 'Database Analyst Intern', 'Student comfortable with MySQL and SQL query writing, data cleanup, and reporting support.', '2026-01-10 09:55:00'),
    (13, 13, 'Machine Learning Intern', 'Student exploring machine learning concepts, analytics tools, and applied model evaluation tasks.', '2026-01-10 10:00:00'),
    (14, 14, 'C Programmer Trainee', 'Student with problem solving interest and practical exposure to programming fundamentals in C.', '2026-01-10 10:05:00'),
    (15, 15, 'C++ Developer Trainee', 'Student with C++ basics, data structure knowledge, and interest in software optimization.', '2026-01-10 10:10:00'),
    (16, 16, 'Node.js Developer Intern', 'Student with backend curiosity and hands on work in Node.js and API integration exercises.', '2026-01-10 10:15:00'),
    (17, 17, 'MongoDB Developer Intern', 'Student with growing interest in NoSQL databases, dashboards, and analytics driven systems.', '2026-01-10 10:20:00'),
    (18, 18, 'FastAPI Developer Intern', 'Student with Python API practice and interest in modern backend framework development.', '2026-01-10 10:25:00'),
    (19, 19, 'Data Analyst Intern', 'Student with Excel reporting experience and interest in analytics and dashboard creation.', '2026-01-10 10:30:00'),
    (20, 20, 'Software Engineer Intern', 'Student with data structure fundamentals and willingness to learn across backend and systems roles.', '2026-01-10 10:35:00');

INSERT INTO premium_payments (
    id, user_id, provider, payment_reference, payment_signature, amount_cents,
    currency, status, created_at, verified_at
) VALUES
    (1, 1, 'razorpay', 'rzp_2026_0001', 'sig_2026_user01', 199900, 'INR', 'verified', '2026-01-11 09:00:00', '2026-01-11 09:05:00'),
    (2, 2, 'stripe', 'stp_2026_0002', 'sig_2026_user02', 99900, 'INR', 'failed', '2026-01-11 09:10:00', NULL),
    (3, 3, 'razorpay', 'rzp_2026_0003', 'sig_2026_user03', 199900, 'INR', 'verified', '2026-01-11 09:20:00', '2026-01-11 09:25:00'),
    (4, 4, 'stripe', 'stp_2026_0004', 'sig_2026_user04', 99900, 'INR', 'pending', '2026-01-11 09:30:00', NULL),
    (5, 5, 'razorpay', 'rzp_2026_0005', 'sig_2026_user05', 199900, 'INR', 'verified', '2026-01-11 09:40:00', '2026-01-11 09:45:00'),
    (6, 6, 'stripe', 'stp_2026_0006', 'sig_2026_user06', 249900, 'INR', 'verified', '2026-01-11 09:50:00', '2026-01-11 09:55:00'),
    (7, 7, 'razorpay', 'rzp_2026_0007', 'sig_2026_user07', 99900, 'INR', 'failed', '2026-01-11 10:00:00', NULL),
    (8, 8, 'stripe', 'stp_2026_0008', 'sig_2026_user08', 99900, 'INR', 'pending', '2026-01-11 10:10:00', NULL),
    (9, 9, 'razorpay', 'rzp_2026_0009', 'sig_2026_user09', 149900, 'INR', 'verified', '2026-01-11 10:20:00', '2026-01-11 10:25:00'),
    (10, 10, 'stripe', 'stp_2026_0010', 'sig_2026_user10', 99900, 'INR', 'failed', '2026-01-11 10:30:00', NULL),
    (11, 11, 'razorpay', 'rzp_2026_0011', 'sig_2026_user11', 99900, 'INR', 'pending', '2026-01-11 10:40:00', NULL),
    (12, 12, 'stripe', 'stp_2026_0012', 'sig_2026_user12', 99900, 'INR', 'verified', '2026-01-11 10:50:00', '2026-01-11 10:55:00'),
    (13, 13, 'razorpay', 'rzp_2026_0013', 'sig_2026_user13', 149900, 'INR', 'verified', '2026-01-11 11:00:00', '2026-01-11 11:05:00'),
    (14, 14, 'stripe', 'stp_2026_0014', 'sig_2026_user14', 99900, 'INR', 'failed', '2026-01-11 11:10:00', NULL),
    (15, 15, 'razorpay', 'rzp_2026_0015', 'sig_2026_user15', 99900, 'INR', 'pending', '2026-01-11 11:20:00', NULL),
    (16, 16, 'stripe', 'stp_2026_0016', 'sig_2026_user16', 99900, 'INR', 'verified', '2026-01-11 11:30:00', '2026-01-11 11:35:00'),
    (17, 17, 'razorpay', 'rzp_2026_0017', 'sig_2026_user17', 149900, 'INR', 'verified', '2026-01-11 11:40:00', '2026-01-11 11:45:00'),
    (18, 18, 'stripe', 'stp_2026_0018', 'sig_2026_user18', 99900, 'INR', 'pending', '2026-01-11 11:50:00', NULL),
    (19, 19, 'razorpay', 'rzp_2026_0019', 'sig_2026_user19', 99900, 'INR', 'failed', '2026-01-11 12:00:00', NULL),
    (20, 20, 'stripe', 'stp_2026_0020', 'sig_2026_user20', 99900, 'INR', 'verified', '2026-01-11 12:10:00', '2026-01-11 12:15:00');

INSERT INTO projects (
    id, user_id, title, description, tech_stack, project_link, created_at
) VALUES
    (1, 1, 'Campus Hiring Dashboard', 'Internal recruiter dashboard for managing student applications and interview pipelines.', 'React, FastAPI, MySQL', 'https://example.com/projects/campus-hiring-dashboard', '2026-01-12 09:00:00'),
    (2, 2, 'Resume Filter Portal', 'Recruitment support tool for sorting and tracking candidate profiles by skills and scores.', 'HTML, CSS, JavaScript', 'https://example.com/projects/resume-filter-portal', '2026-01-12 09:05:00'),
    (3, 3, 'Interview Tracker', 'Portal to schedule interviews and maintain recruiter feedback records.', 'Node.js, MySQL', 'https://example.com/projects/interview-tracker', '2026-01-12 09:10:00'),
    (4, 4, 'Applicant CRM Lite', 'Simple candidate relationship management tool for internship programs.', 'React, Node.js, MongoDB', 'https://example.com/projects/applicant-crm-lite', '2026-01-12 09:15:00'),
    (5, 5, 'Referral Management Tool', 'Web app to handle referral submissions and recruiter review flows.', 'FastAPI, MySQL, HTML', 'https://example.com/projects/referral-management-tool', '2026-01-12 09:20:00'),
    (6, 6, 'Admin Audit Console', 'Administrative panel for monitoring users, jobs, and payment verification events.', 'Python, FastAPI, MySQL', 'https://example.com/projects/admin-audit-console', '2026-01-12 09:25:00'),
    (7, 7, 'Student Skill Matcher', 'Project that matches student profiles to internships using skill overlap scores.', 'Python, SQL', 'https://example.com/projects/student-skill-matcher', '2026-01-12 09:30:00'),
    (8, 8, 'Portfolio Builder', 'Frontend app for creating and publishing student portfolio pages.', 'React, CSS, JavaScript', 'https://example.com/projects/portfolio-builder', '2026-01-12 09:35:00'),
    (9, 9, 'Academic API Suite', 'Collection of backend APIs for student records and project submission workflows.', 'Django, MySQL', 'https://example.com/projects/academic-api-suite', '2026-01-12 09:40:00'),
    (10, 10, 'Code Practice Tracker', 'Tool for logging coding progress, streaks, and interview prep goals.', 'Java, MySQL', 'https://example.com/projects/code-practice-tracker', '2026-01-12 09:45:00'),
    (11, 11, 'Responsive College Site', 'Modern college information website with responsive sections and contact forms.', 'HTML, CSS, JavaScript', 'https://example.com/projects/responsive-college-site', '2026-01-12 09:50:00'),
    (12, 12, 'SQL Report Generator', 'Database utility to produce attendance and placement summary reports.', 'MySQL, SQL, Excel', 'https://example.com/projects/sql-report-generator', '2026-01-12 09:55:00'),
    (13, 13, 'Student Performance Predictor', 'Machine learning project that estimates placement readiness from academic inputs.', 'Python, Machine Learning, Power BI', 'https://example.com/projects/student-performance-predictor', '2026-01-12 10:00:00'),
    (14, 14, 'C Programming Lab Toolkit', 'Console based toolkit covering classic array and string problem statements.', 'C, Data Structures', 'https://example.com/projects/c-programming-lab-toolkit', '2026-01-12 10:05:00'),
    (15, 15, 'DSA Visualizer', 'Interactive visualizer for sorting and searching concepts for beginners.', 'C++, HTML, CSS', 'https://example.com/projects/dsa-visualizer', '2026-01-12 10:10:00'),
    (16, 16, 'Realtime Chat API', 'Backend service for chat messaging and notification experiments.', 'Node.js, MongoDB', 'https://example.com/projects/realtime-chat-api', '2026-01-12 10:15:00'),
    (17, 17, 'Sales Analytics Dashboard', 'Dashboard showing trends, KPIs, and drill down analysis for sample data.', 'Power BI, Excel', 'https://example.com/projects/sales-analytics-dashboard', '2026-01-12 10:20:00'),
    (18, 18, 'FastAPI Task Manager', 'Task management API with authentication and CRUD operations.', 'FastAPI, MySQL, Git', 'https://example.com/projects/fastapi-task-manager', '2026-01-12 10:25:00'),
    (19, 19, 'Placement Data Workbook', 'Analytical workbook for tracking placement performance and recruiter activity.', 'Excel, SQL', 'https://example.com/projects/placement-data-workbook', '2026-01-12 10:30:00'),
    (20, 20, 'Algorithm Notes Hub', 'Repository style portal for data structure notes and coding patterns.', 'Data Structures, HTML, CSS', 'https://example.com/projects/algorithm-notes-hub', '2026-01-12 10:35:00');

INSERT INTO certifications (
    id, user_id, certificate_name, organization, issue_date
) VALUES
    (1, 1, 'Technical Recruitment Fundamentals', 'LinkedIn Learning', '2025-06-15'),
    (2, 2, 'Talent Sourcing Essentials', 'Coursera', '2025-07-10'),
    (3, 3, 'Hiring Process Management', 'Udemy', '2025-08-20'),
    (4, 4, 'HR Analytics Basics', 'Great Learning', '2025-09-05'),
    (5, 5, 'Campus Hiring Strategy', 'Simplilearn', '2025-10-12'),
    (6, 6, 'Database Administration Basics', 'Oracle Academy', '2025-05-18'),
    (7, 7, 'Python for Everybody', 'Coursera', '2025-11-01'),
    (8, 8, 'React Basics', 'Meta', '2025-11-08'),
    (9, 9, 'Django Application Development', 'Udemy', '2025-11-15'),
    (10, 10, 'Java Programming Masterclass', 'Udemy', '2025-11-22'),
    (11, 11, 'Responsive Web Design', 'freeCodeCamp', '2025-11-29'),
    (12, 12, 'SQL Intermediate', 'HackerRank', '2025-12-03'),
    (13, 13, 'Machine Learning Foundations', 'Coursera', '2025-12-07'),
    (14, 14, 'C Programming Certification', 'Infosys Springboard', '2025-12-10'),
    (15, 15, 'Data Structures in C++', 'NPTEL', '2025-12-12'),
    (16, 16, 'Node.js Essentials', 'IBM SkillsBuild', '2025-12-15'),
    (17, 17, 'MongoDB Basics', 'MongoDB University', '2025-12-18'),
    (18, 18, 'FastAPI Crash Course', 'Udemy', '2025-12-20'),
    (19, 19, 'Excel for Data Analysis', 'Coursera', '2025-12-23'),
    (20, 20, 'Problem Solving Basics', 'HackerRank', '2025-12-27');

COMMIT;
