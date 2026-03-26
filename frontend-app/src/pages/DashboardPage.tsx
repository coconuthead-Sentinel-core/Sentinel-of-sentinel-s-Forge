import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import {
  getDashboardMetrics,
  getDashboardActivity,
  type DashboardMetrics,
  type DashboardActivity,
} from "../lib/api";

const healthColors: Record<string, string> = {
  green: "#16a34a",
  yellow: "#ca8a04",
  red: "#dc2626",
};

export default function DashboardPage() {
  const { profile } = useAuth();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [activity, setActivity] = useState<DashboardActivity | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    Promise.allSettled([getDashboardMetrics(), getDashboardActivity()]).then(
      ([mRes, aRes]) => {
        if (cancelled) return;
        if (mRes.status === "fulfilled") setMetrics(mRes.value);
        if (aRes.status === "fulfilled") setActivity(aRes.value);
        if (mRes.status === "rejected" && aRes.status === "rejected") {
          setError("Failed to load dashboard data");
        }
      },
    );
    return () => { cancelled = true; };
  }, []);

  return (
    <section className="panel">
      <h2>Dashboard</h2>
      <p>
        Welcome back, {profile?.display_name || profile?.email || "User"}.
        {profile?.subscription_tier && profile.subscription_tier !== "free" && (
          <> Your plan: <strong>{profile.subscription_tier}</strong>.</>
        )}
      </p>

      {error && <p className="error-msg">{error}</p>}

      {/* Quick Actions */}
      <div className="quick-actions">
        <Link to="/chat" className="action-card">
          <strong>AI Chat</strong>
          <span>Talk to the cognitive engine</span>
        </Link>
        <Link to="/cognition" className="action-card">
          <strong>Process Text</strong>
          <span>Run cognitive analysis</span>
        </Link>
        <Link to="/notes" className="action-card">
          <strong>Notes</strong>
          <span>Manage knowledge base</span>
        </Link>
        <Link to="/insights" className="action-card">
          <strong>Insights</strong>
          <span>Memory, rules, threads</span>
        </Link>
      </div>

      {/* System Health */}
      {metrics && (
        <>
          <h3>
            System Health{" "}
            <span
              className="health-dot"
              style={{ background: healthColors[metrics.health_status] || "#999" }}
            />
          </h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Status</span>
              <strong>{metrics.core.status}</strong>
            </div>
            <div>
              <span className="kv-label">Pools</span>
              <strong>{metrics.core.pools}</strong>
            </div>
            <div>
              <span className="kv-label">Processors</span>
              <strong>{metrics.core.processors}</strong>
            </div>
            <div>
              <span className="kv-label">Total Executions</span>
              <strong>{metrics.core.executions}</strong>
            </div>
          </div>

          <h3>Performance</h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Avg Latency</span>
              <strong>{metrics.performance.avg_latency_ms.toFixed(1)} ms</strong>
            </div>
            <div>
              <span className="kv-label">P95 Latency</span>
              <strong>{metrics.performance.p95_latency_ms.toFixed(1)} ms</strong>
            </div>
            <div>
              <span className="kv-label">Heap</span>
              <strong>{metrics.performance.heap_mib.toFixed(2)} MiB</strong>
            </div>
          </div>

          <h3>Cognition Engine</h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Enabled</span>
              <strong>{metrics.cognition.enabled ? "Yes" : "No"}</strong>
            </div>
            <div>
              <span className="kv-label">Memory Entries</span>
              <strong>{metrics.cognition.memory_entries}</strong>
            </div>
            <div>
              <span className="kv-label">Symbolic Rules</span>
              <strong>{metrics.cognition.symbolic_rules}</strong>
            </div>
            <div>
              <span className="kv-label">Embeddings</span>
              <strong>{metrics.cognition.embedding_active ? "Active" : "Off"}</strong>
            </div>
          </div>
        </>
      )}

      {/* Activity */}
      {activity && (
        <>
          <h3>Activity</h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Active Threads</span>
              <strong>{activity.active_threads}</strong>
            </div>
            <div>
              <span className="kv-label">Recent Events</span>
              <strong>{activity.recent_events?.length ?? 0}</strong>
            </div>
          </div>
          {Object.keys(activity.topics).length > 0 && (
            <div className="topic-tags">
              {Object.entries(activity.topics).map(([topic, count]) => (
                <span key={topic} className="topic-tag">
                  {topic} ({count})
                </span>
              ))}
            </div>
          )}
        </>
      )}

      {/* Account */}
      <h3>Account</h3>
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
    </section>
  );
}
