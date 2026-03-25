import { useAuth } from "../auth/AuthContext";

export default function SettingsPage() {
  const { profile } = useAuth();

  return (
    <section className="panel">
      <h2>Settings</h2>
      <p>Account profile details from your authenticated session.</p>

      <div className="kv-grid">
        <div>
          <span className="kv-label">User ID</span>
          <strong>{profile?.id || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Display Name</span>
          <strong>{profile?.display_name || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Email</span>
          <strong>{profile?.email || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Role</span>
          <strong>{profile?.role || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Created At</span>
          <strong>{profile?.created_at || "-"}</strong>
        </div>
        <div>
          <span className="kv-label">Subscription Tier</span>
          <strong>{profile?.subscription_tier || "free"}</strong>
        </div>
      </div>
    </section>
  );
}