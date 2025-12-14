# Sentinel Prime - Shipment Preparation Protocol
# Purpose: Remove accidental file artifacts to ensure a clean build for market release.
# NO CODE IS REWRITTEN. ONLY GARBAGE FILES ARE REMOVED.

Write-Host "🛡️ Sentinel Prime: Preparing for Shipment..." -ForegroundColor Cyan

# List of artifacts identified in the commit manifest
$artifacts = @(
    "backend/# from typing import Any.py",
    "copy .env.example .env.txt",
    "requirements.txt.txt",
    "smoke_test.py.txt",
    "backend/smoke_test.py.txt",
    "New Text Document.txt"
)

# 1. Remove exact matches
foreach ($file in $artifacts) {
    if (Test-Path -LiteralPath $file) {
        Remove-Item -LiteralPath $file -Force
        Write-Host "   [REMOVED ARTIFACT] $file" -ForegroundColor Green
    }
}

# 2. Remove Pattern-based Artifacts (The "Ghost Files" from chat copy-paste)
# These files contain special characters or instruction text in the filename
Get-ChildItem -Recurse | Where-Object { $_.Name -like "*✅ CORRECT*" } | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Force
    Write-Host "   [REMOVED ARTIFACT] $($_.Name)" -ForegroundColor Green
}

Get-ChildItem -Recurse | Where-Object { $_.Name -like "*DELETE THIS ENTIRE LINE*" } | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Force
    Write-Host "   [REMOVED ARTIFACT] $($_.Name)" -ForegroundColor Green
}

Write-Host "`n✅ Shipment Package Clean." -ForegroundColor Green
Write-Host "👉 Action: Run 'git add .' to update the manifest." -ForegroundColor Yellow
