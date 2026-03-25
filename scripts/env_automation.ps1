param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('doctor','test','security','ports','diagnostics','azure-check')]
    [string]$Action,
    [int[]]$Ports = @(8000,443)
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$venvPy = Join-Path $repo '.venv/Scripts/python.exe'

function Write-Section([string]$title) {
    Write-Host "`n=== $title ===" -ForegroundColor Cyan
}

function Has-Cmd([string]$name) {
    return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

switch ($Action) {
    'doctor' {
        Write-Section 'Tool Availability'
        $tools = @('git','docker','nginx','node','npm','gh','az','terraform')
        foreach ($tool in $tools) {
            if (Has-Cmd $tool) {
                Write-Host "$tool : FOUND"
            } else {
                Write-Host "$tool : MISSING" -ForegroundColor Yellow
            }
        }

        Write-Section 'Python Environment'
        if (Test-Path $venvPy) {
            & $venvPy --version
            & $venvPy -m pip --version
        } else {
            Write-Host '.venv python missing' -ForegroundColor Red
        }
    }

    'test' {
        Write-Section 'Running Billing + Full Test Suite'
        if (-not (Test-Path $venvPy)) { throw '.venv python not found' }
        Push-Location $repo
        try {
            & $venvPy -m pytest tests/test_billing.py -q
            & $venvPy -m pytest tests -q
        } finally {
            Pop-Location
        }
    }

    'security' {
        Write-Section 'Running Local Security Gates'
        if (-not (Test-Path $venvPy)) { throw '.venv python not found' }
        Push-Location $repo
        try {
            & $venvPy -m pip install pip-audit bandit | Out-Null
            & $venvPy -m pip_audit
            & $venvPy -m bandit -r backend -ll
        } finally {
            Pop-Location
        }
    }

    'ports' {
        Write-Section 'Port Check'
        foreach ($p in $Ports) {
            $listener = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
            if ($listener) {
                Write-Host "Port $p : LISTENING"
            } else {
                Write-Host "Port $p : NOT LISTENING" -ForegroundColor Yellow
            }
        }
    }

    'diagnostics' {
        Write-Section 'Diagnostics Hint'
        Write-Host 'Use VS Code Problems panel filters to separate execution errors from markdown style warnings.'
        Write-Host 'Primary execution blockers are typically workflow, Python import, or runtime tool availability errors.'
    }

    'azure-check' {
        Write-Section 'Azure Prerequisite Check'
        if (Has-Cmd 'az') {
            az version | Out-String | Write-Host
            az account show --output table
        } else {
            Write-Host 'az CLI not found' -ForegroundColor Yellow
        }

        if (Has-Cmd 'terraform') {
            terraform version
        } else {
            Write-Host 'terraform not found' -ForegroundColor Yellow
        }
    }
}
