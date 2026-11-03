# Safe local QA runner. No migrations, imports of seed, production changes, or secrets.
param([switch]$SkipFrontend)
$ErrorActionPreference = 'Continue'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Results = [System.Collections.Generic.List[string]]::new()
function Check($Label, [scriptblock]$Work) {
  Write-Host "`n=== $Label ===" -ForegroundColor Cyan
  try {
    & $Work
    if ($LASTEXITCODE -ne 0) { throw "Exit code $LASTEXITCODE" }
    Write-Host "PASS: $Label" -ForegroundColor Green
    $Results.Add("PASS: $Label")
  } catch {
    Write-Host "FAIL or BLOCKED: $Label - $($_.Exception.Message)" -ForegroundColor Yellow
    $Results.Add("FAIL/BLOCKED: $Label")
  }
}
Push-Location $Root
try {
  $Python = Join-Path $Root 'backend\.venv\Scripts\python.exe'
  if (-not (Test-Path $Python)) { $Python = 'python' }
  Check 'Python version' { & $Python --version }
  Check 'Node version' { node --version }
  Check 'Python backend dependencies' { & $Python -c "import fastapi, sqlalchemy, alembic, psycopg, jwt, pytest, httpx; print('Backend imports OK')" }
  Check 'Frontend dependencies' { if (-not (Test-Path 'node_modules\vite\bin\vite.js')) { throw 'node_modules missing: run npm install first' }; Write-Host 'Vite installed' }
  Check 'Backend compile' {
    Push-Location (Join-Path $Root 'backend')
    try { & $Python -m compileall -q app scripts tests } finally { Pop-Location }
  }
  Check 'Backend pytest on isolated test database' {
    Push-Location (Join-Path $Root 'backend')
    try { & $Python -m pytest -q tests } finally { Pop-Location }
  }
  Check 'Node source and locale tests' { npm test }
  if (-not $SkipFrontend) {
    Check 'Frontend tests' { npm run test:frontend }
    Check 'Vite production build' { npm run build }
  }
  Write-Host "`n=== RESULTS ===" -ForegroundColor Cyan
  $Results | ForEach-Object { Write-Host $_ }
  Write-Host 'No database migration, seed, or production database modification was performed.'
} finally { Pop-Location }
if (($Results | Where-Object { $_ -like 'FAIL*' }).Count -gt 0) { exit 1 }
