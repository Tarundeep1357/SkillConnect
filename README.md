# SkillConnect

## What I Learned and Understood From This Project
This project is more than a DBMS assignment for me. While building SkillConnect, I understood how database concepts work in a real application instead of only in theory. I learned that a database is not just for storing records - it controls relationships, user roles, permissions, workflows, reports, and the complete flow of a platform.

Through this project, I learned how to design tables for users, skills, jobs, applications, resumes, payments, and messages in a way that reflects a real-world system. I understood how primary keys, foreign keys, unique constraints, indexing, joins, filtering, grouping, and transactions are used to make features actually work. I also learned how the frontend, backend, and database depend on each other in a full-stack project.

This project helped me improve in these areas:

- I learned how to convert a real idea into a relational database design.
- I understood one-to-many and many-to-many relationships through tables like `user_skills`, `job_required_skills`, and `job_applications`.
- I learned how backend APIs connect the database with the frontend and how role-based access works for students, recruiters, and admins.
- I understood how authentication, JWT tokens, password hashing, and protected routes secure a system.
- I learned how premium features, AI resume generation, and real-time messaging still rely on strong database structure and query design.
- I understood how to think like both a DBMS student and a software developer while building one complete system.

In short, SkillConnect helped me move from studying DBMS concepts to applying them in a practical and meaningful product.

## Project Overview
SkillConnect is a full-stack placement and professional networking platform built for students, recruiters, and admins. It allows students to build skill profiles, apply to jobs, upgrade to premium, generate AI-based resumes, and communicate with recruiters. Recruiters can post jobs, search candidates, review applications, and move students through a hiring pipeline. Admins can monitor the entire platform through a centralized dashboard.

## User Roles
- `student`: Register, add skills, browse jobs, apply, upgrade to premium, generate resumes, and chat with recruiters.
- `recruiter`: Register, post jobs, filter candidates, review applications, update status, and message applicants.
- `admin`: Log in and view platform-wide data, counts, and records from multiple tables.

## Core Features
- Secure registration and login using hashed passwords and JWT tokens.
- Role-based route protection in both backend and frontend.
- Student dashboard for profile and skill management.
- Free plan skill limit and premium upgrade workflow.
- Premium AI Resume Creator with OpenAI integration and a fallback generator.
- Recruiter dashboard for posting jobs and managing applications.
- Job board with filtering by skill and company.
- Real-time messaging between student and recruiter using WebSocket.
- Admin dashboard with platform analytics and raw data tables.
- Startup-time schema creation and backward-compatible database migration logic.

## Tech Stack
- Backend: Python, FastAPI, MySQL Connector, Passlib, JWT (`python-jose`)
- Frontend: React 19, Vite, React Router, Axios, CSS
- Database: MySQL
- AI Integration: OpenAI API with local fallback resume generation
- Authentication: OAuth2 password flow + bearer token
- Real-time Communication: WebSocket

## Why This Is a Strong DBMS Project
This project demonstrates DBMS concepts through a real application instead of isolated SQL examples.

- It uses normalized relational tables for major entities.
- It includes one-to-many and many-to-many relationships.
- It applies foreign keys and unique constraints to preserve integrity.
- It uses indexes to support filtering and performance.
- It handles transactional operations like registration, skill insertion, job application, and premium upgrade.
- It shows query-driven features such as filtering jobs, filtering candidates, counting applicants, and generating admin summaries.
- It connects database design directly with user-facing workflows.

## System Architecture
SkillConnect follows a simple three-layer structure:

1. Frontend
   React pages in `skillconnect-frontend/src` handle the UI for students, recruiters, admins, premium access, jobs, and messaging.
2. Backend API
   `main.py` contains FastAPI routes, authentication logic, validation flow, premium checks, AI resume generation, and WebSocket messaging.
3. Database
   MySQL stores users, skills, jobs, applications, premium payments, resumes, and message records.

## Main Workflows
### Student Flow
- Register or log in
- Add skills to profile
- View available jobs
- Apply for jobs
- Track application status
- Upgrade to premium
- Generate ATS-friendly resume
- Message recruiter after application

### Recruiter Flow
- Register or log in
- View recruiter dashboard
- Search candidates by name, skill, and proficiency
- Post new jobs
- View applications per job
- Update application status
- Message applicants

### Admin Flow
- Log in as admin
- View total users, jobs, applications, premium users, and AI resumes
- Inspect data across users, skills, jobs, applications, and resumes

## Database Design
### Core tables used by the running application
- `users`: stores account identity, role, subscription, and timestamps
- `skills`: stores master skill names and categories
- `user_skills`: connects students to skills with proficiency level
- `jobs`: stores recruiter job postings
- `job_required_skills`: maps jobs to required skills
- `job_applications`: stores applications made by students
- `ai_resumes`: stores generated resume history
- `premium_payments`: stores premium membership payment verification data
- `job_application_messages`: stores recruiter-student conversation messages

### Additional tables present in SQL schema files
- `projects`: prepared for user project records
- `certifications`: prepared for certification records

### Important schema note
- `schema_exact.sql` contains the main schema snapshot.
- On backend startup, `main.py` also creates `job_application_messages` and performs safe schema migrations for missing columns, indexes, and foreign keys.
- The backend also backfills `job_required_skills` from older comma-separated job skill data for backward compatibility.

## Relationship Summary
- One user can have many skills through `user_skills`.
- One recruiter can post many jobs.
- One job can require many skills through `job_required_skills`.
- One student can apply to many jobs through `job_applications`.
- One application can have many messages in `job_application_messages`.
- One premium user can generate many resumes stored in `ai_resumes`.

## API Overview
### Common and Auth
- `GET /` - API welcome message
- `GET /health` - health check
- `GET /me` - current authenticated user
- `POST /register` - register student or recruiter
- `POST /login` - login and get JWT token

### Premium and Resume
- `POST /billing/dev-signature` - create development payment signature
- `POST /upgrade-to-premium` - verify and upgrade account
- `POST /ai-resume/generate` - generate premium resume
- `GET /ai-resume/history` - fetch resume history

### Student
- `POST /add-skill` - add a skill with proficiency and category
- `GET /my-skills` - get student skill list
- `GET /jobs` - browse jobs with filters
- `POST /jobs/{job_id}/apply` - apply for a job
- `GET /student/applications` - view own applications

### Messaging
- `GET /messages/threads` - list conversations
- `GET /messages/threads/{application_id}` - open a conversation
- `POST /messages/threads/{application_id}` - send a message
- `POST /messages/threads/{application_id}/read` - mark as read
- `WS /ws/messages` - real-time messaging socket

### Recruiter
- `GET /recruiter/candidates` - search and filter students
- `POST /recruiter/jobs` - create job posting
- `GET /recruiter/jobs` - view recruiter jobs
- `GET /recruiter/jobs/{job_id}/applications` - view applicants for one job
- `PATCH /recruiter/applications/{application_id}/status` - change application status

### Admin
- `GET /admin/overview` - full dashboard summary and data tables

## Business Rules Implemented
- Only `student` and `recruiter` can self-register.
- Free students can add up to 5 skills.
- Premium is required for AI resume generation.
- Only students can apply for jobs.
- Only recruiters and admins can post jobs or manage hiring flow.
- Only student and recruiter members of the same application thread can exchange messages.
- Login attempts are rate-limited in memory for added protection.

## Project Structure
```text
DBMS PROJECT/
|-- main.py
|-- db.py
|-- models.py
|-- schemas.py
|-- schema_exact.sql
|-- remaining_inserts_based_on_current_db.sql
|-- seed_data_20_rows_all_tables copy.sql
|-- package.json
|-- LICENSE
`-- skillconnect-frontend/
    |-- package.json
    |-- vite.config.js
    |-- src/
    |   |-- App.jsx
    |   |-- api/api.js
    |   |-- components/ProtectedRoute.jsx
    |   `-- pages/
    |       |-- AuthPages.jsx
    |       |-- StudentDashboard.jsx
    |       |-- StudentJobsPage.jsx
    |       |-- RecruiterDashboard.jsx
    |       |-- PremiumPage.jsx
    |       |-- MessagesPage.jsx
    |       `-- AdminDashboard.jsx
    `-- public/
```

## Frontend Pages
- `AuthPages.jsx`: login and registration
- `StudentDashboard.jsx`: student home and skill management
- `StudentJobsPage.jsx`: job browsing, filtering, and applications
- `RecruiterDashboard.jsx`: candidate search, job posting, application pipeline
- `PremiumPage.jsx`: premium upgrade and resume generation
- `MessagesPage.jsx`: live recruiter-student chat
- `AdminDashboard.jsx`: full admin analytics and data view

## Backend Files
- `main.py`: complete API logic, auth, premium logic, AI resume generation, WebSocket messaging, and startup migrations
- `db.py`: MySQL configuration, local `.env` reading, and connection pool
- `schemas.py`: request and response validation models
- `models.py`: valid role, status, and subscription constants

## SQL Files
- `schema_exact.sql`: main schema snapshot
- `seed_data_20_rows_all_tables copy.sql`: fresh sample data for a clean database
- `remaining_inserts_based_on_current_db.sql`: extra inserts for a partially filled database

## How to Run the Project
### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8+

### 1. Install backend dependencies
This repository currently does not include a `requirements.txt`, so install the backend packages manually:

```bash
pip install fastapi "uvicorn[standard]" mysql-connector-python passlib[bcrypt] python-jose python-multipart email-validator openai
```

### 2. Create environment file
Create a `.env` or `.env.local` file in the project root:

```env
APP_ENV=development
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=DBMS_project
DB_POOL_SIZE=10
SECRET_KEY=change_this_secret_key
PAYMENT_SIGNING_SECRET=change_this_payment_secret
OPENAI_API_KEY=
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Notes:
- In development mode, some database values have defaults, but defining them explicitly is better.
- If `OPENAI_API_KEY` is not provided, the project still generates a fallback resume format instead of failing.

### 3. Prepare the database
1. Create a MySQL database named `DBMS_project`
2. Import `schema_exact.sql`
3. Import `seed_data_20_rows_all_tables copy.sql` for sample records
4. If your database is already partially filled, use `remaining_inserts_based_on_current_db.sql` only when needed

### 4. Start the backend
From the project root:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 5. Start the frontend
In a new terminal:

```bash
cd skillconnect-frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

### 6. Optional root npm scripts
The root `package.json` contains convenience scripts that forward to the frontend:

```bash
npm run dev
npm run build
npm run lint
npm run preview
```

## Demo Accounts
If you import the seed file, every seeded user uses the same password:

```text
123456
```

Example accounts:

- Admin: `admin@skillconnect.in`
- Recruiter: `aarav.sharma@skillconnect.in`
- Student: `priya.singh@skillconnect.in`

## Current Implementation Notes
- The frontend API base URL is currently hardcoded to `http://127.0.0.1:8000` in `skillconnect-frontend/src/api/api.js`.
- Premium upgrade uses a development signing flow through `/billing/dev-signature`.
- The app supports OpenAI resume generation but safely falls back to a local text generator if no API key is configured.
- `projects` and `certifications` exist in the SQL schema files but are not yet exposed in the current frontend or API routes.

## What This Project Shows About My Understanding
This project shows that I understand:

- database schema design for a real use case
- SQL relationships and constraints
- backend API development with validation and security
- frontend integration with authenticated APIs
- role-based system design
- premium and feature-gating logic
- real-time communication using WebSocket
- how DBMS concepts support a complete software product

## Future Improvements
- Add `requirements.txt` for easier backend setup
- Move frontend API base URL to environment configuration
- Add CRUD for projects and certifications
- Add automated tests for backend and frontend
- Integrate a real payment gateway for production use
- Improve deployment and production configuration

## Author
Tarundeep Singh

## License
This project is licensed under the MIT License. See `LICENSE` for details.
