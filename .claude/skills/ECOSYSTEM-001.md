# ECOSYSTEM-001 — QNF Ecosystem Mapper

## Purpose
Maps the complete Quantum Nexus Forge ecosystem across all three layers, tracking component status, dependencies, and integration health.

## Ecosystem Components

### FORGE Layer (Software)
| Component | Status | Backend Route | Frontend Page |
|-----------|--------|---------------|---------------|
| Auth System | Active | `/api/auth/*` | LoginPage, SignupPage |
| AI Chat | Active | `/api/ai/chat` | ChatPage |
| Cognition Engine | Active | `/api/cog/*` | CognitionPage |
| Memory Lattice | Active | `/api/cog/memory` | InsightsPage |
| Symbolic Rules | Active | `/api/cog/rules` | InsightsPage |
| Thread Manager | Active | `/api/cog/threads` | InsightsPage |
| Suggestions | Active | `/api/cog/suggest` | InsightsPage |
| Notes System | Active | `/api/notes/*` | NotesPage |
| Glyph Codex | Active | `/api/glyphs/*` | Not yet wired |
| Billing/Stripe | Active | `/api/billing/*` | BillingPage |
| Dashboard Metrics | Active | `/api/dashboard/*` | DashboardPage |
| Settings | Active | `/api/auth/me` | SettingsPage |

### MAU-1 Layer (Hardware)
| Component | Status | Service Method |
|-----------|--------|----------------|
| Pool Manager | Active | `service.create_pool()` |
| Processor Engine | Active | `service.process()` |
| Heap Scheduler | Active | via `QuantumNexusForge` |
| Event Bus | Active | `eventbus.bus` |
| Triage Tuner | Standby | `service.metrics()` |
| Prometheus Export | Active | `/api/metrics/prom` |

### Avatar Layer (Interface)
| Component | Status | File |
|-----------|--------|------|
| Landing Page | Active | `LandingPage.tsx` |
| Conversation Mode | Active | `ChatPage.tsx` |
| Work Mode Dashboard | Active | `DashboardPage.tsx` |
| Onboarding Flow | Scaffold | `OnboardingPage.tsx` |
| Settings Panel | Active | `SettingsPage.tsx` |

## Integration Gaps
1. Glyph endpoints exist in backend but no frontend page yet
2. Session persistence (SESSION-WRAP) not yet implemented
3. WebSocket API (`ws_api.py`) not connected to frontend
4. Sync coordinator (`sentinel_sync.py`) not exposed in UI
