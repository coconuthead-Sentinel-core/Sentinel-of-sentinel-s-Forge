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
    title: "AI Conversation Mode",
    description:
      "Talk naturally with an AI that remembers context across sessions. Ask questions, brainstorm ideas, and get structured guidance — all through conversation.",
  },
  {
    title: "Cognitive Processing Engine",
    description:
      "Process text through symbolic reasoning, memory lattice, and thread-based analysis. Turn unstructured information into organized, actionable knowledge.",
  },
  {
    title: "Knowledge Notes & Memory",
    description:
      "Capture ideas, tag knowledge, and build your personal memory lattice. The system learns your patterns and surfaces relevant connections automatically.",
  },
  {
    title: "Built for How You Think",
    description:
      "Designed for neurodivergent professionals. Two distinct modes — conversation and work — with ADHD-friendly UX, minimal cognitive load, and interruption tolerance.",
  },
];

const useCases = [
  {
    title: "Neurodivergent Professionals",
    description: "Structured cognitive support with mode switching, external memory, and pattern recognition that adapts to how you work.",
  },
  {
    title: "Healthcare & CNA Workers",
    description: "Manage patient notes, track procedures, and handle high-pressure task management with AI-assisted organization.",
  },
  {
    title: "Solo Entrepreneurs",
    description: "Offload cognitive overhead to AI. Brainstorm, plan, track ideas, and process information without hiring a team.",
  },
  {
    title: "Students & Researchers",
    description: "Study aid with memory lattice, symbolic reasoning for complex topics, and AI tutoring through conversation mode.",
  },
  {
    title: "Automotive & Trades",
    description: "Quick reference lookup, procedure notes, and diagnostic reasoning — hands-free conversation mode for the shop floor.",
  },
  {
    title: "Elder Care Providers",
    description: "Simplified interface with routine support, medication tracking notes, and structured daily task management.",
  },
];

export default function LandingPage() {
  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <h1>Sentinel Forge</h1>
        <p className="hero-tagline">
          Your AI-powered cognitive companion.
          <br />
          Think clearer. Work smarter. Remember everything.
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

      {/* Use Cases */}
      <section className="section section-alt" id="use-cases">
        <h2 className="section-title">Who It's For</h2>
        <div className="feature-grid">
          {useCases.map((uc) => (
            <div key={uc.title} className="feature-card">
              <h3>{uc.title}</h3>
              <p>{uc.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section className="section" id="pricing">
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
