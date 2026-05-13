import { Link } from "react-router-dom";
import "../index.css";

function Navbar() {
  return (
    <div className="navbar">
      <div className="nav-logo">
        Skill<span>Connect</span>
      </div>

      <div className="nav-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/premium">Premium</Link>
        <Link to="/">Logout</Link>
      </div>
    </div>
  );
}

export default Navbar;