# Code Review and Analysis Tool

A ChatGPT App that provides comprehensive code analysis with interactive widget visualization.

## Features

- **Code Quality Analysis**: Identify common code issues and anti-patterns
- **Security Scanning**: Detect potential security vulnerabilities
- **Interactive Widget**: Visual code review dashboard with syntax highlighting
- **Action Buttons**: Generate explanations, fixes, and best practices
- **Multi-Language Support**: JavaScript, Python, and more

## Architecture

```
ChatGPT Interface
       ↓
Interactive Widget (HTML/CSS/JS)
       ↓
MCP Server (FastMCP + Python)
       ↓
Code Analysis Engine
```

## Prerequisites

- Python 3.12+
- ngrok account (for exposing local server)
- ChatGPT Plus/Team/Enterprise account

## Installation

1. **Install Python Dependencies**
   ```bash
   cd code-review-app
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key if needed
   ```

## Running the Application

### Step 1: Start the MCP Server

```bash
python main.py
```

Server will start on `http://localhost:8001`

### Step 2: Expose via ngrok

In a separate terminal:

```bash
ngrok http 8001
```

Copy the HTTPS forwarding URL (e.g., `https://abc123.ngrok-free.app`)

### Step 3: Register in ChatGPT

1. Navigate to [ChatGPT Apps](https://chatgpt.com/apps)
2. Click Settings (gear icon) → Enable **Developer mode**
3. Click **Create app**
4. Fill in:
   - **Name**: Code Review Tool
   - **MCP Server URL**: `https://YOUR-NGROK-URL/mcp`
   - **Authentication**: No Auth
5. Click **Create**

### Step 4: Test the Application

1. Start a new chat in ChatGPT
2. Type `@Code Review Tool`
3. Use the `analyze_code` or `security_scan` tools
4. View results in the interactive widget

## Available Tools

### analyze_code

Comprehensive code analysis including:
- Code quality issues
- Best practice violations
- Documentation gaps
- Common anti-patterns

**Usage:**
```
@Code Review Tool analyze this code:
function processData(data) {
  var result = eval(data);
  return result;
}
```

### security_scan

Security-focused vulnerability detection:
- Code injection risks
- XSS vulnerabilities
- Weak cryptographic functions
- Command injection patterns

**Usage:**
```
@Code Review Tool perform security scan on:
<your code here>
```

## Widget Features

The interactive widget provides:

- **Summary Statistics**: Error, warning, and suggestion counts
- **Code Display**: Syntax-highlighted code with line numbers
- **Issue Cards**: Detailed issue descriptions with severity levels
- **Action Buttons**:
  - 💡 Explain All Issues
  - 🔧 Suggest Fixes
  - 📚 Show Best Practices

## Development

### Project Structure

```
code-review-app/
├── main.py              # MCP server with FastMCP
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

### Extending Analysis

To add custom analysis patterns, modify the `analyze_code_quality()` function in `main.py`:

```python
def analyze_code_quality(code: str, language: str) -> dict:
    issues = []

    # Add your custom patterns here
    if 'your_pattern' in code:
        issues.append({
            'severity': 'error',  # or 'warning', 'info'
            'line': 1,
            'title': 'Your Issue Title',
            'description': 'Detailed explanation...'
        })

    return {...}
```

## Troubleshooting

### Widget Not Displaying

1. Check server logs for errors
2. Verify ngrok tunnel is active
3. Delete and recreate the app in ChatGPT settings
4. Use a fresh ngrok URL

### Tools Not Appearing

1. Ensure MCP server is running
2. Verify URL is accessible: `curl https://YOUR-NGROK-URL/mcp`
3. Check ChatGPT app configuration
4. Try in a new conversation

### Cached Widget

ChatGPT caches widgets aggressively. To force refresh:
1. Delete the app in Settings
2. Stop server and ngrok
3. Start with new ngrok URL
4. Create new app registration

## Learning Objectives

This application demonstrates:

1. **MCP Server Architecture**: FastMCP framework patterns
2. **Widget Integration**: HTML widgets with `window.openai` API
3. **Tool Design**: Creating effective ChatGPT tools
4. **Response Metadata**: Embedding widgets in tool responses
5. **Interactive UI**: Action buttons with `sendFollowUpMessage`

## Next Steps

- Integrate OpenAI API for advanced analysis
- Add support for more programming languages
- Implement automated fix generation
- Add configuration for custom analysis rules
- Deploy to production server

## References

- [ChatGPT Apps Documentation](https://platform.openai.com/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
