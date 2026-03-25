---
name: environment-automation-control
description: Use when configuring this workspace for high-velocity delivery, reducing noisy Problems diagnostics, automating local validation, ports checks, and debug triage loops. Triggers: automate environment, fix problems tab noise, setup terminal profile, debug console workflow, port checks, local quality gates.
---

# Environment Automation Control

## Goal

Make the workspace deterministic and low-friction for SDLC execution.

## Capabilities

1. Normalize terminal startup and Python environment use.
2. Run local health checks and test gates.
3. Triage diagnostics volume and separate actionable errors from style noise.
4. Validate runtime ports and endpoint reachability.

## Primary Commands

1. `pwsh scripts/env_automation.ps1 doctor`
2. `pwsh scripts/env_automation.ps1 test`
3. `pwsh scripts/env_automation.ps1 security`
4. `pwsh scripts/env_automation.ps1 ports -Ports 8000,443`
5. `pwsh scripts/env_automation.ps1 diagnostics`

## Guardrails

1. Never mark blocked runtime checks complete if Docker/nginx/GitHub runtime access is missing.
2. Keep approval/signature fields external and explicit.
3. Treat lint-style markdown findings separately from execution blockers.
