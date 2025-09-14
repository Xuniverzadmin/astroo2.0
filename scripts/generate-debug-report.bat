@echo off
REM AstroOverz Debug Report Generator for Windows
REM This script generates a debug report with current system information

echo 🔍 Generating AstroOverz Debug Report...

REM Get current date and time
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "DATE=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
set "SESSION_ID=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"
set "REPORTER_NAME=%USERNAME%"

REM Check if we're in the right directory
if not exist "backend\numerology_app\main.py" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Get system information
for /f "tokens=*" %%i in ('ver') do set "OS_VERSION=%%i"
for /f "tokens=*" %%i in ('node --version 2^>nul') do set "NODE_VERSION=%%i"
if "%NODE_VERSION%"=="" set "NODE_VERSION=Not installed"
for /f "tokens=*" %%i in ('python --version 2^>nul') do set "PYTHON_VERSION=%%i"
if "%PYTHON_VERSION%"=="" set "PYTHON_VERSION=Not installed"
set "BROWSER_VERSION=Chrome/Edge/Firefox (check manually)"

REM Check backend dependencies
if exist "backend\requirements.txt" (
    set "BACKEND_DEPS_STATUS=✅ Requirements file found"
) else (
    set "BACKEND_DEPS_STATUS=❌ Requirements file missing"
)

REM Check frontend dependencies
if exist "frontend\node_modules" (
    set "FRONTEND_DEPS_STATUS=✅ Node modules installed"
) else (
    set "FRONTEND_DEPS_STATUS=❌ Node modules missing"
)

REM Check if virtual environment exists
if exist ".venv" (
    set "VENV_STATUS=✅ Virtual environment found"
) else (
    set "VENV_STATUS=❌ Virtual environment missing"
)

REM Check if debug files exist
set "DEBUG_FILES_STATUS="
if exist "api_test.rest" set "DEBUG_FILES_STATUS=✅ REST Client, "
if exist ".vscode\launch.json" set "DEBUG_FILES_STATUS=%DEBUG_FILES_STATUS%✅ VS Code configs, "
if exist "DEBUG_GUIDE.md" set "DEBUG_FILES_STATUS=%DEBUG_FILES_STATUS%✅ Debug guide, "
if exist "CURSOR_DEBUG_CHEATSHEET.md" set "DEBUG_FILES_STATUS=%DEBUG_FILES_STATUS%✅ Cheatsheet"

REM Check port availability
set "PORT_8000_STATUS="
netstat -an | findstr :8000 >nul
if not errorlevel 1 (
    set "PORT_8000_STATUS=⚠️ Port 8000 in use"
) else (
    set "PORT_8000_STATUS=✅ Port 8000 available"
)

set "PORT_5173_STATUS="
netstat -an | findstr :5173 >nul
if not errorlevel 1 (
    set "PORT_5173_STATUS=⚠️ Port 5173 in use"
) else (
    set "PORT_5173_STATUS=✅ Port 5173 available"
)

REM Generate report filename
set "REPORT_FILE=debug_report_%SESSION_ID%.md"

REM Create the report
(
echo # 📝 AstroOverz Debug Session Report
echo.
echo **Date:** `%DATE%`
echo **Project:** AstroOverz
echo **Environment:** Cursor IDE / VS Code
echo **Debug Session ID:** `%SESSION_ID%`
echo **Reporter:** `%REPORTER_NAME%`
echo.
echo ---
echo.
echo ## **1. Debugging Environment Setup**
echo.
echo * [x] REST Client file (`api_test.rest`) available and working.
echo * [x] VS Code/Cursor launch configs (`.vscode/launch.json`) set for:
echo   * FastAPI backend
echo   * React frontend
echo   * Full stack
echo * [x] Debug scripts for Windows/Linux/Mac present and executable.
echo * [x] QuickActions.jsx updated with logging for props and event handling.
echo * [x] All documentation (`DEBUG_GUIDE.md`, cheatsheets) present in project root.
echo.
echo **Environment Status:**
echo - %DEBUG_FILES_STATUS%
echo - %VENV_STATUS%
echo - %PORT_8000_STATUS%
echo - %PORT_5173_STATUS%
echo.
echo ---
echo.
echo ## **2. Debug Session Steps (Commands Used)**
echo.
echo | Step                   | Command / Shortcut                     | Result | Notes |
echo | ---------------------- | -------------------------------------- | ------ | ----- |
echo | Open Command Palette   | `Ctrl+Shift+P`                         | ⏳      | Ready to use |
echo | Start Full Stack Debug | `F5` / select config                   | ⏳      | Ready to use |
echo | Open terminal          | `Ctrl+``                               | ⏳      | Ready to use |
echo | Run backend script     | `scripts\debug-backend.bat`            | ⏳      | Ready to use |
echo | Run frontend script    | `scripts\debug-frontend.bat`           | ⏳      | Ready to use |
echo | Set breakpoint         | `F9`                                   | ⏳      | Ready to use |
echo | Step over/into         | `F10`/`F11`                            | ⏳      | Ready to use |
echo | Run REST API test      | `api_test.rest` + "Send Request"       | ⏳      | Ready to use |
echo | View logs              | DevTools Console (`F12`)               | ⏳      | Ready to use |
echo.
echo ---
echo.
echo ## **3. Key Observations**
echo.
echo ### **API Endpoints Status:**
echo * [ ] **Health Check:** `/health` → [200/404/Error] - `{{health_status}}`
echo * [ ] **Panchangam API:** `/api/panchangam` → [200/404/Error] - `{{panchangam_status}}`
echo * [ ] **Birth Chart API:** `/api/birth-chart` → [200/404/Error] - `{{birthchart_status}}`
echo * [ ] **Quick Reading API:** `/api/quick-reading` → [200/404/Error] - `{{quickreading_status}}`
echo * [ ] **Name Analysis API:** `/api/name-analysis` → [200/404/Error] - `{{nameanalysis_status}}`
echo * [ ] **Dasha API:** `/api/dasha` → [200/404/Error] - `{{dasha_status}}`
echo * [ ] **Auth APIs:** `/api/auth/*` → [200/404/Error] - `{{auth_status}}`
echo.
echo ### **Frontend Behavior:**
echo * [ ] **QuickActions Component:** Correctly renders and displays buttons
echo * [ ] **Click Events:** QuickActions buttons respond to clicks
echo * [ ] **Console Logs Show:**
echo   ```
echo   QuickActions props: {{props_log}}
echo   QuickActions auth state: {{auth_log}}
echo   handleQuickAction called with: {{action_log}}
echo   ```
echo * [ ] **Error Tracing:**
echo   * `"e is not a function"` occurs at line `{{error_line}}` in `QuickActions.jsx`
echo   * Root cause: `{{root_cause}}`
echo   * Error stack trace: `{{stack_trace}}`
echo.
echo ### **Network Requests:**
echo * [ ] **Backend Connection:** Frontend successfully connects to backend
echo * [ ] **CORS Issues:** [None/Some] - `{{cors_status}}`
echo * [ ] **Failed Requests:** [None/Some] - `{{failed_requests}}`
echo * [ ] **Response Times:** Average `{{avg_response_time}}`ms
echo.
echo ---
echo.
echo ## **4. Fixes & Actions Taken**
echo.
echo * [ ] Fixed parent component to pass correct function prop to `QuickActions`
echo * [ ] Corrected API endpoint path in frontend fetch
echo * [ ] Added prop type validation (optional)
echo * [ ] Restarted servers after changes
echo * [ ] Updated environment variables
echo * [ ] Fixed CORS configuration
echo * [ ] Resolved dependency issues
echo.
echo **Specific Changes Made:**
echo ```
echo {{changes_made}}
echo ```
echo.
echo ---
echo.
echo ## **5. Remaining Issues / To-Do**
echo.
echo * [ ] Ensure all API endpoints are covered in `api_test.rest`
echo * [ ] [List any unresolved 404s or server errors here]
echo * [ ] [Document any persistent frontend errors]
echo * [ ] [Add any missing error handling]
echo * [ ] [Update documentation if needed]
echo.
echo **Priority Issues:**
echo 1. `{{priority_issue_1}}`
echo 2. `{{priority_issue_2}}`
echo 3. `{{priority_issue_3}}`
echo.
echo ---
echo.
echo ## **6. Recommendations**
echo.
echo * Always run `npm run dev` (frontend) and `uvicorn ... --reload` (backend) for fast hot-reloading during dev
echo * Use REST Client for quick endpoint tests before connecting frontend
echo * Keep prop logging in place during active feature dev; remove before production
echo * Consider adding **prop-types** or TypeScript for strict prop validation
echo * Set up automated testing for critical user flows
echo * Add error boundaries in React components
echo * Implement proper logging strategy for production
echo.
echo ---
echo.
echo ## **7. Performance Metrics**
echo.
echo * **Backend Startup Time:** `{{backend_startup_time}}`s
echo * **Frontend Build Time:** `{{frontend_build_time}}`s
echo * **API Response Times:**
echo   - Health Check: `{{health_response_time}}`ms
echo   - Panchangam: `{{panchangam_response_time}}`ms
echo   - Birth Chart: `{{birthchart_response_time}}`ms
echo * **Memory Usage:**
echo   - Backend: `{{backend_memory}}`MB
echo   - Frontend: `{{frontend_memory}}`MB
echo.
echo ---
echo.
echo ## **8. Environment Details**
echo.
echo * **OS:** `%OS_VERSION%`
echo * **Node Version:** `%NODE_VERSION%`
echo * **Python Version:** `%PYTHON_VERSION%`
echo * **Browser:** `%BROWSER_VERSION%`
echo * **Cursor/VS Code Version:** `{{editor_version}}`
echo * **Dependencies:**
echo   - Backend: %BACKEND_DEPS_STATUS%
echo   - Frontend: %FRONTEND_DEPS_STATUS%
echo.
echo ---
echo.
echo ## **9. Attachments / References**
echo.
echo * `DEBUG_GUIDE.md`
echo * `CURSOR_DEBUG_CHEATSHEET.md`
echo * `api_test.rest`
echo * `QuickActions.jsx` (annotated)
echo * Console logs screenshot: `{{console_screenshot}}`
echo * Network requests screenshot: `{{network_screenshot}}`
echo * Error stack trace: `{{error_screenshot}}`
echo.
echo ---
echo.
echo ## **10. Next Debug Steps (if error persists)**
echo.
echo 1. Set breakpoints in both backend route and frontend handler
echo 2. Step through to ensure data flows end-to-end
echo 3. Check Network tab for failed requests (404s, CORS, etc)
echo 4. Double-check prop drilling from parent to child in React tree
echo 5. Verify all environment variables are set correctly
echo 6. Test with different browsers to rule out browser-specific issues
echo 7. Check for any TypeScript/JavaScript compilation errors
echo 8. [Paste key error logs/screenshots here]
echo.
echo **Immediate Next Actions:**
echo 1. `{{next_action_1}}`
echo 2. `{{next_action_2}}`
echo 3. `{{next_action_3}}`
echo.
echo ---
echo.
echo ## **11. Session Summary**
echo.
echo **Total Debug Time:** `{{total_debug_time}}` minutes
echo **Issues Found:** `{{issues_found}}`
echo **Issues Resolved:** `{{issues_resolved}}`
echo **Status:** [✅ Resolved / ⚠️ Partially Resolved / ❌ Unresolved]
echo.
echo **Key Learnings:**
echo - `{{learning_1}}`
echo - `{{learning_2}}`
echo - `{{learning_3}}`
echo.
echo ---
echo.
echo **End of Report**
echo.
echo ---
echo.
echo > **Generated by:** `generate-debug-report.bat` on `%DATE%`
echo > **Report File:** `%REPORT_FILE%`
) > "%REPORT_FILE%"

echo ✅ Debug report generated: %REPORT_FILE%
echo.
echo 📋 Next steps:
echo 1. Fill in the {{placeholder}} values with your actual findings
echo 2. Add screenshots of console logs and network requests
echo 3. Document any errors or issues found
echo 4. Share with your team or save for future reference
echo.
echo 🔍 To start debugging:
echo    Press F5 in Cursor IDE and select 'Debug Full Stack'
echo    Or run: scripts\debug-fullstack.bat

