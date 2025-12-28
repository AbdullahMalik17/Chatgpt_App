"""
Code Review and Analysis Tool - MCP Server
Provides comprehensive code analysis with interactive widget visualization
"""

import os
import json
from typing import Optional
from dotenv import load_dotenv
import mcp.types as types
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Widget MIME type for ChatGPT
MIME_TYPE = "text/html+skybridge"

# Code Review Widget HTML
CODE_REVIEW_WIDGET = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Code Review Results</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 24px;
      color: #333;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
    }

    .card {
      background: rgba(255, 255, 255, 0.98);
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      overflow: hidden;
      margin-bottom: 20px;
    }

    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 24px;
      border-bottom: 3px solid rgba(255, 255, 255, 0.2);
    }

    .header h1 {
      font-size: 28px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .header p {
      opacity: 0.95;
      font-size: 14px;
    }

    .content {
      padding: 24px;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .stat-card {
      background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
      padding: 16px;
      border-radius: 12px;
      text-align: center;
      border: 2px solid transparent;
      transition: all 0.3s ease;
    }

    .stat-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .stat-card.error {
      border-color: #dc3545;
      background: linear-gradient(135deg, #ffe5e5 0%, #ffd4d4 100%);
    }

    .stat-card.warning {
      border-color: #ffc107;
      background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
    }

    .stat-card.info {
      border-color: #17a2b8;
      background: linear-gradient(135deg, #e0f7ff 0%, #b3e5fc 100%);
    }

    .stat-number {
      font-size: 36px;
      font-weight: bold;
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 14px;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .code-section {
      background: #282c34;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
      overflow-x: auto;
    }

    .code-header {
      color: #abb2bf;
      font-size: 12px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #3e4451;
    }

    .code-block {
      font-family: 'Monaco', 'Courier New', monospace;
      font-size: 14px;
      line-height: 1.6;
      color: #abb2bf;
    }

    .code-line {
      display: flex;
      gap: 16px;
    }

    .line-number {
      color: #5c6370;
      user-select: none;
      min-width: 40px;
      text-align: right;
    }

    .line-content {
      flex: 1;
    }

    .issues-section {
      margin-bottom: 24px;
    }

    .issue-card {
      background: white;
      border-left: 4px solid;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .issue-card.error {
      border-left-color: #dc3545;
      background: #fff5f5;
    }

    .issue-card.warning {
      border-left-color: #ffc107;
      background: #fffbf0;
    }

    .issue-card.info {
      border-left-color: #17a2b8;
      background: #f0f9ff;
    }

    .issue-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }

    .issue-badge {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .issue-badge.error {
      background: #dc3545;
      color: white;
    }

    .issue-badge.warning {
      background: #ffc107;
      color: #333;
    }

    .issue-badge.info {
      background: #17a2b8;
      color: white;
    }

    .issue-title {
      font-weight: 600;
      flex: 1;
    }

    .issue-line {
      color: #666;
      font-size: 12px;
      background: rgba(0, 0, 0, 0.05);
      padding: 2px 8px;
      border-radius: 4px;
    }

    .issue-description {
      color: #555;
      line-height: 1.6;
      margin-bottom: 12px;
    }

    .action-buttons {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    .btn {
      background: #667eea;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn:hover {
      background: #5568d3;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
      background: #6c757d;
    }

    .btn-secondary:hover {
      background: #5a6268;
    }

    .btn-success {
      background: #28a745;
    }

    .btn-success:hover {
      background: #218838;
    }

    .no-issues {
      text-align: center;
      padding: 40px;
      color: #28a745;
    }

    .no-issues h2 {
      font-size: 48px;
      margin-bottom: 16px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div class="header">
        <h1>
          <span>🔍</span>
          Code Review Results
        </h1>
        <p>Comprehensive analysis with security and quality insights</p>
      </div>

      <div class="content">
        <div class="summary" id="summary">
          <!-- Summary stats will be injected here -->
        </div>

        <div class="code-section" id="codeSection" style="display: none;">
          <div class="code-header">Analyzed Code</div>
          <div class="code-block" id="codeBlock"></div>
        </div>

        <div class="issues-section" id="issuesSection">
          <!-- Issues will be injected here -->
        </div>

        <div class="action-buttons">
          <button class="btn" id="explainBtn">
            💡 Explain All Issues
          </button>
          <button class="btn btn-success" id="fixBtn">
            🔧 Suggest Fixes
          </button>
          <button class="btn btn-secondary" id="bestPracticesBtn">
            📚 Show Best Practices
          </button>
        </div>
      </div>
    </div>
  </div>

  <script>
    // Parse structured data from ChatGPT (example structure)
    const reviewData = {
      code: `function processData(data) {
  var result = eval(data);
  return result;
}`,
      issues: [
        {
          severity: 'error',
          line: 2,
          title: 'Security Vulnerability: eval() Usage',
          description: 'Using eval() is extremely dangerous as it executes arbitrary code. This creates a code injection vulnerability.'
        },
        {
          severity: 'warning',
          line: 1,
          title: 'Variable Declaration: Use const/let',
          description: 'var is function-scoped and can lead to unexpected behavior. Use const or let for block-scoped variables.'
        },
        {
          severity: 'info',
          line: 1,
          title: 'Missing JSDoc Documentation',
          description: 'Function lacks documentation describing parameters, return value, and purpose.'
        }
      ]
    };

    // Render summary statistics
    function renderSummary(issues) {
      const errors = issues.filter(i => i.severity === 'error').length;
      const warnings = issues.filter(i => i.severity === 'warning').length;
      const info = issues.filter(i => i.severity === 'info').length;

      const summaryHTML = `
        <div class="stat-card error">
          <div class="stat-number">${errors}</div>
          <div class="stat-label">Errors</div>
        </div>
        <div class="stat-card warning">
          <div class="stat-number">${warnings}</div>
          <div class="stat-label">Warnings</div>
        </div>
        <div class="stat-card info">
          <div class="stat-number">${info}</div>
          <div class="stat-label">Suggestions</div>
        </div>
      `;

      document.getElementById('summary').innerHTML = summaryHTML;
    }

    // Render code with line numbers
    function renderCode(code) {
      if (!code) return;

      const lines = code.split('\\n');
      const codeHTML = lines.map((line, idx) => `
        <div class="code-line">
          <span class="line-number">${idx + 1}</span>
          <span class="line-content">${escapeHtml(line)}</span>
        </div>
      `).join('');

      document.getElementById('codeBlock').innerHTML = codeHTML;
      document.getElementById('codeSection').style.display = 'block';
    }

    // Render issues
    function renderIssues(issues) {
      if (issues.length === 0) {
        document.getElementById('issuesSection').innerHTML = `
          <div class="no-issues">
            <h2>✅</h2>
            <p>No issues found! Code looks great.</p>
          </div>
        `;
        return;
      }

      const issuesHTML = issues.map(issue => `
        <div class="issue-card ${issue.severity}">
          <div class="issue-header">
            <span class="issue-badge ${issue.severity}">${issue.severity}</span>
            <span class="issue-title">${escapeHtml(issue.title)}</span>
            <span class="issue-line">Line ${issue.line}</span>
          </div>
          <div class="issue-description">${escapeHtml(issue.description)}</div>
        </div>
      `).join('');

      document.getElementById('issuesSection').innerHTML = issuesHTML;
    }

    // Utility: Escape HTML
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // Initialize widget
    renderSummary(reviewData.issues);
    renderCode(reviewData.code);
    renderIssues(reviewData.issues);

    // Action button handlers using sendFollowUpMessage
    document.getElementById('explainBtn')?.addEventListener('click', async () => {
      if (window.openai?.sendFollowUpMessage) {
        await window.openai.sendFollowUpMessage({
          prompt: 'Explain all the issues found in detail and why they matter'
        });
      }
    });

    document.getElementById('fixBtn')?.addEventListener('click', async () => {
      if (window.openai?.sendFollowUpMessage) {
        await window.openai.sendFollowUpMessage({
          prompt: 'Provide fixed code addressing all identified issues'
        });
      }
    });

    document.getElementById('bestPracticesBtn')?.addEventListener('click', async () => {
      if (window.openai?.sendFollowUpMessage) {
        await window.openai.sendFollowUpMessage({
          prompt: 'Show best practices and design patterns relevant to this code'
        });
      }
    });
  </script>
</body>
</html>'''

# Widget registry
WIDGETS = {
    "code-review": {
        "uri": "ui://widget/code-review.html",
        "html": CODE_REVIEW_WIDGET,
        "title": "Code Review Dashboard",
    },
}

# Create FastMCP server
mcp = FastMCP("Code Review Tool")


@mcp.resource(
    uri="ui://widget/{widget_name}.html",
    name="Widget Resource",
    mime_type=MIME_TYPE
)
def widget_resource(widget_name: str) -> str:
    """Serve widget HTML for code review visualization."""
    if widget_name in WIDGETS:
        return WIDGETS[widget_name]["html"]
    return WIDGETS["code-review"]["html"]


def _embedded_widget_resource(widget_id: str) -> types.EmbeddedResource:
    """Create embedded widget resource for tool response."""
    widget = WIDGETS[widget_id]
    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=widget["uri"],
            mimeType=MIME_TYPE,
            text=widget["html"],
            title=widget["title"],
        ),
    )


def listing_meta() -> dict:
    """Tool metadata for ChatGPT tool listing."""
    return {
        "openai.com/widget": {
            "uri": WIDGETS["code-review"]["uri"],
            "title": WIDGETS["code-review"]["title"]
        }
    }


def response_meta() -> dict:
    """Response metadata with embedded widget."""
    return {
        "openai.com/widget": _embedded_widget_resource("code-review")
    }


def analyze_code_quality(code: str, language: str) -> dict:
    """
    Analyze code for common issues, security vulnerabilities, and best practices.
    This is a simplified analysis - in production, integrate with OpenAI API.
    """
    issues = []

    # Basic pattern-based analysis (placeholder for actual AI analysis)
    if 'eval(' in code:
        issues.append({
            'severity': 'error',
            'line': code.split('\n').index([l for l in code.split('\n') if 'eval(' in l][0]) + 1 if any('eval(' in l for l in code.split('\n')) else 1,
            'title': 'Security Vulnerability: eval() Usage',
            'description': 'Using eval() is extremely dangerous as it executes arbitrary code. This creates a code injection vulnerability.'
        })

    if 'var ' in code and language.lower() in ['javascript', 'typescript']:
        for idx, line in enumerate(code.split('\n'), 1):
            if 'var ' in line:
                issues.append({
                    'severity': 'warning',
                    'line': idx,
                    'title': 'Variable Declaration: Use const/let',
                    'description': 'var is function-scoped and can lead to unexpected behavior. Use const or let for block-scoped variables.'
                })
                break

    # Check for missing error handling
    if 'try' not in code and ('fetch(' in code or 'await' in code):
        issues.append({
            'severity': 'warning',
            'line': 1,
            'title': 'Missing Error Handling',
            'description': 'Asynchronous operations should be wrapped in try-catch blocks to handle potential errors.'
        })

    # Check for documentation
    if '/**' not in code and 'function' in code:
        issues.append({
            'severity': 'info',
            'line': 1,
            'title': 'Missing JSDoc Documentation',
            'description': 'Function lacks documentation describing parameters, return value, and purpose.'
        })

    return {
        'code': code,
        'language': language,
        'issues': issues,
        'total_issues': len(issues),
        'errors': len([i for i in issues if i['severity'] == 'error']),
        'warnings': len([i for i in issues if i['severity'] == 'warning']),
        'suggestions': len([i for i in issues if i['severity'] == 'info']),
    }


@mcp.tool(
    annotations={
        "title": "Analyze Code",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    _meta=listing_meta(),
)
def analyze_code(
    code: str,
    language: str = "javascript"
) -> types.CallToolResult:
    """
    Analyze code for quality issues, security vulnerabilities, and best practices.

    Args:
        code: The source code to analyze
        language: Programming language (javascript, python, etc.)

    Returns:
        Comprehensive code review with interactive widget visualization
    """

    analysis = analyze_code_quality(code, language)

    # Format text summary
    summary_text = f"""Code Analysis Complete

Language: {language}
Total Issues: {analysis['total_issues']}
- Errors: {analysis['errors']}
- Warnings: {analysis['warnings']}
- Suggestions: {analysis['suggestions']}

Review the interactive widget below for detailed results."""

    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text=summary_text
            )
        ],
        structuredContent=analysis,
        _meta=response_meta(),
    )


@mcp.tool(
    annotations={
        "title": "Security Scan",
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def security_scan(code: str, language: str = "javascript") -> types.CallToolResult:
    """
    Perform security-focused analysis of code to identify vulnerabilities.

    Args:
        code: The source code to scan
        language: Programming language

    Returns:
        Security vulnerability report
    """

    vulnerabilities = []

    # Security pattern checks
    security_patterns = {
        'eval(': 'Code Injection Risk',
        'innerHTML': 'XSS Vulnerability',
        'document.write': 'XSS Vulnerability',
        'exec(': 'Command Injection Risk',
        'MD5': 'Weak Cryptographic Hash',
        'SHA1': 'Weak Cryptographic Hash',
    }

    for pattern, risk in security_patterns.items():
        if pattern in code:
            for idx, line in enumerate(code.split('\n'), 1):
                if pattern in line:
                    vulnerabilities.append({
                        'severity': 'error',
                        'line': idx,
                        'title': f'Security: {risk}',
                        'description': f'Pattern "{pattern}" detected. This may introduce security vulnerabilities.'
                    })

    result = {
        'code': code,
        'language': language,
        'issues': vulnerabilities,
        'total_issues': len(vulnerabilities),
        'errors': len(vulnerabilities),
        'warnings': 0,
        'suggestions': 0,
    }

    summary = f"""Security Scan Complete

Vulnerabilities Found: {len(vulnerabilities)}

{'⚠️ Critical security issues detected!' if vulnerabilities else '✅ No obvious security vulnerabilities found.'}"""

    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text=summary
            )
        ],
        structuredContent=result,
        _meta=response_meta(),
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║          Code Review & Analysis Tool - MCP Server            ║
╠══════════════════════════════════════════════════════════════╣
║  Server: http://{host}:{port}                              ║
║  Status: Running                                             ║
║                                                              ║
║  Next Steps:                                                 ║
║  1. Start ngrok: ngrok http {port}                           ║
║  2. Copy ngrok URL                                           ║
║  3. Register in ChatGPT: https://chatgpt.com/apps           ║
║     MCP URL: https://YOUR-NGROK-URL/mcp                     ║
╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "main:mcp.app",
        host=host,
        port=port,
        reload=True
    )
