# Sentinel Prime - Deep Decontamination Protocol
# Purpose: Remove specific file artifacts identified in the commit manifest.

$artifacts = @(
    "backend/# from typing import Any.py",
    "copy .env.example .env.txt",
    "requirements.txt.txt",
    "smoke_test.py.txt",
    "backend/smoke_test.py.txt",
    "New Text Document.txt"
)

Write-Host "🛡️ Sentinel Prime: Scanning for Anomalies..." -ForegroundColor Cyan

# 1. Remove exact matches
foreach ($file in $artifacts) {
    if (Test-Path -LiteralPath $file) {
        Remove-Item -LiteralPath $file -Force
        Write-Host "   [PURGED] $file" -ForegroundColor Red
    }
}

# 2. Remove Pattern-based Artifacts (The "Ghost Files")
# These have special characters that are hard to target by exact name
Get-ChildItem -Recurse | Where-Object { $_.Name -like "*✅ CORRECT*" } | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Force
    Write-Host "   [PURGED] $($_.Name)" -ForegroundColor Red
}

Get-ChildItem -Recurse | Where-Object { $_.Name -like "*DELETE THIS ENTIRE LINE*" } | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Force
    Write-Host "   [PURGED] $($_.Name)" -ForegroundColor Red
}

# 3. Check for redundant main.py
if ((Test-Path "backend/main.py") -and (Test-Path "main.py")) {
    Write-Host "⚠️  Warning: Duplicate entry points detected ('main.py' and 'backend/main.py')." -ForegroundColor Yellow
    Write-Host "   Please verify if 'backend/main.py' is needed. The root 'main.py' is usually the entry point." -ForegroundColor Yellow
}

Write-Host "`n✅ Decontamination Complete." -ForegroundColor Green
Write-Host "👉 EXECUTE: 'git reset' to unstage the garbage, then 'git add .' to restage the clean system." -ForegroundColor Cyan
