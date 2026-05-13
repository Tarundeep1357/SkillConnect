import { useCallback, useEffect, useMemo, useState } from "react";
import API from "../api/api";
import "./student-jobs-page.css";

function formatStatusLabel(status) {
  if (!status) {
    return "Unknown";
  }

  return status.charAt(0).toUpperCase() + status.slice(1);
}

function formatDateTime(value) {
  if (!value) {
    return "Just now";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Just now";
  }

  return date.toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function StudentJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [coverLetters, setCoverLetters] = useState({});
  const [skillFilter, setSkillFilter] = useState("");
  const [companyFilter, setCompanyFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  const loadData = useCallback(async ({ skill = "", company = "" } = {}) => {
    try {
      setLoading(true);
      const jobsPromise = API.get("/jobs", {
        params: {
          skill: skill.trim() || undefined,
          company: company.trim() || undefined,
          limit: 60,
        },
      });
      const appsPromise = API.get("/student/applications");
      const [jobsRes, appsRes] = await Promise.all([jobsPromise, appsPromise]);
      setJobs(jobsRes.data);
      setApplications(appsRes.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load jobs");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const applicationsByJobId = useMemo(
    () =>
      applications.reduce((acc, application) => {
        acc[application.job_id] = application;
        return acc;
      }, {}),
    [applications]
  );

  const applyFilters = (e) => {
    e.preventDefault();
    void loadData({
      skill: skillFilter,
      company: companyFilter,
    });
  };

  const clearFilters = () => {
    setSkillFilter("");
    setCompanyFilter("");
    void loadData();
  };

  const updateCoverLetter = (jobId, value) => {
    setCoverLetters((prev) => ({
      ...prev,
      [jobId]: value,
    }));
  };

  const applyToJob = async (jobId) => {
    try {
      await API.post(`/jobs/${jobId}/apply`, {
        cover_letter: coverLetters[jobId]?.trim() || null,
      });
      setStatus("Application submitted successfully");
      setError("");
      setCoverLetters((prev) => ({ ...prev, [jobId]: "" }));
      void loadData({
        skill: skillFilter,
        company: companyFilter,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to apply for job");
    }
  };

  const goDashboard = () => {
    window.location.href = "/student";
  };

  const openMessages = (applicationId = null) => {
    const suffix = applicationId ? `?applicationId=${applicationId}` : "";
    window.location.href = `/student/messages${suffix}`;
  };

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <div className="student-jobs-shell">
      <header className="student-jobs-topbar">
        <div>
          <h1>Job Board</h1>
          <p>Apply to opportunities posted by recruiters</p>
        </div>
        <div className="jobs-top-actions">
          <button onClick={goDashboard}>Back to Home</button>
          <button onClick={() => openMessages()}>Messages</button>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="student-jobs-main">
        <section className="filters-card">
          <h2>Search Jobs</h2>
          <form onSubmit={applyFilters} className="jobs-filter-form">
            <input
              value={skillFilter}
              onChange={(e) => setSkillFilter(e.target.value)}
              placeholder="Filter by skill (e.g. React, Python)"
            />
            <input
              value={companyFilter}
              onChange={(e) => setCompanyFilter(e.target.value)}
              placeholder="Filter by company"
            />
            <button type="submit" className="primary-btn">Apply</button>
            <button type="button" className="ghost-btn" onClick={clearFilters}>
              Clear
            </button>
          </form>
        </section>

        {error && <div className="jobs-error">{error}</div>}
        {status && <div className="jobs-status">{status}</div>}
        {loading && <div className="jobs-loading">Loading jobs...</div>}

        <section className="jobs-grid">
          {jobs.length === 0 && !loading && (
            <div className="jobs-empty">No jobs found with current filters.</div>
          )}

          {jobs.map((job) => {
            const relatedApplication = applicationsByJobId[job.id];

            return (
              <article key={job.id} className="job-card">
                <div className="job-card-head">
                  <div>
                    <h3>{job.title}</h3>
                    <p>{job.company_name} - {job.location}</p>
                  </div>
                  <span className="job-type">{job.employment_type}</span>
                </div>

                <p className="job-description">{job.description}</p>

                <div className="job-meta">
                  <span>Recruiter: {job.recruiter_name}</span>
                  <span>Applicants: {job.applicant_count}</span>
                  {job.salary_range && <span>Salary: {job.salary_range}</span>}
                </div>

                {relatedApplication && (
                  <div className="job-application-status">
                    <span className={`application-status-pill status-${relatedApplication.status}`}>
                      {formatStatusLabel(relatedApplication.status)}
                    </span>
                    <span>
                      Updated {formatDateTime(relatedApplication.updated_at || relatedApplication.created_at)}
                    </span>
                  </div>
                )}

                <div className="skills-row">
                  {job.required_skills.length === 0 && (
                    <span className="skill-chip muted">No skill requirements listed</span>
                  )}
                  {job.required_skills.map((skill, index) => (
                    <span key={`${job.id}-${skill}-${index}`} className="skill-chip">
                      {skill}
                    </span>
                  ))}
                </div>

                <textarea
                  rows="3"
                  value={coverLetters[job.id] || ""}
                  onChange={(e) => updateCoverLetter(job.id, e.target.value)}
                  placeholder={job.already_applied ? "Application already submitted" : "Optional cover letter"}
                  disabled={job.already_applied}
                />

                <div className="job-actions">
                  <button
                    className="primary-btn"
                    onClick={() => applyToJob(job.id)}
                    disabled={job.already_applied}
                  >
                    {relatedApplication
                      ? `Status: ${formatStatusLabel(relatedApplication.status)}`
                      : "Apply Now"}
                  </button>
                </div>
              </article>
            );
          })}
        </section>

        <section className="applications-card">
          <h2>My Applications</h2>
          {applications.length === 0 && <p className="muted">You have not applied yet.</p>}
          {applications.map((item) => (
            <div key={item.id} className="application-row">
              <div className="application-copy">
                <div className="application-copy-head">
                  <strong>{item.title}</strong>
                  <span className={`application-status-pill status-${item.status}`}>
                    {formatStatusLabel(item.status)}
                  </span>
                </div>
                <span>{item.company_name}</span>
                <span>Applied {formatDateTime(item.created_at)}</span>
                <span>Last updated {formatDateTime(item.updated_at || item.created_at)}</span>
              </div>
              <button
                type="button"
                className="ghost-btn"
                onClick={() => openMessages(item.id)}
              >
                Message Recruiter
              </button>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}

export default StudentJobsPage;
