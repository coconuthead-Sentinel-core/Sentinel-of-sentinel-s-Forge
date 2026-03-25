import { Link } from "react-router-dom";

const checklist = [
  "Create your account and sign in",
  "Review profile details in Settings",
  "Select a subscription plan in Billing",
  "Run your first cognition request from the API dashboard",
];

export default function OnboardingPage() {
  return (
    <section className="panel">
      <h2>Onboarding</h2>
      <p>Use this short checklist to complete first-time setup.</p>
      <ol className="onboarding-list">
        {checklist.map((step) => (
          <li key={step}>{step}</li>
        ))}
      </ol>
      <p>
        When complete, continue to your <Link to="/dashboard">dashboard</Link>.
      </p>
    </section>
  );
}