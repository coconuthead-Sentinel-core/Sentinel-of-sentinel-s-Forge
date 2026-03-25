---
name: azure-runtime-ops
description: Use when validating Azure prerequisites, CLI auth context, deployment readiness, and runtime dependency checks for Sentinel Forge. Triggers: Azure CLI checks, azure deployment readiness, azure auth context, azure runtime validation, container registry setup.
---

# Azure Runtime Ops

## Goal

Standardize Azure-related local readiness checks before deployment operations.

## Capabilities

1. Verify Azure CLI availability and auth context.
2. Verify Terraform availability where required.
3. Verify container registry command readiness.
4. Record environment limitations explicitly.

## Primary Commands

1. `pwsh scripts/env_automation.ps1 azure-check`
2. `az account show`
3. `az group list --output table`

## Guardrails

1. Do not claim Azure deployment completion from static files only.
2. Distinguish local config validity from live subscription verification.
3. Keep secrets out of logs and command history.
