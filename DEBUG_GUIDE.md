# AstroOverz Debugging Guide

This guide provides comprehensive debugging instructions for the AstroOverz application using Cursor IDE and VS Code.

## 🚀 Quick Start Debugging

### 1. Backend Debugging (FastAPI)

#### Option A: Using VS Code Debugger
1. Open Command Palette: `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
2. Type: `Debug: Start Debugging`
3. Select: `Debug FastAPI with Uvicorn`
4. Set breakpoints by clicking the left gutter or pressing `F9`

#### Option B: Terminal Debugging
```bash
# Activate virtual environment
. .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate # Mac/Linux

# Start with debug logging
uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### 2. Frontend Debugging (React)

#### Option A: Using VS Code Debugger
1. Open Command Palette: `Ctrl+Shift+P`
2. Type: `Debug: Start Debugging`
3. Select: `Debug React Frontend`

#### Option B: Terminal Debugging
```bash
cd frontend
npm run dev
```

### 3. Full Stack Debugging
1. Open Command Palette: `Ctrl+Shift+P`
2. Type: `Debug: Start Debugging`
3. Select: `Debug Full Stack`

## 🔧 Debug Configurations

### Available Debug Configurations

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| `Debug FastAPI Backend` | Debug main.py directly | Testing specific functions |
| `Debug FastAPI with Uvicorn` | Debug with hot reload | API development |
| `Debug Current Python File` | Debug any Python file | Quick testing |
| `Debug React Frontend` | Debug Vite dev server | Frontend development |
| `Attach to Chrome` | Attach to Chrome DevTools | Advanced frontend debugging |
| `Debug Full Stack` | Debug both backend and frontend | End-to-end debugging |

## 🛠️ Debugging Tools

### 1. REST Client Testing
- File: `api_test.rest`
- Install REST Client extension in VS Code
- Click "Send Request" above any HTTP request
- Test both local and production APIs

### 2. Console Logging
The QuickActions component now includes comprehensive logging:
```javascript
console.log("QuickActions props:", { onQuick });
console.log("QuickActions auth state:", { isAuthenticated, currentProfile });
console.log("handleQuickAction called with:", action);
```

### 3. Browser DevTools
- Press `F12` to open DevTools
- Check Console tab for JavaScript errors
- Check Network tab for API request failures
- Check Sources tab for breakpoints

## 🐛 Common Issues & Solutions

### Issue: "e is not a function" Error
**Symptoms:** JavaScript error in browser console
**Debug Steps:**
1. Check browser console for full error stacktrace
2. Look for undefined function calls in QuickActions
3. Verify `onQuick` prop is being passed correctly
4. Check if component is receiving proper props

**Solution:**
```javascript
// Add this to QuickActions component
console.log("onQuick function type:", typeof onQuick);
if (typeof onQuick !== 'function') {
  console.error("onQuick is not a function:", onQuick);
}
```

### Issue: API 404 Errors
**Symptoms:** Network requests failing with 404
**Debug Steps:**
1. Check Network tab in DevTools
2. Verify API endpoint URLs
3. Test endpoints with REST Client
4. Check backend is running on correct port

**Solution:**
```bash
# Test API directly
curl http://localhost:8000/health
curl http://localhost:8000/api/panchangam?date=2025-01-15&location=Chennai
```

### Issue: Backend Not Starting
**Symptoms:** FastAPI server won't start
**Debug Steps:**
1. Check Python virtual environment is activated
2. Verify all dependencies are installed
3. Check for port conflicts
4. Review error messages in terminal

**Solution:**
```bash
# Check if port is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Kill process if needed
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Mac/Linux
```

## 📋 Debug Checklist

### Before Starting Debug Session
- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Database is running (if using local Postgres)
- [ ] Redis is running (if using caching)
- [ ] No port conflicts (8000 for backend, 5173 for frontend)

### During Debug Session
- [ ] Set breakpoints in critical functions
- [ ] Monitor console logs in both terminal and browser
- [ ] Check Network tab for failed requests
- [ ] Verify API responses with REST Client
- [ ] Test authentication flow if applicable

### After Debug Session
- [ ] Remove debug console.log statements
- [ ] Clean up temporary breakpoints
- [ ] Document any issues found
- [ ] Update this guide if new issues discovered

## 🎯 Specific Debug Scenarios

### Scenario 1: QuickActions Not Working
1. **Check Props:** Look for console logs showing props
2. **Verify Function:** Ensure `onQuick` is a function
3. **Test Click:** Add click handler logging
4. **Check Auth:** Verify authentication state

### Scenario 2: API Calls Failing
1. **Test Endpoint:** Use REST Client to test API
2. **Check CORS:** Verify CORS configuration
3. **Check Headers:** Ensure proper content-type
4. **Check Auth:** Verify authentication tokens

### Scenario 3: Frontend Not Loading
1. **Check Build:** Ensure frontend builds successfully
2. **Check Dev Server:** Verify Vite is running
3. **Check Console:** Look for JavaScript errors
4. **Check Network:** Verify all assets load

## 🔍 Advanced Debugging

### Python Debugging
```python
# Add to any Python file for debugging
import pdb; pdb.set_trace()  # Breakpoint
import logging
logging.basicConfig(level=logging.DEBUG)
```

### JavaScript Debugging
```javascript
// Add to any JavaScript file
debugger;  // Breakpoint (requires DevTools open)
console.trace();  // Stack trace
console.table(data);  // Table view of data
```

### Network Debugging
```bash
# Monitor network traffic
tcpdump -i any port 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows
```

## 📚 Additional Resources

- [VS Code Debugging Documentation](https://code.visualstudio.com/docs/editor/debugging)
- [FastAPI Debugging Guide](https://fastapi.tiangolo.com/tutorial/debugging/)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. Check the console logs (both terminal and browser)
2. Use the REST Client to test API endpoints
3. Set breakpoints and step through the code
4. Check the Network tab for failed requests
5. Verify all environment variables are set correctly

Remember: The key to effective debugging is systematic investigation and good logging!

