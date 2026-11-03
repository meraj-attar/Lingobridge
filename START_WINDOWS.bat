@echo off
setlocal
cd /d "%~dp0"
if not exist "backend\.env" (
  echo Missing backend\.env. Follow README.md to configure PostgreSQL first.
  pause
  exit /b 1
)
if not exist "backend\.venv\Scripts\python.exe" (
  echo Missing Python environment. Follow backend setup steps in README.md.
  pause
  exit /b 1
)
if not exist "node_modules\vite\bin\vite.js" (
  echo Missing Node packages. Run npm install before starting.
  pause
  exit /b 1
)
start "LingoBridge FastAPI" cmd /k "cd /d %~dp0backend && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8003"
echo Starting Vite on http://localhost:5175
call npm run dev
endlocal
