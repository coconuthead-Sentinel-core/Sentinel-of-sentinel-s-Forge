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

// --- Chat ---
export type ChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export type ChatChoice = {
  index: number;
  message: { role: string; content: string | null };
  finish_reason: string | null;
};

export type ChatResponse = {
  id: string;
  model: string | null;
  created: number;
  choices: ChatChoice[];
  usage: Record<string, unknown> | null;
};

// --- Cognitive Processing ---
export type ProcessResponse = {
  input_id: string;
  output_id: string;
  result: unknown;
  processing_time: number;
  pool_used: string;
};

// --- Notes ---
export type NoteItem = {
  id: string;
  text: string;
  tag: string;
  metadata?: Record<string, unknown>;
  created_at?: string;
};

// --- Dashboard Metrics ---
export type DashboardMetrics = {
  timestamp: number;
  health_status: "green" | "yellow" | "red";
  core: {
    status: string;
    pools: number;
    processors: number;
    executions: number;
  };
  performance: {
    avg_latency_ms: number;
    p95_latency_ms: number;
    heap_mib: number;
    heap_stale_ratio: number;
  };
  cognition: {
    enabled: boolean;
    memory_entries: number;
    symbolic_rules: number;
    embedding_active: boolean;
  };
  platform: string;
};

export type DashboardActivity = {
  intents: Record<string, number>;
  topics: Record<string, number>;
  active_threads: number;
  recent_events: unknown[];
};

// --- Cognition ---
export type MemorySnapshot = {
  size: number;
  capacity: number;
  top_preview: string[];
};

export type Suggestions = {
  suggestions: Array<Record<string, unknown>>;
};

export type SymbolicRules = {
  rules: Record<string, string>;
};

export type CogThread = {
  id: string;
  topic: string;
  count: number;
};

// --- API Client ---

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

function authHeaders(token: string): Record<string, string> {
  return { Authorization: `Bearer ${token}` };
}

// --- Auth ---

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
    headers: authHeaders(accessToken),
  });
}

// --- Billing ---

export async function getStatus(): Promise<SystemStatus> {
  return request<SystemStatus>("/api/status", { method: "GET" });
}

export async function listPlans(accessToken: string): Promise<BillingPlansResponse> {
  return request<BillingPlansResponse>("/api/billing/plans", {
    method: "GET",
    headers: authHeaders(accessToken),
  });
}

export async function getSubscription(accessToken: string): Promise<SubscriptionStatus> {
  return request<SubscriptionStatus>("/api/billing/subscription", {
    method: "GET",
    headers: authHeaders(accessToken),
  });
}

export async function createCheckout(
  accessToken: string,
  payload: { plan: string; success_url: string; cancel_url: string },
): Promise<CheckoutResponse> {
  return request<CheckoutResponse>("/api/billing/checkout", {
    method: "POST",
    headers: authHeaders(accessToken),
    body: JSON.stringify(payload),
  });
}

export async function openBillingPortal(accessToken: string): Promise<BillingPortalResponse> {
  return request<BillingPortalResponse>("/api/billing/portal", {
    method: "POST",
    headers: authHeaders(accessToken),
  });
}

// --- AI Chat ---

export async function sendChat(messages: ChatMessage[]): Promise<ChatResponse> {
  return request<ChatResponse>("/api/ai/chat", {
    method: "POST",
    body: JSON.stringify({ messages }),
  });
}

// --- Cognitive Processing ---

export async function cogProcess(data: string): Promise<ProcessResponse> {
  return request<ProcessResponse>("/api/cog/process", {
    method: "POST",
    body: JSON.stringify({ data }),
  });
}

export async function cogGetRules(): Promise<SymbolicRules> {
  return request<SymbolicRules>("/api/cog/rules", { method: "GET" });
}

export async function cogGetMemory(): Promise<MemorySnapshot> {
  return request<MemorySnapshot>("/api/cog/memory", { method: "GET" });
}

export async function cogGetSuggestions(limit: number = 5): Promise<Suggestions> {
  return request<Suggestions>(`/api/cog/suggest?limit=${limit}`, { method: "GET" });
}

export async function cogGetThreads(): Promise<{ threads: CogThread[] }> {
  return request<{ threads: CogThread[] }>("/api/cog/threads", { method: "GET" });
}

// --- Notes ---

export async function listNotes(): Promise<NoteItem[]> {
  return request<NoteItem[]>("/api/notes", { method: "GET" });
}

export async function upsertNote(payload: {
  text: string;
  tag: string;
  metadata?: Record<string, unknown>;
}): Promise<NoteItem> {
  return request<NoteItem>("/api/notes/upsert", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// --- Dashboard ---

export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  return request<DashboardMetrics>("/api/dashboard/metrics", { method: "GET" });
}

export async function getDashboardActivity(): Promise<DashboardActivity> {
  return request<DashboardActivity>("/api/dashboard/activity", { method: "GET" });
}
