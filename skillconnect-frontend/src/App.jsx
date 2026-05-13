import { Routes, Route } from "react-router-dom";
import AuthPage from "./pages/AuthPages";
import StudentDashboard from "./pages/StudentDashboard";
import RecruiterDashboard from "./pages/RecruiterDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import PremiumPage from "./pages/PremiumPage";
import StudentJobsPage from "./pages/StudentJobsPage";
import MessagesPage from "./pages/MessagesPage";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthPage />} />

      <Route
        path="/student"
        element={
          <ProtectedRoute allowedRole="student">
            <StudentDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/recruiter"
        element={
          <ProtectedRoute allowedRole="recruiter">
            <RecruiterDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/premium"
        element={
          <ProtectedRoute allowedRole="student">
            <PremiumPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/jobs"
        element={
          <ProtectedRoute allowedRole="student">
            <StudentJobsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/student/messages"
        element={
          <ProtectedRoute allowedRole="student">
            <MessagesPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/recruiter/messages"
        element={
          <ProtectedRoute allowedRole="recruiter">
            <MessagesPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;
