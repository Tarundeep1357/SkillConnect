import { useCallback, useEffect, useMemo, useState } from "react";
import API from "../api/api";
import "./recruiter-dashboard.css";

const PROFICIENCY_OPTIONS = ["all", "beginner", "intermediate", "advanced", "expert"];
const EMPLOYMENT_TYPES = ["full-time", "part-time", "internship", "contract"];
const APPLICATION_STATUS_OPTIONS = ["applied", "shortlisted", "interview", "hired", "rejected"];
const EMPTY_JOB_FORM = {
  title: "",
  company_name: "",
  location: "Remote",
  employment_type: "full-time",
  salary_range: "",
  required_skills_text: "",
  description: "",
};

function parseSkills(text) {
  return text
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

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

function RecruiterDashboard() {
  const [profile, setProfile] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [recruiterJobs, setRecruiterJobs] = useState([]);
  const [applicationsByJob, setApplicationsByJob] = useState({});
  const [openApplicationsJobId, setOpenApplicationsJobId] = useState(null);
  const [applicationStatusDrafts, setApplicationStatusDrafts] = useState({});
  const [statusUpdateLoading, setStatusUpdateLoading] = useState({});

  const [skillQuery, setSkillQuery] = useState("");
  const [nameQuery, setNameQuery] = useState("");
  const [proficiency, setProficiency] = useState("all");
  const [jobForm, setJobForm] = useState(EMPTY_JOB_FORM);

  const [loading, setLoading] = useState(false);
  const [jobLoading, setJobLoading] = useState(false);
  const [error, setError] = useState("");
  const [jobStatus, setJobStatus] = useState("");
  const [pipelineStatus, setPipelineStatus] = useState("");

  const totalCandidates = useMemo(() => candidates.length, [candidates]);
  const premiumCandidates = useMemo(
    () => candidates.filter((item) => item.subscription_type === "premium").length,
    [candidates]
  );

  const totalApplications = useMemo(
    () => recruiterJobs.reduce((acc, item) => acc + Number(item.applicant_count || 0), 0),
    [recruiterJobs]
  );

  const loadRecruiterData = useCallback(async ({ skill = "", name = "", proficiencyLevel = "all" } = {}) => {
    try {
      setLoading(true);
      const candidateParams = {
        limit: 50,
      };
      if (skill.trim()) {
        candidateParams.skill = skill.trim();
      }
      if (name.trim()) {
        candidateParams.name = name.trim();
      }
      if (proficiencyLevel !== "all") {
        candidateParams.proficiency = proficiencyLevel;
      }

      const [meRes, candidateRes, jobsRes] = await Promise.all([
        API.get("/me"),
        API.get("/recruiter/candidates", { params: candidateParams }),
        API.get("/recruiter/jobs"),
      ]);

      setProfile(meRes.data);
      setCandidates(candidateRes.data);
      setRecruiterJobs(jobsRes.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load recruiter workspace");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadRecruiterData();
  }, [loadRecruiterData]);

  const onSearchCandidates = (e) => {
    e.preventDefault();
    void loadRecruiterData({
      skill: skillQuery,
      name: nameQuery,
      proficiencyLevel: proficiency,
    });
  };

  const clearCandidateFilters = () => {
    setSkillQuery("");
    setNameQuery("");
    setProficiency("all");
    void loadRecruiterData();
  };

  const updateJobField = (field, value) => {
    setJobForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const postJob = async (e) => {
    e.preventDefault();

    if (!jobForm.title.trim() || !jobForm.company_name.trim() || !jobForm.description.trim()) {
      setError("Title, company, and description are required to post a job");
      return;
    }

    if (jobForm.description.trim().length < 20) {
      setError("Description should be at least 20 characters");
      return;
    }

    try {
      setJobLoading(true);
      await API.post("/recruiter/jobs", {
        title: jobForm.title.trim(),
        company_name: jobForm.company_name.trim(),
        location: jobForm.location.trim() || "Remote",
        employment_type: jobForm.employment_type,
        description: jobForm.description.trim(),
        required_skills: parseSkills(jobForm.required_skills_text),
        salary_range: jobForm.salary_range.trim() || null,
      });
      setJobForm(EMPTY_JOB_FORM);
      setJobStatus("Job posted successfully");
      setError("");
      void loadRecruiterData({
        skill: skillQuery,
        name: nameQuery,
        proficiencyLevel: proficiency,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to post job");
    } finally {
      setJobLoading(false);
    }
  };

  const toggleApplications = async (jobId) => {
    if (openApplicationsJobId === jobId) {
      setOpenApplicationsJobId(null);
      return;
    }

    setOpenApplicationsJobId(jobId);
    if (applicationsByJob[jobId]) {
      return;
    }

    try {
      const res = await API.get(`/recruiter/jobs/${jobId}/applications`);
      setApplicationsByJob((prev) => ({
        ...prev,
        [jobId]: res.data,
      }));
      setApplicationStatusDrafts((prev) => {
        const nextDrafts = { ...prev };
        res.data.forEach((application) => {
          nextDrafts[application.id] = application.status;
        });
        return nextDrafts;
      });
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load applications");
    }
  };

  const updateApplicationStatusDraft = (applicationId, value) => {
    setApplicationStatusDrafts((prev) => ({
      ...prev,
      [applicationId]: value,
    }));
  };

  const updateApplicationStatus = async (jobId, application) => {
    const nextStatus = applicationStatusDrafts[application.id] || application.status;
    if (nextStatus === application.status) {
      return;
    }

    try {
      setStatusUpdateLoading((prev) => ({
        ...prev,
        [application.id]: true,
      }));

      await API.patch(`/recruiter/applications/${application.id}/status`, {
        status: nextStatus,
      });

      const updatedAt = new Date().toISOString();
      setApplicationsByJob((prev) => ({
        ...prev,
        [jobId]: (prev[jobId] || []).map((item) =>
          item.id === application.id
            ? {
                ...item,
                status: nextStatus,
                updated_at: updatedAt,
              }
            : item
        ),
      }));
      setPipelineStatus(
        `${application.student_name} moved to ${formatStatusLabel(nextStatus)}`
      );
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update application status");
    } finally {
      setStatusUpdateLoading((prev) => ({
        ...prev,
        [application.id]: false,
      }));
    }
  };

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const openMessages = (applicationId = null) => {
    const suffix = applicationId ? `?applicationId=${applicationId}` : "";
    window.location.href = `/recruiter/messages${suffix}`;
  };

  return (
    <div className="recruiter-shell">
      <header className="recruiter-topbar">
        <div className="recruiter-brand">
          <div className="recruiter-logo">SC</div>
          <div>
            <h1>Recruiter Console</h1>
            <p>Post jobs, review applications, and move candidates through the pipeline</p>
          </div>
        </div>
        <div className="recruiter-actions">
          <button
            onClick={() =>
              void loadRecruiterData({
                skill: skillQuery,
                name: nameQuery,
                proficiencyLevel: proficiency,
              })
            }
          >
            Refresh
          </button>
          <button onClick={() => openMessages()}>Messages</button>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="recruiter-grid">
        <aside className="recruiter-left">
          <section className="recruiter-profile-card">
            <div className="avatar">{(profile?.name || "R").charAt(0).toUpperCase()}</div>
            <h3>{profile?.name || "Recruiter"}</h3>
            <p>{profile?.email || ""}</p>
            <span className="role-pill">{profile?.role || "recruiter"}</span>
          </section>

          <section className="stats-card">
            <h4>Pipeline Snapshot</h4>
            <article>
              <span>Total Candidates</span>
              <strong>{totalCandidates}</strong>
            </article>
            <article>
              <span>Premium Students</span>
              <strong>{premiumCandidates}</strong>
            </article>
            <article>
              <span>Posted Jobs</span>
              <strong>{recruiterJobs.length}</strong>
            </article>
            <article>
              <span>Total Applications</span>
              <strong>{totalApplications}</strong>
            </article>
          </section>
        </aside>

        <section className="recruiter-main">
          <section className="job-post-card">
            <h2>Post a New Job</h2>
            <form onSubmit={postJob} className="job-post-form">
              <input
                placeholder="Job title"
                value={jobForm.title}
                onChange={(e) => updateJobField("title", e.target.value)}
              />
              <input
                placeholder="Company name"
                value={jobForm.company_name}
                onChange={(e) => updateJobField("company_name", e.target.value)}
              />
              <input
                placeholder="Location"
                value={jobForm.location}
                onChange={(e) => updateJobField("location", e.target.value)}
              />
              <select
                value={jobForm.employment_type}
                onChange={(e) => updateJobField("employment_type", e.target.value)}
              >
                {EMPLOYMENT_TYPES.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
              <input
                placeholder="Salary range (optional)"
                value={jobForm.salary_range}
                onChange={(e) => updateJobField("salary_range", e.target.value)}
              />
              <input
                placeholder="Required skills (comma-separated)"
                value={jobForm.required_skills_text}
                onChange={(e) => updateJobField("required_skills_text", e.target.value)}
              />
              <textarea
                placeholder="Job description"
                rows="3"
                value={jobForm.description}
                onChange={(e) => updateJobField("description", e.target.value)}
              />
              <button type="submit" className="primary-btn" disabled={jobLoading}>
                {jobLoading ? "Posting..." : "Post Job"}
              </button>
            </form>
            {jobStatus && <p className="success-banner">{jobStatus}</p>}
          </section>

          <section className="posted-jobs-card">
            <div className="candidates-head">
              <h2>Posted Jobs</h2>
              <span>{recruiterJobs.length} job(s)</span>
            </div>

            {recruiterJobs.length === 0 && (
              <div className="empty-state">No jobs posted yet.</div>
            )}

            <div className="posted-jobs-list">
              {recruiterJobs.map((job) => (
                <article key={job.id} className="posted-job-item">
                  <div className="posted-job-head">
                    <div>
                      <h3>{job.title}</h3>
                      <p>{job.company_name} • {job.location}</p>
                    </div>
                    <span>{job.applicant_count} applicant(s)</span>
                  </div>
                  <p className="job-snippet">{job.description}</p>
                  <div className="skills-list">
                    {job.required_skills.length === 0 && (
                      <span className="skill-chip muted-chip">No required skills listed</span>
                    )}
                    {job.required_skills.map((skill, index) => (
                      <span key={`${job.id}-${skill}-${index}`} className="skill-chip">
                        {skill}
                      </span>
                    ))}
                  </div>
                  <div className="candidate-actions">
                    <button className="ghost-btn" onClick={() => toggleApplications(job.id)}>
                      {openApplicationsJobId === job.id ? "Hide Applications" : "View Applications"}
                    </button>
                  </div>

                  {openApplicationsJobId === job.id && (
                    <div className="applications-list">
                      {!applicationsByJob[job.id] && <p>Loading applications...</p>}
                      {applicationsByJob[job.id] && applicationsByJob[job.id].length === 0 && (
                        <p>No applications yet.</p>
                      )}
                      {applicationsByJob[job.id]?.map((application) => (
                        <div key={application.id} className="application-item">
                          <div className="application-item-head">
                            <div>
                              <strong>{application.student_name}</strong>
                              <span>{application.student_email}</span>
                            </div>
                            <span className={`application-status-pill status-${application.status}`}>
                              {formatStatusLabel(application.status)}
                            </span>
                          </div>
                          <div className="application-meta-row">
                            <span>Applied {formatDateTime(application.created_at)}</span>
                            <span>Last updated {formatDateTime(application.updated_at || application.created_at)}</span>
                          </div>
                          {application.cover_letter && (
                            <p>{application.cover_letter}</p>
                          )}
                          <div className="application-controls">
                            <label htmlFor={`application-status-${application.id}`}>Pipeline stage</label>
                            <div className="application-controls-row">
                              <select
                                id={`application-status-${application.id}`}
                                value={applicationStatusDrafts[application.id] || application.status}
                                onChange={(e) => updateApplicationStatusDraft(application.id, e.target.value)}
                                disabled={statusUpdateLoading[application.id]}
                              >
                                {APPLICATION_STATUS_OPTIONS.map((option) => (
                                  <option key={option} value={option}>
                                    {formatStatusLabel(option)}
                                  </option>
                                ))}
                              </select>
                              <button
                                type="button"
                                className="primary-btn"
                                onClick={() => updateApplicationStatus(job.id, application)}
                                disabled={
                                  statusUpdateLoading[application.id]
                                  || (applicationStatusDrafts[application.id] || application.status) === application.status
                                }
                              >
                                {statusUpdateLoading[application.id] ? "Saving..." : "Save Status"}
                              </button>
                              <button
                                type="button"
                                className="ghost-btn message-action-btn"
                                onClick={() => openMessages(application.id)}
                              >
                                Message Candidate
                              </button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>

          <section className="search-card">
            <h2>Search Candidates</h2>
            <form onSubmit={onSearchCandidates} className="search-form">
              <input
                placeholder="Filter by skill (e.g. python)"
                value={skillQuery}
                onChange={(e) => setSkillQuery(e.target.value)}
              />
              <input
                placeholder="Filter by student name"
                value={nameQuery}
                onChange={(e) => setNameQuery(e.target.value)}
              />
              <select value={proficiency} onChange={(e) => setProficiency(e.target.value)}>
                {PROFICIENCY_OPTIONS.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
              <button type="submit" className="primary-btn">Apply</button>
              <button type="button" className="ghost-btn" onClick={clearCandidateFilters}>
                Clear
              </button>
            </form>
          </section>

          {error && <p className="error-banner">{error}</p>}
          {pipelineStatus && <p className="success-banner">{pipelineStatus}</p>}
          {loading && <p className="loading-banner">Loading recruiter data...</p>}

          <section className="candidates-card">
            <div className="candidates-head">
              <h2>Candidate List</h2>
              <span>{totalCandidates} result(s)</span>
            </div>

            <div className="candidate-grid">
              {!loading && candidates.length === 0 && (
                <div className="empty-state">
                  No candidates found for current filters.
                </div>
              )}

              {candidates.map((candidate) => (
                <article key={candidate.id} className="candidate-card">
                  <div className="candidate-head">
                    <div className="candidate-avatar">
                      {candidate.name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <h3>{candidate.name}</h3>
                      <p>{candidate.email}</p>
                    </div>
                  </div>

                  <div className="candidate-meta">
                    <span>{candidate.total_skills} skills</span>
                    <span className={candidate.subscription_type === "premium" ? "premium" : "free"}>
                      {candidate.subscription_type}
                    </span>
                  </div>

                  <div className="skills-list">
                    {candidate.skills.length === 0 && (
                      <span className="skill-chip muted-chip">No skills added</span>
                    )}
                    {candidate.skills.map((item, idx) => (
                      <span key={`${candidate.id}-${item.name}-${idx}`} className="skill-chip">
                        {item.name} ({item.proficiency_level})
                      </span>
                    ))}
                  </div>

                  <div className="candidate-actions">
                    <button
                      onClick={() => window.open(`mailto:${candidate.email}`, "_blank")}
                      className="primary-btn"
                    >
                      Contact
                    </button>
                  </div>
                  <p className="candidate-hint">
                    Shortlist candidates from the job application pipeline after they apply.
                  </p>
                </article>
              ))}
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}

export default RecruiterDashboard;
