import { useState } from "react";
import axios from "axios";

function AdminLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const loginAdmin = async () => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await axios.post(
      "http://127.0.0.1:8000/login",
      formData,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    if (res.data.role !== "admin") {
      alert("Not authorized as admin");
      return;
    }

    localStorage.setItem("token", res.data.access_token);
    localStorage.setItem("role", res.data.role);

    window.location.href = "/admin";
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Admin Login</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={loginAdmin}>Login</button>
    </div>
  );
}

export default AdminLogin;