export type TokenResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export type UserProfile = {
  id: string;
  email: string;
  display_name: string;
  role: string;
  created_at: string;
  subscription_tier: string;
};

export type SystemStatus = {
  status: string;
  [key: string]: unknown;
};

export type BillingPlan = {
  id: string;
  name: string;
  description: string;
  features: string[];
  price_monthly: number;
  price_annual: number;
};

export type BillingPlansResponse = {
  plans: BillingPlan[];
};

export type SubscriptionStatus = {
  tier: string;
  status: string;
  current_period_end?: string | null;
  cancel_at_period_end: boolean;
  stripe_customer_id: string;
};

export type CheckoutResponse = {
  checkout_url: string;
  session_id: string;
};

export type BillingPortalResponse = {
  portal_url: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  return (await response.json()) as T;
}

export async function signup(payload: {
  email: string;
  password: string;
  display_name: string;
}): Promise<TokenResponse> {
  return request<TokenResponse>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function login(payload: { email: string; password: string }): Promise<TokenResponse> {
  return request<TokenResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getProfile(accessToken: string): Promise<UserProfile> {
  return request<UserProfile>("/api/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export async function getStatus(): Promise<SystemStatus> {
  return request<SystemStatus>("/api/status", { method: "GET" });
}

export async function listPlans(accessToken: string): Promise<BillingPlansResponse> {
  return request<BillingPlansResponse>("/api/billing/plans", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export async function getSubscription(accessToken: string): Promise<SubscriptionStatus> {
  return request<SubscriptionStatus>("/api/billing/subscription", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export async function createCheckout(
  accessToken: string,
  payload: { plan: string; success_url: string; cancel_url: string },
): Promise<CheckoutResponse> {
  return request<CheckoutResponse>("/api/billing/checkout", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(payload),
  });
}

export async function openBillingPortal(accessToken: string): Promise<BillingPortalResponse> {
  return request<BillingPortalResponse>("/api/billing/portal", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}