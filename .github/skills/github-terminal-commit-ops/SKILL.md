---
name: github-terminal-commit-ops
description: Use when performing pull/push, branch sync, non-interactive commits, release evidence capture, and terminal-driven GitHub workflows for this repository. Triggers: push pull github, commit workflow, sync branch, release run evidence, powershell git automation.
---

# GitHub Terminal Commit Ops

## Goal

Provide repeatable non-interactive Git operations from PowerShell.

## Capabilities

1. Safe pull/rebase and status checks.
2. Commit with message validation.
3. Push and upstream setup.
4. Optional GitHub CLI run-link capture when available.

## Primary Commands

1. `pwsh scripts/git_ops.ps1 status`
2. `pwsh scripts/git_ops.ps1 sync`
3. `pwsh scripts/git_ops.ps1 commit -Message "feat: ..."`
4. `pwsh scripts/git_ops.ps1 push`
5. `pwsh scripts/git_ops.ps1 release-runs`

## Guardrails

1. No force push unless explicitly requested.
2. No commit without a message.
3. Show staged file list before commit.
