# Quick Start Guide

## 5-Minute Setup

### Terminal 1: Start Server

```bash
cd code-review-app

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║          Code Review & Analysis Tool - MCP Server            ║
╠══════════════════════════════════════════════════════════════╣
║  Server: http://0.0.0.0:8001                                 ║
║  Status: Running                                             ║
╚══════════════════════════════════════════════════════════════╝
```

### Terminal 2: Start ngrok

```bash
ngrok http 8001
```

Copy the **Forwarding** HTTPS URL:
```
Forwarding: https://abc123.ngrok-free.app -> http://localhost:8001
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            Copy this URL
```

### Browser: Register in ChatGPT

1. Go to https://chatgpt.com/apps
2. Click ⚙️ Settings → Enable "Developer mode"
3. Click "Create app"
4. Enter:
   ```
   Name: Code Review Tool
   MCP Server URL: https://YOUR-NGROK-URL/mcp
   Authentication: No Auth
   ```
5. Check "I understand and want to continue"
6. Click "Create"

### Test in ChatGPT

Start a new conversation and try:

```
@Code Review Tool analyze this code:

function processData(data) {
  var result = eval(data);
  return result;
}
```

You should see an interactive widget with the code review results!

## Example Prompts

### Code Analysis
```
@Code Review Tool analyze this JavaScript code:
function fetchUser(id) {
  fetch('/api/user/' + id)
    .then(res => res.json())
    .then(data => console.log(data))
}
```

### Security Scan
```
@Code Review Tool perform a security scan on:
const query = "SELECT * FROM users WHERE id = " + userId;
db.execute(query);
```

### Multiple Languages
```
@Code Review Tool analyze this Python code:
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```

## Widget Actions

After reviewing code, use the action buttons:

- **💡 Explain All Issues**: Get detailed explanations of each issue
- **🔧 Suggest Fixes**: Generate corrected code
- **📚 Show Best Practices**: Learn recommended patterns

## Troubleshooting

### "Tool not found"
- Verify server is running (Terminal 1)
- Check ngrok is active (Terminal 2)
- Confirm app is registered in ChatGPT settings

### Widget shows "Loading..."
- Delete app in ChatGPT settings
- Stop both server and ngrok
- Start fresh with new ngrok URL
- Re-register app

### No widget appears
- Try in a new ChatGPT conversation
- Check browser console for errors
- Verify `_meta` is included in server response

## Next Steps

1. ✅ Test basic code analysis
2. ✅ Try security scanning
3. ✅ Use widget action buttons
4. 📖 Read full README.md for customization options
5. 🔧 Extend analysis patterns in main.py

## Pro Tips

- **Cache Issues**: If widget doesn't update, use a fresh ngrok URL
- **Testing**: Use ngrok web interface at http://127.0.0.1:4040 to inspect requests
- **Logs**: Watch Terminal 1 for server logs and errors
- **Multiple Tests**: Open multiple ChatGPT conversations for parallel testing
