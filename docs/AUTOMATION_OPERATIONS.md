# Automation Operations Guide

This guide documents terminal-first automation commands added for this workspace.

## Environment Automation

1. `pwsh scripts/env_automation.ps1 doctor`
2. `pwsh scripts/env_automation.ps1 test`
3. `pwsh scripts/env_automation.ps1 security`
4. `pwsh scripts/env_automation.ps1 ports -Ports 8000,443`
5. `pwsh scripts/env_automation.ps1 diagnostics`
6. `pwsh scripts/env_automation.ps1 azure-check`

## Git and Commit Automation

1. `pwsh scripts/git_ops.ps1 status`
2. `pwsh scripts/git_ops.ps1 sync`
3. `pwsh scripts/git_ops.ps1 commit -Message "feat: ..."`
4. `pwsh scripts/git_ops.ps1 push`
5. `pwsh scripts/git_ops.ps1 release-runs`

## Added Skills

1. `.github/skills/environment-automation-control/SKILL.md`
2. `.github/skills/github-terminal-commit-ops/SKILL.md`
3. `.github/skills/azure-runtime-ops/SKILL.md`

## Notes

1. Runtime Docker/nginx checks still require those binaries
   to be installed on the host.
2. Azure deployment checks require authenticated Azure CLI.
3. GitHub workflow run queries require GitHub CLI authentication.
