# Sentinel-of-sentinel-s-Forge SDLC Tools + Skills Blueprint

Date: 2026-03-24
Owner: Project Delivery and Operations
Purpose: Define the minimum and recommended toolchain and skill model required to complete Sentinel Forge to SDLC closeout standards.

## 1. Tool Assessment for Completion

### Tier A: No-Completion-Without (Critical Path)

These are hard blockers. Without them, project completion cannot be claimed at SDLC closeout level.

1. Docker Desktop (with `docker compose`)
   - Needed for runtime validation, deployment parity, container logs, and cutover rehearsal.
2. Python project environment with pytest and all repo dependencies
   - Needed for repeatable test evidence and acceptance quality gates.
3. Node.js LTS + npm
   - Needed for frontend build verification and release artifact confidence.
4. nginx validation path (`nginx -t` locally or containerized equivalent)
   - Needed for TLS and reverse-proxy acceptance evidence.
5. GitHub Actions execution access (`gh` CLI or web-run evidence process)
   - Needed for release pipeline completion evidence.

### Tier B: Must-Have for Professional SDLC Closure

1. OpenSSL
   - Certificate/key checks, TLS diagnostics, expiration checks.
2. jq
   - Structured API response validation and scriptable acceptance evidence.
3. Stripe CLI
   - Webhook and billing runtime verification.
4. Security gate tools
   - `pip-audit`, `bandit`, `semgrep`, `gitleaks`, `trivy`.
5. Performance test tool
   - `k6` or `locust`.
6. API contract/flow test tool
   - `newman` (or equivalent).

### Tier C: Wow Tools (High-Leverage Multipliers)

1. `act` for local GitHub Actions simulation.
2. Dev Containers for reproducible contributor environments.
3. Pre-commit framework with lint/security/test hooks.
4. Observability local stack (Prometheus + Grafana + Loki).
5. Automated evidence pack script for SDLC closeout artifacts.

## 2. Skills Blueprint (What Must Be Learned)

### Skill Group 1: Environment and Build Operations

Target outcome: Team can bootstrap and validate the full stack on demand.

Core skills:

1. Python venv creation, dependency pinning, deterministic installs.
2. Container lifecycle and Compose diagnostics.
3. Node/npm build pipeline and lockfile hygiene.
4. Environment variable governance and secrets handling.

Readiness test:

1. A new contributor can run setup and all tests in one session.
2. Build and runtime logs are understandable and actionable.

### Skill Group 2: Runtime Verification and Acceptance Evidence

Target outcome: Every checklist item can be proven with reproducible evidence.

Core skills:

1. Health/readiness/API endpoint validation scripting.
2. Billing flow verification in configured and mock modes.
3. TLS chain and keypair validation.
4. Capture and archive of workflow run evidence.

Readiness test:

1. Partner checklist completes in one pass with artifacts attached.
2. No acceptance claim depends on verbal confirmation alone.

### Skill Group 3: Security and Compliance Gates

Target outcome: Security posture is continuously measured, not assumed.

Core skills:

1. Dependency vulnerability scanning and triage.
2. Secret leak detection and remediation workflow.
3. Static analysis rule tuning and suppression governance.
4. Container image scanning and remediation prioritization.

Readiness test:

1. CI includes security gates and threshold policy.
2. Exceptions are documented with owner and expiry date.

### Skill Group 4: Release Engineering and Rollback

Target outcome: Releases are repeatable, observable, and reversible.

Core skills:

1. Workflow design (test, build, publish, promote).
2. Release artifact integrity and traceability.
3. Rollback criteria and playbook execution.
4. Hypercare monitoring and incident response handoff.

Readiness test:

1. A failed release can be rolled back within defined RTO.
2. Release proof package is generated for each production candidate.

### Skill Group 5: SDLC Documentation Discipline

Target outcome: Docs remain evidence-backed and current with code state.

Core skills:

1. Evidence-linked updates to P1 and P9 documents.
2. Distinguishing repository-complete vs environment-complete.
3. Signature/approval boundary control (no synthetic sign-off).
4. DR and operations checklist maintenance.

Readiness test:

1. All open placeholders are either closed or explicitly tracked with owner/date.
2. The closeout decision is auditable from repository artifacts alone.

## 3. SDLC Phase-to-Tool Matrix

## Phase 1: Initiation (P1 docs)

Required tools:

1. Git, Markdown linting, architecture diagram tooling, planning templates.
2. Cost and risk modeling sheets.

Required skills:

1. Scope framing, measurable success metrics, stakeholder/RACI quality.
2. Risk register and launch gate design.

Exit evidence:

1. P1 docs complete with owners, dates, and measurable criteria.

## Phase 2-5: Build, Verify, Harden

Required tools:

1. Python/pytest, Node/npm, Docker/Compose, lint/type tooling.
2. API test tooling and local observability.

Required skills:

1. Test-first implementation, dependency control, configuration hygiene.
2. Cross-component debugging and triage.

Exit evidence:

1. Full test pass, runtime service health, known issues classified.

## Phase 6-8: Release Preparation and Operations Readiness

Required tools:

1. GitHub Actions, registry tooling, TLS validation tooling.
2. Security scanners and load/perf runners.

Required skills:

1. Pipeline reliability and artifact governance.
2. SLO/alert/runbook readiness and rollback drills.

Exit evidence:

1. Pipeline run proof, security gate results, operations handoff package.

## Phase 9: Closure (P9 docs)

Required tools:

1. Evidence capture scripts, checklist runner, signature workflow.
2. DR test and restore validation tooling.

Required skills:

1. Evidence reconciliation, blocker typing, closure decision integrity.
2. PIR quality and lessons-learned conversion to backlog actions.

Exit evidence:

1. P9 docs reconciled, runtime checks complete, approvals captured, DR restore validated.

## 4. Guardrails (Non-Negotiables)

1. No item is marked complete without command output, artifact link, or signed approval.
2. Repository-complete and environment-complete must be tracked separately.
3. Pending approvals must remain explicit until signed.
4. Runtime limitations are blockers, not silent assumptions.
5. Every SDLC status must have an owner and next date.

## 5. 14-Day Enablement Plan (Skill Build Sprint)

Days 1-3:

1. Install Tier A tools and verify command availability.
2. Repair project venv workflow and test run commands.

Days 4-6:

1. Install Tier B security and evidence tools.
2. Add repeatable verification scripts for API/TLS/billing.

Days 7-10:

1. Wire security gates into CI with fail thresholds.
2. Add release workflow evidence capture checklist.

Days 11-14:

1. Execute full partner environment checklist.
2. Reconcile P9 docs with evidence and close open blockers.

## 6. Definition of Tool-Ready Environment

Environment is tool-ready only if all statements below are true:

1. Compose stack can build, run, and expose healthy endpoints.
2. Full test suite and billing suite pass from project venv.
3. TLS configuration validates and serves expected certificates.
4. Release workflow has a successful run with artifacts.
5. Security scans run in CI and produce policy-based pass/fail.
6. DR restore validation has at least one successful recorded run.

## 7. Completion Decision Rule

Project closeout can be declared only when:

1. Critical Path tools are present and operational.
2. Phase 9 runtime checks are complete and evidenced.
3. Approval/signature requirements are satisfied.
4. Remaining items are only accepted exceptions with owners and due dates.

If any of the above fails, status remains Blocked.

