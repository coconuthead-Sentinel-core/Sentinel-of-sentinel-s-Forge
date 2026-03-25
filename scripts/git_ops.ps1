param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('status','sync','commit','push','release-runs')]
    [string]$Action,
    [string]$Message
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    switch ($Action) {
        'status' {
            git status --short
        }

        'sync' {
            git fetch --all --prune
            git pull --rebase
            git status --short
        }

        'commit' {
            if ([string]::IsNullOrWhiteSpace($Message)) {
                throw 'Commit message required. Use -Message "..."'
            }
            git status --short
            git add -A
            git commit -m $Message
        }

        'push' {
            git push
        }

        'release-runs' {
            if (Get-Command gh -ErrorAction SilentlyContinue) {
                gh run list --workflow release.yml --limit 10
            } else {
                Write-Host 'gh CLI not found' -ForegroundColor Yellow
            }
        }
    }
} finally {
    Pop-Location
}
