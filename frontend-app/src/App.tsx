import { Link, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import BillingPage from "./pages/BillingPage";
import DashboardPage from "./pages/DashboardPage";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import OnboardingPage from "./pages/OnboardingPage";
import SettingsPage from "./pages/SettingsPage";
import SignupPage from "./pages/SignupPage";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="loading-spinner">Loading...</div>;
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  const { isAuthenticated, profile, logout, loading } = useAuth();

  // Landing page gets its own full-width layout (no topbar)
  const isLandingRoute =
    typeof window !== "undefined" && window.location.pathname === "/";

  if (!loading && !isAuthenticated && isLandingRoute) {
    return (
      <Routes>
        <Route path="/" element={<LandingPage />} />
      </Routes>
    );
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to={isAuthenticated ? "/dashboard" : "/"} className="topbar-brand">
          <h1>Sentinel Forge</h1>
        </Link>
        <nav>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/billing">Billing</Link>
              <Link to="/settings">Settings</Link>
              <button type="button" onClick={logout} className="link-button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Sign Up</Link>
            </>
          )}
        </nav>
      </header>

      {profile ? (
        <p className="session-banner">Signed in as {profile.email}</p>
      ) : null}

      <main>
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <LandingPage />
              )
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/onboarding"
            element={
              <ProtectedRoute>
                <OnboardingPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/billing"
            element={
              <ProtectedRoute>
                <BillingPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="*"
            element={
              <section className="panel">
                <h2>Not Found</h2>
                <p>
                  The page you're looking for doesn't exist.{" "}
                  <Link to="/">Go home</Link>
                </p>
              </section>
            }
          />
        </Routes>
      </main>
    </div>
  );
}
