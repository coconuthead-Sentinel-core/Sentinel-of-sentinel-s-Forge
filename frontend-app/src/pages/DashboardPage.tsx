import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { getStatus, type SystemStatus } from "../lib/api";

export default function DashboardPage() {
  const { profile } = useAuth();
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    getStatus()
      .then((result) => {
        if (!cancelled) {
          setStatus(result);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load status");
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section className="panel">
      <h2>Dashboard</h2>
      <p>Welcome back, {profile?.display_name || profile?.email || "User"}.</p>

      <div className="kv-grid">
        <div>
          <span className="kv-label">Role</span>
          <strong>{profile?.role || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Subscription</span>
          <strong>{profile?.subscription_tier || "free"}</strong>
        </div>
      </div>

      <h3>API Status</h3>
      {error ? <p className="error-msg">{error}</p> : null}
      <pre className="code-block">{JSON.stringify(status ?? { loading: true }, null, 2)}</pre>
    </section>
  );
}