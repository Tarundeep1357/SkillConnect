# Insert Queries Based On Current Database

This file is based on the current live database state.

Current counts:
- `users` = 17
- `skills` = 20
- `user_skills` = 20
- `jobs` = 2

Target:
- `users` = 20
- `skills` = 20
- `user_skills` = 20
- `jobs` = 20

Important note:
- This file only adds rows where more rows are needed.
- The new rows below are written so they do not insert `NULL` values.
- Your database already has some older rows with `NULL` values in other tables/columns.
- Since you asked for insert queries only, this file does not update or delete old rows.

## 1. Insert 3 Rows Into `users`

After this, `users` will become 20 rows.

Password for all 3 new users:
- `123456`

```sql
INSERT INTO users (
    name,
    email,
    password,
    role,
    subscription_type,
    created_at,
    updated_at
)
VALUES
('Aarav Sharma', 'aarav.sharma.college@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'recruiter', 'free', NOW(), NOW()),
('Priya Nair', 'priya.nair.college@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', 'free', NOW(), NOW()),
('Kavya Reddy', 'kavya.reddy.college@skillconnect.in', '$2b$12$ckwwvVdMJ3GXa5r5qV5feO2lNXONBs2hkwcFUfiQn7aU0gIlkbsd2', 'student', 'premium', NOW(), NOW());
```

## 2. `skills` Table

No insert is needed now.

Reason:
- `skills` already has 20 rows

## 3. `user_skills` Table

No insert is needed now.

Reason:
- `user_skills` already has 20 rows

## 4. Insert 18 Rows Into `jobs`

After this, `jobs` will become 20 rows.

Existing recruiter IDs in your database:
- `11` = `rish@example.com`
- `16` = `tarundeepsingh@mail.com`

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
    is_active,
    created_at,
    updated_at
)
VALUES
(11, 'Backend Developer Intern', 'Infosys', 'Bengaluru', 'internship', 'Work on backend APIs and database operations for web applications.', 'Python, MySQL', '300000-450000', 1, NOW(), NOW()),
(11, 'Frontend Developer Intern', 'TCS', 'Pune', 'internship', 'Build responsive pages and improve frontend components for company portals.', 'HTML, CSS, JavaScript', '250000-400000', 1, NOW(), NOW()),
(11, 'SQL Developer Intern', 'Wipro', 'Hyderabad', 'internship', 'Write SQL queries and support daily reporting and database tasks.', 'SQL, MySQL', '280000-420000', 1, NOW(), NOW()),
(11, 'React Developer Intern', 'Cognizant', 'Chennai', 'internship', 'Develop React pages and connect frontend modules with APIs.', 'React, JavaScript', '300000-430000', 1, NOW(), NOW()),
(11, 'Python Developer Intern', 'Zoho', 'Chennai', 'internship', 'Support backend feature development using Python and database queries.', 'Python, SQL', '320000-460000', 1, NOW(), NOW()),
(11, 'Data Analyst Intern', 'HCLTech', 'Noida', 'internship', 'Prepare reports and perform data analysis for business teams.', 'Excel, SQL', '280000-410000', 1, NOW(), NOW()),
(11, 'Java Developer Intern', 'Tech Mahindra', 'Mumbai', 'internship', 'Assist in Java application development and debugging tasks.', 'Java, Git', '300000-450000', 1, NOW(), NOW()),
(11, 'Web Developer Intern', 'Mindtree', 'Bengaluru', 'internship', 'Develop website modules and improve page layouts and forms.', 'HTML, CSS', '260000-380000', 1, NOW(), NOW()),
(11, 'Database Intern', 'ICICI Bank', 'Mumbai', 'internship', 'Support data handling and database maintenance work.', 'MySQL, DBMS', '300000-430000', 1, NOW(), NOW()),
(16, 'Node.js Intern', 'Paytm', 'Noida', 'internship', 'Work on backend services and API integration tasks.', 'Node.js, JavaScript', '310000-440000', 1, NOW(), NOW()),
(16, 'UI Developer Intern', 'LTIMindtree', 'Mumbai', 'internship', 'Create simple user interfaces and update dashboard pages.', 'HTML, CSS, React', '270000-390000', 1, NOW(), NOW()),
(16, 'Software Engineer Intern', 'Mphasis', 'Pune', 'internship', 'Support software modules, testing, and issue fixes.', 'Java, SQL', '290000-420000', 1, NOW(), NOW()),
(16, 'Machine Learning Intern', 'Reliance Jio', 'Mumbai', 'internship', 'Support basic machine learning workflows and model testing.', 'ml, scikit-learn', '350000-500000', 1, NOW(), NOW()),
(16, 'Flask Developer Intern', 'Freshworks', 'Chennai', 'internship', 'Build simple backend routes and connect APIs using Flask.', 'Python, Flask', '300000-440000', 1, NOW(), NOW()),
(16, 'Django Developer Intern', 'Flipkart', 'Bengaluru', 'internship', 'Work on Django modules and backend improvements.', 'Python, Django', '330000-470000', 1, NOW(), NOW()),
(16, 'Power BI Intern', 'Capgemini', 'Pune', 'internship', 'Create dashboards and business reports using Power BI.', 'Power BI, Excel', '280000-410000', 1, NOW(), NOW()),
(16, 'Testing Intern', 'TCS', 'Kolkata', 'internship', 'Perform testing and document defects for internal products.', 'Java, DBMS', '250000-360000', 1, NOW(), NOW()),
(16, 'MongoDB Intern', 'Infosys', 'Mysuru', 'internship', 'Help manage document data and support backend teams.', 'MongoDB, Node.js', '290000-420000', 1, NOW(), NOW());
```

## 5. Check Final Counts

```sql
SELECT COUNT(*) AS total_users FROM users;
SELECT COUNT(*) AS total_skills FROM skills;
SELECT COUNT(*) AS total_user_skills FROM user_skills;
SELECT COUNT(*) AS total_jobs FROM jobs;
```

Expected result:
- `users` = 20
- `skills` = 20
- `user_skills` = 20
- `jobs` = 20

