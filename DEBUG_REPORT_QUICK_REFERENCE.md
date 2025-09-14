# 📋 Debug Report Quick Reference

## **Generate Debug Report**

### **Linux/Mac:**
```bash
./scripts/generate-debug-report.sh
```

### **Windows:**
```cmd
scripts\generate-debug-report.bat
```

## **Report Files Created**

| File | Purpose | When to Use |
|------|---------|-------------|
| `debug_report_YYYYMMDD_HHMMSS.md` | Auto-generated report with system info | After each debug session |
| `DEBUG_REPORT_TEMPLATE.md` | Template for manual report creation | When you need a custom report |
| `DEBUG_GUIDE.md` | Comprehensive debugging guide | Reference during debugging |
| `CURSOR_DEBUG_CHEATSHEET.md` | Quick command reference | While debugging |

## **Report Sections to Fill**

### **Required Sections:**
- [ ] **API Endpoints Status** - Test each endpoint and mark status
- [ ] **Console Logs** - Copy actual console output
- [ ] **Error Tracing** - Document the exact error and line number
- [ ] **Fixes & Actions Taken** - List what you changed
- [ ] **Remaining Issues** - What still needs to be fixed

### **Optional Sections:**
- [ ] **Performance Metrics** - Response times, memory usage
- [ ] **Screenshots** - Console logs, network requests, errors
- [ ] **Environment Details** - OS, versions, dependencies

## **Quick Fill Template**

```markdown
### **API Endpoints Status:**
* [x] **Health Check:** `/health` → [200] - ✅ Working
* [x] **Panchangam API:** `/api/panchangam` → [200] - ✅ Working
* [ ] **Birth Chart API:** `/api/birth-chart` → [404] - ❌ Not found

### **Console Logs Show:**
```
QuickActions props: { onQuick: [Function] }
QuickActions auth state: { isAuthenticated: true, currentProfile: {...} }
handleQuickAction called with: { id: 'panchangam', ... }
```

### **Error Tracing:**
* `"e is not a function"` occurs at line 68 in `QuickActions.jsx`
* Root cause: `onQuick prop is undefined`
* Error stack trace: `TypeError: e is not a function at handleQuickAction`
```

## **Report Workflow**

1. **Before Debugging:**
   - Run `./scripts/generate-debug-report.sh`
   - Note the report filename

2. **During Debugging:**
   - Fill in API endpoint statuses
   - Copy console logs
   - Document errors found
   - Take screenshots if needed

3. **After Debugging:**
   - Fill in fixes applied
   - List remaining issues
   - Add recommendations
   - Update session summary

4. **Share Results:**
   - Send report to team
   - Save for future reference
   - Update documentation if needed

## **Common Placeholders to Replace**

| Placeholder | What to Fill |
|-------------|--------------|
| `{{health_status}}` | 200/404/Error |
| `{{panchangam_status}}` | 200/404/Error |
| `{{props_log}}` | Actual console log output |
| `{{error_line}}` | Line number where error occurs |
| `{{root_cause}}` | Brief description of the issue |
| `{{changes_made}}` | List of code changes |
| `{{priority_issue_1}}` | Most important remaining issue |

## **Pro Tips**

1. **Use the auto-generated report** - It includes system info and environment status
2. **Fill as you debug** - Don't wait until the end to document findings
3. **Take screenshots** - Visual evidence is very helpful
4. **Be specific** - Include exact error messages and line numbers
5. **Update regularly** - Keep the report current as you make changes

## **Example Completed Section**

```markdown
### **API Endpoints Status:**
* [x] **Health Check:** `/health` → [200] - ✅ Working
* [x] **Panchangam API:** `/api/panchangam?date=2025-01-15&location=Chennai` → [200] - ✅ Working
* [x] **Birth Chart API:** `/api/birth-chart` → [200] - ✅ Working
* [ ] **Quick Reading API:** `/api/quick-reading` → [500] - ❌ Internal server error

### **Console Logs Show:**
```
QuickActions props: { onQuick: [Function] }
QuickActions auth state: { isAuthenticated: true, currentProfile: { id: 1, name: "Test User" } }
handleQuickAction called with: { id: 'panchangam', label: 'Panchangam', query: "Show today's Panchangam" }
onQuick function: [Function]
Calling onQuick with query: Show today's Panchangam
```

### **Error Tracing:**
* `"e is not a function"` occurs at line 68 in `QuickActions.jsx`
* Root cause: `onQuick prop is being passed correctly, but there's an issue in the parent component`
* Error stack trace: `TypeError: e is not a function at handleQuickAction (QuickActions.jsx:68)`
```

---

**💡 Remember:** The debug report is your debugging diary - the more detailed, the better!

