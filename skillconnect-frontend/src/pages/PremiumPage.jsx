import { useEffect, useState } from "react";
import API from "../api/api";
import "./premium-page.css";

const DEFAULT_FORM = {
  full_name: "",
  target_role: "Software Engineer",
  years_experience: 0,
  skills_text: "",
  education: "",
  achievements_text: "",
};

function toCommaList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function toLineList(value) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function buildPaymentReference() {
  const randomPart = Math.random().toString(36).slice(2, 10);
  return `dev-${Date.now()}-${randomPart}`;
}

function PremiumPage() {
  const [profile, setProfile] = useState(null);
  const [history, setHistory] = useState([]);
  const [form, setForm] = useState(DEFAULT_FORM);
  const [resumeText, setResumeText] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [upgrading, setUpgrading] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const meRes = await API.get("/me");
      setProfile(meRes.data);
      setForm((prev) => ({
        ...prev,
        full_name: prev.full_name || meRes.data.name || "",
      }));

      if (meRes.data.subscription_type === "premium") {
        const historyRes = await API.get("/ai-resume/history");
        setHistory(historyRes.data);
      } else {
        setHistory([]);
      }
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load premium page");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const updateField = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const goDashboard = () => {
    window.location.href = "/student";
  };

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const upgradeMembership = async () => {
    try {
      setUpgrading(true);
      const provider = "devpay";
      const payment_reference = buildPaymentReference();

      const signatureRes = await API.post("/billing/dev-signature", {
        provider,
        payment_reference,
      });

      await API.post("/upgrade-to-premium", {
        provider,
        payment_reference,
        payment_signature: signatureRes.data.payment_signature,
        amount_cents: 99900,
        currency: "INR",
      });

      setStatus("Premium activated. AI Resume Creator is unlocked.");
      setError("");
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to upgrade membership");
    } finally {
      setUpgrading(false);
    }
  };

  const generateResume = async () => {
    if (!profile || profile.subscription_type !== "premium") {
      setError("Please upgrade to premium to use the AI Resume Creator");
      return;
    }

    if (!form.full_name.trim() || !form.target_role.trim() || !form.education.trim()) {
      setError("Please fill full name, target role, and education");
      return;
    }

    try {
      setGenerating(true);
      const payload = {
        full_name: form.full_name.trim(),
        target_role: form.target_role.trim(),
        years_experience: Number(form.years_experience) || 0,
        skills: toCommaList(form.skills_text),
        education: form.education.trim(),
        achievements: toLineList(form.achievements_text),
      };

      const res = await API.post("/ai-resume/generate", payload);
      setResumeText(res.data.resume_text);
      setStatus("Resume generated successfully.");
      setError("");

      const historyRes = await API.get("/ai-resume/history");
      setHistory(historyRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate resume");
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return <div className="premium-shell loading-state">Loading premium workspace...</div>;
  }

  return (
    <div className="premium-shell">
      <header className="premium-topbar">
        <div>
          <h1>Premium Studio</h1>
          <p>AI Resume Creator + membership controls</p>
        </div>
        <div className="premium-top-actions">
          <button className="subtle-btn" onClick={goDashboard}>Back to Dashboard</button>
          <button className="subtle-btn" onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="premium-grid">
        <section className="membership-card">
          <h2>Membership</h2>
          <p>Current plan: <strong>{profile?.subscription_type || "free"}</strong></p>
          {profile?.subscription_type !== "premium" ? (
            <button className="primary-btn" onClick={upgradeMembership} disabled={upgrading}>
              {upgrading ? "Upgrading..." : "Upgrade to Premium"}
            </button>
          ) : (
            <div className="active-badge">Premium Active</div>
          )}
          <small>Premium members get AI resume generation and history tracking.</small>
        </section>

        <section className="generator-card">
          <h2>AI Resume Creator</h2>

          <div className="input-grid">
            <label>
              Full Name
              <input
                value={form.full_name}
                onChange={(e) => updateField("full_name", e.target.value)}
              />
            </label>

            <label>
              Target Role
              <input
                value={form.target_role}
                onChange={(e) => updateField("target_role", e.target.value)}
              />
            </label>

            <label>
              Years Experience
              <input
                type="number"
                min="0"
                max="50"
                value={form.years_experience}
                onChange={(e) => updateField("years_experience", e.target.value)}
              />
            </label>

            <label>
              Skills (comma-separated)
              <input
                value={form.skills_text}
                onChange={(e) => updateField("skills_text", e.target.value)}
                placeholder="Python, FastAPI, MySQL"
              />
            </label>

            <label className="full-width">
              Education
              <input
                value={form.education}
                onChange={(e) => updateField("education", e.target.value)}
                placeholder="B.Tech CSE, XYZ Institute, 2026"
              />
            </label>

            <label className="full-width">
              Achievements (one per line)
              <textarea
                rows="4"
                value={form.achievements_text}
                onChange={(e) => updateField("achievements_text", e.target.value)}
                placeholder={"Built placement portal used by 400+ students\nReduced API latency by 35%"}
              />
            </label>
          </div>

          <button className="primary-btn" onClick={generateResume} disabled={generating}>
            {generating ? "Generating..." : "Generate Resume"}
          </button>
        </section>

        <section className="output-card">
          <h2>Generated Resume</h2>
          {resumeText ? (
            <pre>{resumeText}</pre>
          ) : (
            <p className="muted">Your generated resume will appear here.</p>
          )}
        </section>

        <section className="history-card">
          <h2>Recent Resume History</h2>
          {history.length === 0 && <p className="muted">No generated resumes yet.</p>}
          {history.map((item) => (
            <details key={item.id} className="history-item">
              <summary>
                {item.target_role} • {item.created_at ? new Date(item.created_at).toLocaleString() : "recent"}
              </summary>
              <pre>{item.resume_text}</pre>
            </details>
          ))}
        </section>
      </main>

      {error && <div className="floating-error">{error}</div>}
      {status && <div className="floating-status">{status}</div>}
    </div>
  );
}

export default PremiumPage;
