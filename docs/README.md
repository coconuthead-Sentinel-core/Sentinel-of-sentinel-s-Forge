# Sentinel Forge — Paperwork Index

This is the single routing point for every non-code artifact in the Sentinel
Forge repository. The top-level `README.md` points here for the full
engineering-build, SDLC, governance, security, legal, and iOS-track paperwork
packets.

If something is missing from this index, it is not considered "finished" — add
the document in the right section and link it here.

---

## 1. Engineering-build and operations

| Document | Purpose |
| --- | --- |
| [`QUICKSTART.md`](QUICKSTART.md) | Minimal local bring-up. |
| [`USER_GUIDE.md`](USER_GUIDE.md) | End-user walk-through of the chat / cognition flows. |
| [`API.md`](API.md) | Narrative REST + WebSocket surface. |
| [`API_EXAMPLES.md`](API_EXAMPLES.md) | Runnable client snippets for the API surface. |
| [`env_setup.md`](env_setup.md) | Environment variables, secrets, and local mock mode. |
| [`AUTOMATION_OPERATIONS.md`](AUTOMATION_OPERATIONS.md) | Background jobs, schedulers, and operational scripts. |
| [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) | Known-failure first-aid guide. |
| [`RELEASE_PIPELINE.md`](RELEASE_PIPELINE.md) | Release workflow, registry variables, and deploy-time secrets. |
| [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) | Branch / commit / review conventions. |
| [`PARTNER_ENV_EXECUTION_CHECKLIST.md`](PARTNER_ENV_EXECUTION_CHECKLIST.md) | Partner-environment runbook. |
| [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) | Third-party software attributions. |
| [`ROADMAP.md`](ROADMAP.md) | Forward-looking work tracked alongside the README roadmap. |
| [`examples/dashboard.py`](examples/dashboard.py) | Example dashboard client. |

## 2. SDLC packet (`docs/sdlc/`)

Phase-tagged artifacts (`P1-…` through `P9-…`) so every SDLC stage has an
owned, dated document.

| Document | Purpose |
| --- | --- |
| [`sdlc/P1-CHARTER-001.md`](sdlc/P1-CHARTER-001.md) | Project charter. |
| [`sdlc/P1-BIZCASE-002.md`](sdlc/P1-BIZCASE-002.md) | Business case. |
| [`sdlc/P1-FEAS-003.md`](sdlc/P1-FEAS-003.md) | Feasibility study. |
| [`sdlc/P1-SOW-004.md`](sdlc/P1-SOW-004.md) | Statement of work. |
| [`sdlc/P1-STAKE-005.md`](sdlc/P1-STAKE-005.md) | Stakeholder register. |
| [`sdlc/P1-RACI-006.md`](sdlc/P1-RACI-006.md) | RACI matrix. |
| [`sdlc/P1-VISION-008.md`](sdlc/P1-VISION-008.md) | Product vision. |
| [`sdlc/PRD.md`](sdlc/PRD.md) | Product requirements. |
| [`sdlc/SYSTEM_DESIGN.md`](sdlc/SYSTEM_DESIGN.md) | System design. |
| [`sdlc/API_CONTRACTS.md`](sdlc/API_CONTRACTS.md) | API contracts. |
| [`sdlc/BACKLOG.md`](sdlc/BACKLOG.md) | Backlog of tracked work. |
| [`sdlc/TEST_STRATEGY.md`](sdlc/TEST_STRATEGY.md) | Test strategy. |
| [`sdlc/P9-ACCEPT-076.md`](sdlc/P9-ACCEPT-076.md) | Acceptance sign-off. |
| [`sdlc/P9-TRANS-077.md`](sdlc/P9-TRANS-077.md) | Transition to operations. |
| [`sdlc/P9-MAINT-078.md`](sdlc/P9-MAINT-078.md) | Maintenance plan. |
| [`sdlc/P9-PIR-079.md`](sdlc/P9-PIR-079.md) | Post-implementation review. |
| [`sdlc/P9-DRP-080.md`](sdlc/P9-DRP-080.md) | Disaster recovery plan. |
| [`sdlc/P9-PROOF-LEDGER-081.md`](sdlc/P9-PROOF-LEDGER-081.md) | Proof-of-delivery ledger. |
| [`sdlc/P9-CLOSE-075.md`](sdlc/P9-CLOSE-075.md) | Project closure record. |
| [`SDLC_TOOLS_SKILLS_BLUEPRINT.md`](SDLC_TOOLS_SKILLS_BLUEPRINT.md) | Tools + skills blueprint covering the SDLC. |

## 3. Governance, security, and compliance (`docs/compliance/`)

| Document | Purpose |
| --- | --- |
| [`compliance/AI_POLICY.md`](compliance/AI_POLICY.md) | Organisational AI usage policy. |
| [`compliance/INFORMATION_SECURITY_POLICY.md`](compliance/INFORMATION_SECURITY_POLICY.md) | ISMS-aligned information security policy. |
| [`compliance/STATEMENT_OF_APPLICABILITY.md`](compliance/STATEMENT_OF_APPLICABILITY.md) | ISO 27001 SoA. |
| [`compliance/ASSET_RISK_REGISTER.md`](compliance/ASSET_RISK_REGISTER.md) | Asset + risk register. |
| [`compliance/PROCESSING_ACTIVITIES_REGISTER.md`](compliance/PROCESSING_ACTIVITIES_REGISTER.md) | GDPR Article 30 record. |
| [`compliance/DPIA.md`](compliance/DPIA.md) | Data protection impact assessment. |
| [`compliance/FRIA.md`](compliance/FRIA.md) | Fundamental rights impact assessment (EU AI Act). |
| [`compliance/INCIDENT_LOG.md`](compliance/INCIDENT_LOG.md) | Security + privacy incident log. |

## 4. Legal and commercial (`docs/legal/`)

| Document | Purpose |
| --- | --- |
| [`legal/TERMS_OF_SERVICE.md`](legal/TERMS_OF_SERVICE.md) | Customer-facing terms of service. |
| [`legal/PRIVACY_POLICY.md`](legal/PRIVACY_POLICY.md) | Privacy policy. |
| [`legal/SAAS_AGREEMENT.md`](legal/SAAS_AGREEMENT.md) | SaaS master agreement. |
| [`legal/DPA.md`](legal/DPA.md) | Data processing addendum. |
| [`legal/SLA.md`](legal/SLA.md) | Service level agreement. |
| [`legal/REFUND_CANCELLATION_POLICY.md`](legal/REFUND_CANCELLATION_POLICY.md) | Refund and cancellation policy. |
| [`legal/COMMERCIAL_LAUNCH_CHECKLIST.md`](legal/COMMERCIAL_LAUNCH_CHECKLIST.md) | Commercial launch + payments compliance pack. |

## 5. iOS / mobile compliance track

The mobile surface is tracked alongside the commercial launch pack. These
documents cover App Store review readiness, privacy nutrition labelling, and
mobile-specific acceptance criteria:

- [`legal/PRIVACY_POLICY.md`](legal/PRIVACY_POLICY.md) — privacy disclosures surfaced to App Store reviewers.
- [`legal/REFUND_CANCELLATION_POLICY.md`](legal/REFUND_CANCELLATION_POLICY.md) — purchase + refund semantics required for iOS IAP review.
- [`legal/COMMERCIAL_LAUNCH_CHECKLIST.md`](legal/COMMERCIAL_LAUNCH_CHECKLIST.md) — App Store and commercial launch checklist.
- [`compliance/DPIA.md`](compliance/DPIA.md) and [`compliance/FRIA.md`](compliance/FRIA.md) — privacy + rights review referenced by the mobile release gate.
- [`PARTNER_ENV_EXECUTION_CHECKLIST.md`](PARTNER_ENV_EXECUTION_CHECKLIST.md) — partner-facing execution checklist including mobile data-node readiness.

## 6. Readiness memos and pilot handoffs

| Document | Purpose |
| --- | --- |
| [`PLATFORM_READINESS_MEMO.md`](PLATFORM_READINESS_MEMO.md) | Interdepartmental platform readiness memo. |
| [`INTERDEPARTMENTAL_COMPLETION_MEMO.md`](INTERDEPARTMENTAL_COMPLETION_MEMO.md) | Launch-item completion memo (items 7–9). |
| [`FINAL_ACCEPTANCE_READINESS.md`](FINAL_ACCEPTANCE_READINESS.md) | Final acceptance readiness summary. |
| [`COMPLETENESS_ASSESSMENT.md`](COMPLETENESS_ASSESSMENT.md) | Completeness assessment across all workstreams. |
| [`MEMO_TO_CLAUDE.md`](MEMO_TO_CLAUDE.md) | Internal engineering memo to the AI assistant. |
| [`MEMO_TO_VR_STUDIOS_ASSISTANT.md`](MEMO_TO_VR_STUDIOS_ASSISTANT.md) | VR Studios pilot assistant memo. |
| [`VR_STUDIOS_DATA_NODE.md`](VR_STUDIOS_DATA_NODE.md) | VR Studios data-node architecture. |
| [`VR_STUDIOS_FINAL_HANDOFF_REPORT.md`](VR_STUDIOS_FINAL_HANDOFF_REPORT.md) | VR Studios final handoff report. |

---

## Paperwork status

All packets above are present in the repository. When a document changes on the
authoring laptop, update the relevant file in `docs/` and — if its purpose or
location moves — update this index in the same commit so the README's paperwork
promise stays honest.
