import { useEffect, useState } from "react";
import API from "../api/api";
import "./auth-page.css";

const REGISTER_ROLES = ["student", "recruiter"];

function redirectByRole(role) {
  if (role === "student") {
    window.location.href = "/student";
  } else if (role === "recruiter") {
    window.location.href = "/recruiter";
  } else if (role === "admin") {
    window.location.href = "/admin";
  } else {
    window.location.href = "/";
  }
}

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedRole = localStorage.getItem("role");
    if (token && storedRole) {
      redirectByRole(storedRole);
    }
  }, []);

  const resetMessages = () => {
    setError("");
    setStatus("");
  };

  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    resetMessages();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    resetMessages();

    if (!email.trim() || !password.trim() || (!isLogin && !name.trim())) {
      setError("Please fill all required fields.");
      return;
    }

    try {
      setLoading(true);

      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", email.trim());
        formData.append("password", password);

        const res = await API.post("/login", formData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        });

        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("role", res.data.role);
        localStorage.setItem("name", res.data.name);
        redirectByRole(res.data.role);
      } else {
        await API.post("/register", {
          name: name.trim(),
          email: email.trim(),
          password,
          role,
        });
        setStatus("Registration successful. Please login.");
        setIsLogin(true);
        setName("");
        setPassword("");
      }
    } catch (err) {
      if (err.response?.status === 401) {
        setError("Invalid credentials.");
      } else {
        setError(err.response?.data?.detail || "Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-bg-orb auth-bg-orb-a" />
      <div className="auth-bg-orb auth-bg-orb-b" />

      <main className="auth-layout">
        <section className="auth-hero">
          <div className="auth-brand-row">
            <div className="auth-logo">SC</div>
            <h1>SkillConnect</h1>
          </div>

          <h2>Build your professional identity and get hired faster.</h2>
          <p>
            Made By Tarundeep Singh ft. Pulkit Madan
          </p>
        </section>

        <section className="auth-card-wrap">
          <form className="auth-card" onSubmit={handleSubmit}>
            <div className="auth-card-head">
              <h3>{isLogin ? "Welcome back" : "Create your account"}</h3>
              <p>{isLogin ? "Login to continue your journey" : "Join SkillConnect today"}</p>
            </div>

            {!isLogin && (
              <label>
                Full Name
                <input
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </label>
            )}

            <label>
              Email
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>

            <label>
              Password
              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>

            {!isLogin && (
              <label>
                Account Type
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                  {REGISTER_ROLES.map((item) => (
                    <option key={item} value={item}>
                      {item.charAt(0).toUpperCase() + item.slice(1)}
                    </option>
                  ))}
                </select>
              </label>
            )}

            {error && <p className="auth-error">{error}</p>}
            {status && <p className="auth-status">{status}</p>}

            <button className="auth-submit" type="submit" disabled={loading}>
              {loading ? "Please wait..." : isLogin ? "Login" : "Register"}
            </button>

            <button className="auth-switch" type="button" onClick={toggleMode}>
              {isLogin ? "New here? Create account" : "Already have an account? Login"}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default AuthPage;
