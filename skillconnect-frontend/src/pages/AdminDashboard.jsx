import { useEffect, useMemo, useState } from "react";
import API from "../api/api";
import "./admin-dashboard.css";

const EMPTY_DASHBOARD = {
  summary: {
    total_users: 0,
    students: 0,
    recruiters: 0,
    admins: 0,
    premium_users: 0,
    total_skills: 0,
    total_jobs: 0,
    active_jobs: 0,
    total_applications: 0,
    total_ai_resumes: 0,
  },
  users: [],
  user_skills: [],
  jobs: [],
  applications: [],
  ai_resumes: [],
};

function toDisplayDate(value) {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return date.toLocaleString();
}

function toDisplayValue(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return String(value);
}

function shortenText(text, maxLength = 100) {
  const source = text || "";
  if (source.length <= maxLength) {
    return source || "-";
  }
  return `${source.slice(0, maxLength)}...`;
}

function DataTable({ title, rows, columns, emptyMessage }) {
  return (
    <section className="admin-section">
      <h2>
        {title} <span>({rows.length})</span>
      </h2>
      <div className="admin-table-wrap">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column.key}>{column.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan={columns.length}>{emptyMessage}</td>
              </tr>
            ) : (
              rows.map((row, rowIndex) => (
                <tr key={row.id ?? `${title}-${rowIndex}`}>
                  {columns.map((column) => (
                    <td key={`${column.key}-${rowIndex}`}>
                      {column.render ? column.render(row) : toDisplayValue(row[column.key])}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function AdminDashboard() {
  const [dashboard, setDashboard] = useState(EMPTY_DASHBOARD);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await API.get("/admin/overview");
      setDashboard({
        ...EMPTY_DASHBOARD,
        ...res.data,
      });
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load admin dashboard");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const summaryCards = useMemo(
    () => [
      { label: "Total Users", value: dashboard.summary.total_users },
      { label: "Students", value: dashboard.summary.students },
      { label: "Recruiters", value: dashboard.summary.recruiters },
      { label: "Admins", value: dashboard.summary.admins },
      { label: "Premium Users", value: dashboard.summary.premium_users },
      { label: "Skills Added", value: dashboard.summary.total_skills },
      { label: "Total Jobs", value: dashboard.summary.total_jobs },
      { label: "Active Jobs", value: dashboard.summary.active_jobs },
      { label: "Applications", value: dashboard.summary.total_applications },
      { label: "AI Resumes", value: dashboard.summary.total_ai_resumes },
    ],
    [dashboard.summary]
  );

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <div className="admin-shell">
      <header className="admin-topbar">
        <div>
          <h1>Admin Dashboard</h1>
          <p>Access all platform accounts and data in one place</p>
        </div>
        <div className="admin-actions">
          <button onClick={loadDashboard} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh"}
          </button>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      {error && <p className="admin-error">{error}</p>}
      {loading && <p className="admin-message">Loading latest admin data...</p>}

      <section className="admin-summary-grid">
        {summaryCards.map((item) => (
          <article key={item.label} className="admin-summary-card">
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </article>
        ))}
      </section>

      <DataTable
        title="Users"
        rows={dashboard.users}
        emptyMessage="No users found"
        columns={[
          { key: "id", label: "ID" },
          { key: "name", label: "Name" },
          { key: "email", label: "Email" },
          { key: "role", label: "Role" },
          { key: "subscription_type", label: "Subscription" },
        ]}
      />

      <DataTable
        title="User Skills"
        rows={dashboard.user_skills}
        emptyMessage="No skills found"
        columns={[
          { key: "user_id", label: "User ID" },
          { key: "user_name", label: "User Name" },
          { key: "user_email", label: "User Email" },
          { key: "skill_id", label: "Skill ID" },
          { key: "skill_name", label: "Skill Name" },
          { key: "category", label: "Category" },
          { key: "proficiency_level", label: "Proficiency" },
        ]}
      />

      <DataTable
        title="Jobs"
        rows={dashboard.jobs}
        emptyMessage="No jobs found"
        columns={[
          { key: "id", label: "Job ID" },
          { key: "title", label: "Title" },
          { key: "company_name", label: "Company" },
          { key: "recruiter_name", label: "Recruiter" },
          { key: "location", label: "Location" },
          { key: "employment_type", label: "Type" },
          { key: "salary_range", label: "Salary" },
          { key: "is_active", label: "Active", render: (row) => (row.is_active ? "Yes" : "No") },
          { key: "applicant_count", label: "Applicants" },
          { key: "created_at", label: "Created", render: (row) => toDisplayDate(row.created_at) },
        ]}
      />

      <DataTable
        title="Applications"
        rows={dashboard.applications}
        emptyMessage="No applications found"
        columns={[
          { key: "id", label: "Application ID" },
          { key: "job_id", label: "Job ID" },
          { key: "job_title", label: "Job Title" },
          { key: "student_id", label: "Student ID" },
          { key: "student_name", label: "Student Name" },
          { key: "student_email", label: "Student Email" },
          { key: "status", label: "Status" },
          { key: "cover_letter", label: "Cover Letter", render: (row) => shortenText(row.cover_letter) },
          { key: "created_at", label: "Created", render: (row) => toDisplayDate(row.created_at) },
        ]}
      />

      <DataTable
        title="AI Resume History"
        rows={dashboard.ai_resumes}
        emptyMessage="No AI resumes found"
        columns={[
          { key: "id", label: "Resume ID" },
          { key: "user_id", label: "User ID" },
          { key: "user_name", label: "User Name" },
          { key: "user_email", label: "User Email" },
          { key: "target_role", label: "Target Role" },
          { key: "resume_preview", label: "Preview", render: (row) => shortenText(row.resume_preview, 120) },
          { key: "created_at", label: "Created", render: (row) => toDisplayDate(row.created_at) },
        ]}
      />
    </div>
  );
}

export default AdminDashboard;

