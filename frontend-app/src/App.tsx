import { Link, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import BillingPage from "./pages/BillingPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import OnboardingPage from "./pages/OnboardingPage";
import SettingsPage from "./pages/SettingsPage";
import SignupPage from "./pages/SignupPage";

function PlaceholderPage({ title, body }: { title: string; body: string }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <p>{body}</p>
    </section>
  );
}

export default function App() {
  const { isAuthenticated, profile, logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>Sentinel Forge</h1>
        <nav>
          <Link to="/login">Login</Link>
          <Link to="/signup">Signup</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/onboarding">Onboarding</Link>
          <Link to="/settings">Settings</Link>
          <Link to="/billing">Billing</Link>
          {isAuthenticated ? (
            <button type="button" onClick={logout} className="link-button">
              Logout
            </button>
          ) : null}
        </nav>
      </header>

      {profile ? <p className="session-banner">Signed in as {profile.email}</p> : null}

      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? <DashboardPage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="/onboarding"
            element={
              isAuthenticated ? <OnboardingPage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="/settings"
            element={
              isAuthenticated ? <SettingsPage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="/billing"
            element={
              isAuthenticated ? <BillingPage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="*"
            element={<PlaceholderPage title="Not Found" body="Choose a route from the top navigation." />}
          />
        </Routes>
      </main>
    </div>
  );
}