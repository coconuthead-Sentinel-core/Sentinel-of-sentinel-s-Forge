# Sentinel Forge - Repository Decontamination Script

$filesToRemove = @(
    "backend/# from typing import Any.py",
    "copy .env.example .env.txt",
    "requirements.txt.txt",
    "smoke_test.py.txt",
    "backend/smoke_test.py.txt",
    "New Text Document.txt"
)

Write-Host "🛡️ Sentinel Prime: Initiating Cleanup Protocol..." -ForegroundColor Cyan

foreach ($file in $filesToRemove) {
    if (Test-Path -LiteralPath $file) {
        Remove-Item -LiteralPath $file -Force
        Write-Host "   [DELETE] $file" -ForegroundColor Green
    }
}

# Handling files with special characters or spaces that might be tricky to target literally
# Pattern: "backend/... ✅ CORRECT..."
Get-ChildItem "backend" | Where-Object { $_.Name -like "*CORRECT*" } | Remove-Item -Force -Verbose
# Pattern: "backend/api.py ❌ DELETE..."
Get-ChildItem "backend" | Where-Object { $_.Name -like "*DELETE THIS ENTIRE LINE*" } | Remove-Item -Force -Verbose

Write-Host "`n✅ Cleanup Complete." -ForegroundColor Green
Write-Host "👉 Action Required: Run 'git reset' then 'git add .' to refresh your commit." -ForegroundColor Yellow
