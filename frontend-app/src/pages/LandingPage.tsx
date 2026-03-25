import { Link } from "react-router-dom";

const tiers = [
  {
    name: "Starter",
    price: 29,
    features: [
      "1,000 API calls / month",
      "Core cognitive processing",
      "Email support",
      "Single user",
    ],
  },
  {
    name: "Pro",
    price: 99,
    popular: true,
    features: [
      "25,000 API calls / month",
      "Advanced cognitive modes",
      "Priority support",
      "Up to 5 team members",
      "Custom processing rules",
    ],
  },
  {
    name: "Enterprise",
    price: 499,
    features: [
      "Unlimited API calls",
      "Full cognitive suite",
      "Dedicated support & SLA",
      "Unlimited team members",
      "Custom integrations",
      "On-premise option",
    ],
  },
];

const features = [
  {
    title: "Cognitive AI Processing",
    description:
      "Process information through diverse cognitive patterns — analytical, creative, critical, and more — powered by advanced AI orchestration.",
  },
  {
    title: "Real-Time API",
    description:
      "Enterprise-grade REST and WebSocket APIs with sub-second response times. Integrate AI-powered analysis into any application or workflow.",
  },
  {
    title: "Secure by Design",
    description:
      "TLS encryption, JWT authentication, role-based access control, and API key management. Your data stays yours.",
  },
  {
    title: "Flexible Subscriptions",
    description:
      "Start small and scale as you grow. Transparent pricing with no hidden fees. Upgrade, downgrade, or cancel anytime via the billing portal.",
  },
];

export default function LandingPage() {
  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <h1>Sentinel Forge</h1>
        <p className="hero-tagline">
          Enterprise-grade cognitive AI orchestration platform.
          <br />
          Process, analyze, and transform information at scale.
        </p>
        <div className="hero-actions">
          <Link to="/signup" className="btn btn-primary">
            Get Started Free
          </Link>
          <Link to="/login" className="btn btn-outline">
            Sign In
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="section" id="features">
        <h2 className="section-title">Why Sentinel Forge?</h2>
        <div className="feature-grid">
          {features.map((f) => (
            <div key={f.title} className="feature-card">
              <h3>{f.title}</h3>
              <p>{f.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section className="section section-alt" id="pricing">
        <h2 className="section-title">Simple, Transparent Pricing</h2>
        <div className="pricing-grid">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`pricing-card${tier.popular ? " pricing-popular" : ""}`}
            >
              {tier.popular && <span className="popular-badge">Most Popular</span>}
              <h3>{tier.name}</h3>
              <p className="pricing-amount">
                <span className="price">${tier.price}</span>
                <span className="period">/month</span>
              </p>
              <ul>
                {tier.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <Link to="/signup" className="btn btn-primary btn-full">
                Start with {tier.name}
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="section cta-section">
        <h2>Ready to get started?</h2>
        <p>Create your account in seconds. No credit card required to explore.</p>
        <Link to="/signup" className="btn btn-primary btn-lg">
          Create Your Account
        </Link>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-links">
          <a href="/legal/terms.html">Terms of Service</a>
          <a href="/legal/privacy.html">Privacy Policy</a>
          <Link to="/login">Sign In</Link>
        </div>
        <p className="footer-copy">
          &copy; {new Date().getFullYear()} Sentinel Forge. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
