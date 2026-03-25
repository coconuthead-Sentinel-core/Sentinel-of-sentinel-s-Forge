---
name: sdlc-toolchain-closeout
description: Use when planning or executing SDLC completion for Sentinel Forge, including tool readiness, runtime verification, security gates, release evidence, and closure document reconciliation. Triggers: SDLC closeout, acceptance readiness, partner environment checklist, release blockers, tool assessment, completion checklist.
---

# SDLC Toolchain Closeout Skill

## Purpose

Provide a deterministic workflow for moving Sentinel Forge from repository-complete to SDLC-closeout-complete.

## Inputs

1. Current blocker list.
2. Environment tool availability.
3. Current P1 and P9 document status.
4. Required acceptance evidence.

## Workflow

### Step 1: Tool Readiness Gate

Validate critical toolchain first:

1. Docker Desktop with compose.
2. Python project environment plus pytest and dependencies.
3. Node and npm.
4. nginx validation path.
5. GitHub Actions execution access.

If any are missing, classify as Environment Limitation and stop closure claims.

### Step 2: Runtime Verification Gate

Execute partner checklist sequence:

1. Compose contract and startup checks.
2. nginx TLS validation.
3. Billing and full test suites.
4. Health/readiness/billing API checks.
5. Release workflow run evidence.

If any step fails, classify blocker as Runtime Issue or Environment Limitation.

### Step 3: Security Gate

Run and archive:

1. Dependency scan.
2. Static analysis.
3. Secret scan.
4. Container scan.

Record pass/fail thresholds and approved exceptions.

### Step 4: SDLC Reconciliation Gate

Reconcile P1 and P9 documents to real evidence only:

1. Replace stale test baselines.
2. Keep approval fields pending until signed.
3. Do not mark environment-limited checks as complete.
4. Ensure DR restore validation checkbox is evidence-backed.

### Step 5: Closure Decision

Decision is Ready only if all are true:

1. Critical tools available.
2. Runtime checklist passed with evidence.
3. Security gate evidence archived.
4. Required approvals captured.

Otherwise return Blocked with exact blocker count and types.

## Output Contract

Always return:

1. Confirmed items.
2. Partially confirmed items.
3. Not confirmed items.
4. SDLC delta list.
5. Final closure decision with blocker inventory.

## Guardrails

1. No synthetic approvals or signatures.
2. Separate repository-complete from environment-complete.
3. Every open item must include owner and next date.
4. Every completion claim must reference reproducible evidence.
