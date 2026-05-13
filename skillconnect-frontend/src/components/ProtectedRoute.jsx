import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, allowedRole }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  // Not logged in
  if (!token) {
    return <Navigate to="/" replace />;
  }

  // Wrong role
  if (role !== allowedRole) {
    return <Navigate to="/" replace />;
  }

  // All good
  return children;
}

export default ProtectedRoute;