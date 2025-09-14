#!/bin/bash

# AstroOverz Debug Report Generator
# This script generates a debug report with current system information

echo "🔍 Generating AstroOverz Debug Report..."

# Get current date and time
DATE=$(date '+%Y-%m-%d %H:%M:%S')
SESSION_ID=$(date '+%Y%m%d_%H%M%S')
REPORTER_NAME=${USER:-"Unknown"}

# Get system information
OS_VERSION=$(uname -a)
NODE_VERSION=$(node --version 2>/dev/null || echo "Not installed")
PYTHON_VERSION=$(python --version 2>/dev/null || echo "Not installed")
BROWSER_VERSION="Chrome/Edge/Firefox (check manually)"

# Check if we're in the right directory
if [ ! -f "backend/numerology_app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check backend dependencies
if [ -f "backend/requirements.txt" ]; then
    BACKEND_DEPS_STATUS="✅ Requirements file found"
else
    BACKEND_DEPS_STATUS="❌ Requirements file missing"
fi

# Check frontend dependencies
if [ -d "frontend/node_modules" ]; then
    FRONTEND_DEPS_STATUS="✅ Node modules installed"
else
    FRONTEND_DEPS_STATUS="❌ Node modules missing"
fi

# Check if virtual environment exists
if [ -d ".venv" ]; then
    VENV_STATUS="✅ Virtual environment found"
else
    VENV_STATUS="❌ Virtual environment missing"
fi

# Check if debug files exist
DEBUG_FILES_STATUS=""
if [ -f "api_test.rest" ]; then
    DEBUG_FILES_STATUS+="✅ REST Client, "
fi
if [ -f ".vscode/launch.json" ]; then
    DEBUG_FILES_STATUS+="✅ VS Code configs, "
fi
if [ -f "DEBUG_GUIDE.md" ]; then
    DEBUG_FILES_STATUS+="✅ Debug guide, "
fi
if [ -f "CURSOR_DEBUG_CHEATSHEET.md" ]; then
    DEBUG_FILES_STATUS+="✅ Cheatsheet"
fi

# Check port availability
PORT_8000_STATUS=""
if lsof -i :8000 >/dev/null 2>&1; then
    PORT_8000_STATUS="⚠️ Port 8000 in use"
else
    PORT_8000_STATUS="✅ Port 8000 available"
fi

PORT_5173_STATUS=""
if lsof -i :5173 >/dev/null 2>&1; then
    PORT_5173_STATUS="⚠️ Port 5173 in use"
else
    PORT_5173_STATUS="✅ Port 5173 available"
fi

# Generate report filename
REPORT_FILE="debug_report_${SESSION_ID}.md"

# Create the report
cat > "$REPORT_FILE" << EOF
# 📝 AstroOverz Debug Session Report

**Date:** \`$DATE\`
**Project:** AstroOverz
**Environment:** Cursor IDE / VS Code
**Debug Session ID:** \`$SESSION_ID\`
**Reporter:** \`$REPORTER_NAME\`

---

## **1. Debugging Environment Setup**

* [x] REST Client file (\`api_test.rest\`) available and working.
* [x] VS Code/Cursor launch configs (\`.vscode/launch.json\`) set for:
  * FastAPI backend
  * React frontend
  * Full stack
* [x] Debug scripts for Windows/Linux/Mac present and executable.
* [x] QuickActions.jsx updated with logging for props and event handling.
* [x] All documentation (\`DEBUG_GUIDE.md\`, cheatsheets) present in project root.

**Environment Status:**
- $DEBUG_FILES_STATUS
- $VENV_STATUS
- $PORT_8000_STATUS
- $PORT_5173_STATUS

---

## **2. Debug Session Steps (Commands Used)**

| Step                   | Command / Shortcut                     | Result | Notes |
| ---------------------- | -------------------------------------- | ------ | ----- |
| Open Command Palette   | \`Ctrl+Shift+P\`                         | ⏳      | Ready to use |
| Start Full Stack Debug | \`F5\` / select config                   | ⏳      | Ready to use |
| Open terminal          | \`Ctrl+\`\`                               | ⏳      | Ready to use |
| Run backend script     | \`./scripts/debug-backend.sh\` / \`.bat\`  | ⏳      | Ready to use |
| Run frontend script    | \`./scripts/debug-frontend.sh\` / \`.bat\` | ⏳      | Ready to use |
| Set breakpoint         | \`F9\`                                   | ⏳      | Ready to use |
| Step over/into         | \`F10\`/\`F11\`                            | ⏳      | Ready to use |
| Run REST API test      | \`api_test.rest\` + "Send Request"       | ⏳      | Ready to use |
| View logs              | DevTools Console (\`F12\`)               | ⏳      | Ready to use |

---

## **3. Key Observations**

### **API Endpoints Status:**
* [ ] **Health Check:** \`/health\` → [200/404/Error] - \`{{health_status}}\`
* [ ] **Panchangam API:** \`/api/panchangam\` → [200/404/Error] - \`{{panchangam_status}}\`
* [ ] **Birth Chart API:** \`/api/birth-chart\` → [200/404/Error] - \`{{birthchart_status}}\`
* [ ] **Quick Reading API:** \`/api/quick-reading\` → [200/404/Error] - \`{{quickreading_status}}\`
* [ ] **Name Analysis API:** \`/api/name-analysis\` → [200/404/Error] - \`{{nameanalysis_status}}\`
* [ ] **Dasha API:** \`/api/dasha\` → [200/404/Error] - \`{{dasha_status}}\`
* [ ] **Auth APIs:** \`/api/auth/*\` → [200/404/Error] - \`{{auth_status}}\`

### **Frontend Behavior:**
* [ ] **QuickActions Component:** Correctly renders and displays buttons
* [ ] **Click Events:** QuickActions buttons respond to clicks
* [ ] **Console Logs Show:**
  \`\`\`
  QuickActions props: {{props_log}}
  QuickActions auth state: {{auth_log}}
  handleQuickAction called with: {{action_log}}
  \`\`\`
* [ ] **Error Tracing:**
  * \`"e is not a function"\` occurs at line \`{{error_line}}\` in \`QuickActions.jsx\`
  * Root cause: \`{{root_cause}}\`
  * Error stack trace: \`{{stack_trace}}\`

### **Network Requests:**
* [ ] **Backend Connection:** Frontend successfully connects to backend
* [ ] **CORS Issues:** [None/Some] - \`{{cors_status}}\`
* [ ] **Failed Requests:** [None/Some] - \`{{failed_requests}}\`
* [ ] **Response Times:** Average \`{{avg_response_time}}\`ms

---

## **4. Fixes & Actions Taken**

* [ ] Fixed parent component to pass correct function prop to \`QuickActions\`
* [ ] Corrected API endpoint path in frontend fetch
* [ ] Added prop type validation (optional)
* [ ] Restarted servers after changes
* [ ] Updated environment variables
* [ ] Fixed CORS configuration
* [ ] Resolved dependency issues

**Specific Changes Made:**
\`\`\`
{{changes_made}}
\`\`\`

---

## **5. Remaining Issues / To-Do**

* [ ] Ensure all API endpoints are covered in \`api_test.rest\`
* [ ] [List any unresolved 404s or server errors here]
* [ ] [Document any persistent frontend errors]
* [ ] [Add any missing error handling]
* [ ] [Update documentation if needed]

**Priority Issues:**
1. \`{{priority_issue_1}}\`
2. \`{{priority_issue_2}}\`
3. \`{{priority_issue_3}}\`

---

## **6. Recommendations**

* Always run \`npm run dev\` (frontend) and \`uvicorn ... --reload\` (backend) for fast hot-reloading during dev
* Use REST Client for quick endpoint tests before connecting frontend
* Keep prop logging in place during active feature dev; remove before production
* Consider adding **prop-types** or TypeScript for strict prop validation
* Set up automated testing for critical user flows
* Add error boundaries in React components
* Implement proper logging strategy for production

---

## **7. Performance Metrics**

* **Backend Startup Time:** \`{{backend_startup_time}}\`s
* **Frontend Build Time:** \`{{frontend_build_time}}\`s
* **API Response Times:**
  - Health Check: \`{{health_response_time}}\`ms
  - Panchangam: \`{{panchangam_response_time}}\`ms
  - Birth Chart: \`{{birthchart_response_time}}\`ms
* **Memory Usage:**
  - Backend: \`{{backend_memory}}\`MB
  - Frontend: \`{{frontend_memory}}\`MB

---

## **8. Environment Details**

* **OS:** \`$OS_VERSION\`
* **Node Version:** \`$NODE_VERSION\`
* **Python Version:** \`$PYTHON_VERSION\`
* **Browser:** \`$BROWSER_VERSION\`
* **Cursor/VS Code Version:** \`{{editor_version}}\`
* **Dependencies:**
  - Backend: $BACKEND_DEPS_STATUS
  - Frontend: $FRONTEND_DEPS_STATUS

---

## **9. Attachments / References**

* \`DEBUG_GUIDE.md\`
* \`CURSOR_DEBUG_CHEATSHEET.md\`
* \`api_test.rest\`
* \`QuickActions.jsx\` (annotated)
* Console logs screenshot: \`{{console_screenshot}}\`
* Network requests screenshot: \`{{network_screenshot}}\`
* Error stack trace: \`{{error_screenshot}}\`

---

## **10. Next Debug Steps (if error persists)**

1. Set breakpoints in both backend route and frontend handler
2. Step through to ensure data flows end-to-end
3. Check Network tab for failed requests (404s, CORS, etc)
4. Double-check prop drilling from parent to child in React tree
5. Verify all environment variables are set correctly
6. Test with different browsers to rule out browser-specific issues
7. Check for any TypeScript/JavaScript compilation errors
8. [Paste key error logs/screenshots here]

**Immediate Next Actions:**
1. \`{{next_action_1}}\`
2. \`{{next_action_2}}\`
3. \`{{next_action_3}}\`

---

## **11. Session Summary**

**Total Debug Time:** \`{{total_debug_time}}\` minutes
**Issues Found:** \`{{issues_found}}\`
**Issues Resolved:** \`{{issues_resolved}}\`
**Status:** [✅ Resolved / ⚠️ Partially Resolved / ❌ Unresolved]

**Key Learnings:**
- \`{{learning_1}}\`
- \`{{learning_2}}\`
- \`{{learning_3}}\`

---

**End of Report**

---

> **Generated by:** \`generate-debug-report.sh\` on \`$DATE\`
> **Report File:** \`$REPORT_FILE\`
EOF

echo "✅ Debug report generated: $REPORT_FILE"
echo ""
echo "📋 Next steps:"
echo "1. Fill in the {{placeholder}} values with your actual findings"
echo "2. Add screenshots of console logs and network requests"
echo "3. Document any errors or issues found"
echo "4. Share with your team or save for future reference"
echo ""
echo "🔍 To start debugging:"
echo "   Press F5 in Cursor IDE and select 'Debug Full Stack'"
echo "   Or run: ./scripts/debug-fullstack.sh"

