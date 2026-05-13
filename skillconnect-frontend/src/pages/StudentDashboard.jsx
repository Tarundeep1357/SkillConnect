import { useCallback, useEffect, useState } from "react";
import API from "../api/api";
import "./student-dashboard.css";

const PROFICIENCY_OPTIONS = ["beginner", "intermediate", "advanced", "expert"];

function StudentDashboard() {
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [showSkillForm, setShowSkillForm] = useState(false);
  const [skillName, setSkillName] = useState("");
  const [category, setCategory] = useState("");
  const [proficiency, setProficiency] = useState("beginner");

  const loadDashboard = useCallback(async () => {
    try {
      const [meRes, skillsRes] = await Promise.all([API.get("/me"), API.get("/my-skills")]);
      setProfile(meRes.data);
      setSkills(skillsRes.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load dashboard");
    }
  }, []);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadDashboard();
    }, 0);
    return () => window.clearTimeout(timerId);
  }, [loadDashboard]);

  const addSkill = async () => {
    if (!skillName.trim()) {
      setError("Please enter a skill");
      return;
    }

    try {
      await API.post("/add-skill", {
        skill_name: skillName.trim(),
        category: category.trim() || null,
        proficiency_level: proficiency,
      });
      setSkillName("");
      setCategory("");
      setProficiency("beginner");
      setShowSkillForm(false);
      setStatus("Skill added successfully");
      setError("");
      void loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add skill");
    }
  };

  const openPremium = () => {
    window.location.href = "/premium";
  };

  const openJobs = () => {
    window.location.href = "/jobs";
  };

  const openMessages = () => {
    window.location.href = "/student/messages";
  };

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const displayName = profile?.name || localStorage.getItem("name") || "Student";
  const memberSince = new Date().toLocaleString("en-US", { month: "short", year: "numeric" });
  const simulatedConnections = 0;

  return (
    <div className="student-shell">
      <header className="student-topbar">
        <div className="brand-block">
          <div className="brand-logo">SC</div>
          <div className="brand-text">SkillConnect</div>
        </div>

        <nav className="top-nav">
          <button type="button" className="top-nav-link active">Home</button>
          <button type="button" className="top-nav-link">Network</button>
          <button type="button" className="top-nav-link" onClick={openJobs}>Jobs</button>
          <button type="button" className="top-nav-link" onClick={openMessages}>Messaging</button>
        </nav>

        <div className="top-actions">
          <button className="ghost-btn" onClick={openPremium}>Premium</button>
          <button className="ghost-btn" onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="dashboard-grid">
        <aside className="left-col">
          <section className="profile-card">
            <div className="cover-gradient" />
            <div className="avatar-badge">{displayName.charAt(0).toUpperCase()}</div>
            <h2>{displayName}</h2>
            <p>{profile?.role === "student" ? "Student Professional" : "Professional"}</p>
            <div className="profile-meta">
              <div>
                <span>Connections</span>
                <strong>{simulatedConnections}</strong>
              </div>
              <div>
                <span>Joined</span>
                <strong>{memberSince}</strong>
              </div>
            </div>
          </section>

          <section className="insight-card">
            <h4>Profile viewers</h4>
            <p>Discover who viewed your profile.</p>
            <div className="meter">
              <div className="meter-fill" style={{ width: "46%" }} />
            </div>
            <button className="link-btn">See analytics</button>
          </section>
        </aside>

        <section className="center-col">
          <section className="composer-card">
            <div className="mini-avatar">{displayName.charAt(0).toUpperCase()}</div>
            <div className="composer-input">Start a post, share a project...</div>
          </section>

          <section className="skills-card">
            <div className="skills-head">
              <h3>Skills & Endorsements</h3>
              <button className="outline-btn" onClick={() => setShowSkillForm(!showSkillForm)}>
                + Add Skill
              </button>
            </div>

            {showSkillForm && (
              <div className="skill-form">
                <input
                  placeholder="Skill name"
                  value={skillName}
                  onChange={(e) => setSkillName(e.target.value)}
                />
                <input
                  placeholder="Category (optional)"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                />
                <select value={proficiency} onChange={(e) => setProficiency(e.target.value)}>
                  {PROFICIENCY_OPTIONS.map((level) => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
                <button className="solid-btn" onClick={addSkill}>Save</button>
              </div>
            )}

            {error && <p className="error-text">{error}</p>}
            {status && <p className="status-text">{status}</p>}

            <div className="skill-grid">
              {skills.length === 0 && (
                <div className="empty-card">No skills yet. Add your first skill.</div>
              )}
              {skills.map((item) => (
                <article key={item.id} className="skill-pill-card">
                  <h4>{item.name}</h4>
                  <p>
                    <span>{item.proficiency_level}</span>
                    {item.category ? ` - ${item.category}` : ""}
                  </p>
                </article>
              ))}
            </div>
          </section>

          <section className="activity-card">
            <h3>No recent activity</h3>
            <p>When you post or comment, it will show up here.</p>
          </section>
        </section>

        <aside className="right-col">
          <section className="feed-card">
            <h3>Add to your feed</h3>
            <div className="feed-item">
              <div className="feed-avatar" />
              <div>
                <strong>Tech Corp Inc.</strong>
                <p>Hiring software engineers. Apply today to build the future.</p>
                <button>Follow</button>
              </div>
            </div>
            <div className="feed-item">
              <div className="feed-avatar" />
              <div>
                <strong>DataVerse Labs</strong>
                <p>Internships open for backend and data roles.</p>
                <button>Follow</button>
              </div>
            </div>
          </section>

          <section className="premium-card">
            <h3>Premium AI Resume Creator</h3>
            <p>
              Build ATS-friendly resumes instantly with AI. Available for premium members.
            </p>
            <button className="solid-btn premium-btn" onClick={openPremium}>Open Premium</button>
          </section>
        </aside>
      </main>
    </div>
  );
}

export default StudentDashboard;


