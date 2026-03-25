import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import {
  createCheckout,
  getSubscription,
  listPlans,
  openBillingPortal,
  type BillingPlan,
  type SubscriptionStatus,
} from "../lib/api";

export default function BillingPage() {
  const { tokens } = useAuth();
  const [plans, setPlans] = useState<BillingPlan[]>([]);
  const [subscription, setSubscription] = useState<SubscriptionStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!tokens?.access_token) {
      return;
    }

    let cancelled = false;
    Promise.all([listPlans(tokens.access_token), getSubscription(tokens.access_token)])
      .then(([plansResp, subResp]) => {
        if (!cancelled) {
          setPlans(plansResp.plans);
          setSubscription(subResp);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load billing data");
        }
      });

    return () => {
      cancelled = true;
    };
  }, [tokens]);

  async function startCheckout(planId: string) {
    if (!tokens?.access_token) {
      return;
    }
    setError("");
    try {
      const result = await createCheckout(tokens.access_token, {
        plan: planId,
        success_url: window.location.origin + "/billing",
        cancel_url: window.location.origin + "/billing",
      });
      window.location.href = result.checkout_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Checkout failed");
    }
  }

  async function goToPortal() {
    if (!tokens?.access_token) {
      return;
    }
    setError("");
    try {
      const result = await openBillingPortal(tokens.access_token);
      window.location.href = result.portal_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Portal launch failed");
    }
  }

  return (
    <section className="panel">
      <h2>Billing</h2>
      <p>Manage your plan and subscription lifecycle.</p>

      {error ? <p className="error-msg">{error}</p> : null}

      <div className="kv-grid">
        <div>
          <span className="kv-label">Current Tier</span>
          <strong>{subscription?.tier || "free"}</strong>
        </div>
        <div>
          <span className="kv-label">Status</span>
          <strong>{subscription?.status || "none"}</strong>
        </div>
      </div>

      <h3>Plans</h3>
      <div className="plan-grid">
        {plans.map((plan) => (
          <article key={plan.id} className="plan-card">
            <h4>{plan.name}</h4>
            <p>{plan.description}</p>
            <p className="plan-price">${plan.price_monthly}/month</p>
            <ul>
              {plan.features.slice(0, 4).map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
            <button type="button" onClick={() => startCheckout(plan.id)}>
              Choose {plan.name}
            </button>
          </article>
        ))}
      </div>

      <button type="button" onClick={goToPortal} className="secondary-btn">
        Open Billing Portal
      </button>
    </section>
  );
}