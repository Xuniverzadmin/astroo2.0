# 🚀 Cursor IDE Debug Cheatsheet - AstroOverz

## **Essential Keyboard Shortcuts**

| Action | Windows/Linux | Mac | Description |
|--------|---------------|-----|-------------|
| **Open Command Palette** | `Ctrl+Shift+P` | `Cmd+Shift+P` | Access all commands |
| **Start Debugging** | `F5` | `F5` | Launch debugger |
| **Toggle Breakpoint** | `F9` | `F9` | Set/remove breakpoint |
| **Step Over** | `F10` | `F10` | Next line |
| **Step Into** | `F11` | `F11` | Enter function |
| **Continue** | `F5` | `F5` | Resume execution |
| **Stop Debugging** | `Shift+F5` | `Shift+F5` | End debug session |
| **Open Terminal** | `Ctrl+`` | `Cmd+`` | New terminal |
| **Search Project** | `Ctrl+Shift+F` | `Cmd+Shift+F` | Find in files |
| **Find References** | `Shift+F12` | `Shift+F12` | Where used |
| **Format Code** | `Shift+Alt+F` | `Shift+Option+F` | Auto-format |
| **Open DevTools** | `F12` | `F12` | Browser console |

## **Quick Debug Commands (Command Palette)**

Type these in `Ctrl+Shift+P`:

```
Debug: Start Debugging          # Start debugger
Debug: Toggle Breakpoint        # Set/remove breakpoint
Debug: Stop Debugging           # Stop debugger
Python: Select Interpreter      # Choose Python version
Terminal: Create New Terminal   # New terminal
REST Client: Send Request       # Test API endpoints
View: Show Debug Console        # Debug output
View: Toggle Terminal           # Show/hide terminal
View: Open Problems             # Show errors/warnings
```

## **Debug Configurations Available**

| Configuration | Use Case | Shortcut |
|---------------|----------|----------|
| `Debug FastAPI Backend` | Backend only | `F5` → Select |
| `Debug FastAPI with Uvicorn` | Backend with reload | `F5` → Select |
| `Debug React Frontend` | Frontend only | `F5` → Select |
| `Debug Full Stack` | Both services | `F5` → Select |
| `Debug Current Python File` | Quick Python test | `F5` → Select |
| `Attach to Chrome` | Advanced frontend | `F5` → Select |

## **Quick Start Debug Session**

### **Method 1: VS Code Debugger (Recommended)**
1. `F5` → Select `Debug Full Stack`
2. Open browser: `http://localhost:5173`
3. `F12` → Open DevTools
4. Click QuickActions button
5. Check console logs
6. Set breakpoints with `F9`

### **Method 2: Terminal Scripts**
```bash
# Windows
scripts\debug-fullstack.bat

# Linux/Mac
./scripts/debug-fullstack.sh
```

### **Method 3: Manual Commands**
```bash
# Terminal 1: Backend
. .venv/Scripts/activate
uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

## **API Testing with REST Client**

1. Open `api_test.rest`
2. Click "Send Request" above any HTTP line
3. Test endpoints:
   - Health: `GET http://localhost:8000/health`
   - Panchangam: `GET http://localhost:8000/api/panchangam?date=2025-01-15&location=Chennai`

## **Debugging the "e is not a function" Error**

### **Step 1: Check Console Logs**
Open DevTools (`F12`) → Console tab, look for:
```
QuickActions props: { onQuick: [Function] }
QuickActions auth state: { isAuthenticated: true, currentProfile: {...} }
handleQuickAction called with: { id: 'panchangam', ... }
```

### **Step 2: Set Breakpoints**
1. Open `frontend/src/components/QuickActions.jsx`
2. Click left gutter next to line 68 (`const handleQuickAction = (action) => {`)
3. Press `F9` to toggle breakpoint
4. Reload page and click QuickAction button

### **Step 3: Step Through Code**
- `F10` - Step over each line
- `F11` - Step into function calls
- Hover over variables to see values
- Check Debug Console for variable values

### **Step 4: Check API Calls**
1. Open DevTools → Network tab
2. Click QuickAction button
3. Look for failed requests (red entries)
4. Check response status codes

## **Common Issues & Quick Fixes**

| Issue | Quick Fix | Command |
|-------|-----------|---------|
| Port 8000 in use | Kill process | `taskkill /F /IM python.exe` (Windows) |
| Port 5173 in use | Kill process | `taskkill /F /IM node.exe` (Windows) |
| Python not found | Select interpreter | `Ctrl+Shift+P` → `Python: Select Interpreter` |
| Dependencies missing | Install | `pip install -r backend/requirements.txt` |
| Frontend not loading | Check build | `cd frontend && npm run dev` |

## **Pro Tips**

1. **Use Debug Console**: View variable values during debugging
2. **Watch Variables**: Add variables to watch list in debug panel
3. **Conditional Breakpoints**: Right-click breakpoint → Edit Breakpoint
4. **Logpoints**: Add `console.log` without code changes
5. **Exception Breakpoints**: Break on uncaught exceptions
6. **Call Stack**: See function call hierarchy
7. **Scope Variables**: Inspect local/global variables

## **Quick Reference URLs**

- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Frontend**: `http://localhost:5173`
- **Health Check**: `http://localhost:8000/health`

## **Emergency Commands**

```bash
# Kill all Python processes (Windows)
taskkill /F /IM python.exe

# Kill all Node processes (Windows)
taskkill /F /IM node.exe

# Check what's using port 8000 (Windows)
netstat -ano | findstr :8000

# Check what's using port 5173 (Windows)
netstat -ano | findstr :5173
```

---

**💡 Tip**: Keep this cheatsheet open in a separate tab while debugging!

