"""
Enhanced widget templates for code review visualization.
Provides improved UI/UX with modern design patterns.
"""

# Enhanced widget HTML with improved styling and functionality
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
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 24px;
      color: #2d3748;
    }

    .container {
      max-width: 960px;
      margin: 0 auto;
    }

    .card {
      background: rgba(255, 255, 255, 0.98);
      border-radius: 20px;
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3);
      overflow: hidden;
      margin-bottom: 20px;
      backdrop-filter: blur(10px);
    }

    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 32px;
      border-bottom: 4px solid rgba(255, 255, 255, 0.2);
    }

    .header h1 {
      font-size: 32px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 16px;
      font-weight: 700;
    }

    .header p {
      opacity: 0.95;
      font-size: 16px;
      line-height: 1.6;
    }

    .content {
      padding: 32px;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }

    .stat-card {
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      padding: 24px;
      border-radius: 16px;
      text-align: center;
      border: 3px solid transparent;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
    }

    .stat-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, transparent, currentColor, transparent);
      opacity: 0;
      transition: opacity 0.3s;
    }

    .stat-card:hover {
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }

    .stat-card:hover::before {
      opacity: 1;
    }

    .stat-card.error {
      border-color: #dc3545;
      background: linear-gradient(135deg, #ffe5e5 0%, #ffd4d4 100%);
      color: #dc3545;
    }

    .stat-card.warning {
      border-color: #ffc107;
      background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
      color: #f57c00;
    }

    .stat-card.info {
      border-color: #17a2b8;
      background: linear-gradient(135deg, #e0f7ff 0%, #b3e5fc 100%);
      color: #0277bd;
    }

    .stat-number {
      font-size: 48px;
      font-weight: 800;
      margin-bottom: 8px;
      line-height: 1;
    }

    .stat-label {
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      opacity: 0.8;
    }

    .code-section {
      background: #1e1e1e;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 32px;
      overflow-x: auto;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    .code-header {
      color: #9cdcfe;
      font-size: 13px;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 2px solid #3e4451;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    .code-block {
      font-family: 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace;
      font-size: 14px;
      line-height: 1.8;
      color: #d4d4d4;
    }

    .code-line {
      display: flex;
      gap: 20px;
      transition: background 0.2s;
    }

    .code-line:hover {
      background: rgba(255, 255, 255, 0.05);
    }

    .line-number {
      color: #858585;
      user-select: none;
      min-width: 50px;
      text-align: right;
      font-weight: 500;
    }

    .line-content {
      flex: 1;
      word-break: break-all;
    }

    .issues-section {
      margin-bottom: 32px;
    }

    .section-title {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 20px;
      color: #2d3748;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .issue-card {
      background: white;
      border-left: 5px solid;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .issue-card:hover {
      transform: translateX(4px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }

    .issue-card.error {
      border-left-color: #dc3545;
      background: linear-gradient(to right, #fff5f5, #ffffff);
    }

    .issue-card.warning {
      border-left-color: #ffc107;
      background: linear-gradient(to right, #fffbf0, #ffffff);
    }

    .issue-card.info {
      border-left-color: #17a2b8;
      background: linear-gradient(to right, #f0f9ff, #ffffff);
    }

    .issue-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }

    .issue-badge {
      padding: 6px 14px;
      border-radius: 16px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
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
      font-weight: 700;
      flex: 1;
      font-size: 16px;
      color: #2d3748;
    }

    .issue-line {
      color: #718096;
      font-size: 13px;
      background: rgba(0, 0, 0, 0.05);
      padding: 4px 12px;
      border-radius: 8px;
      font-weight: 600;
    }

    .issue-description {
      color: #4a5568;
      line-height: 1.7;
      margin-bottom: 12px;
      font-size: 14px;
    }

    .issue-suggestion {
      background: rgba(102, 126, 234, 0.08);
      border-left: 3px solid #667eea;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 13px;
      color: #4c51bf;
      line-height: 1.6;
    }

    .issue-suggestion::before {
      content: '💡 Suggestion: ';
      font-weight: 700;
    }

    .action-buttons {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
      padding-top: 24px;
      border-top: 2px solid rgba(0, 0, 0, 0.06);
    }

    .btn {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 14px 28px;
      border-radius: 12px;
      cursor: pointer;
      font-size: 15px;
      font-weight: 600;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    .btn:active {
      transform: translateY(0);
    }

    .btn-secondary {
      background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
      box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
    }

    .btn-secondary:hover {
      box-shadow: 0 8px 24px rgba(108, 117, 125, 0.4);
    }

    .btn-success {
      background: linear-gradient(135deg, #28a745 0%, #218838 100%);
      box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    }

    .btn-success:hover {
      box-shadow: 0 8px 24px rgba(40, 167, 69, 0.4);
    }

    .no-issues {
      text-align: center;
      padding: 60px 40px;
      color: #28a745;
    }

    .no-issues h2 {
      font-size: 64px;
      margin-bottom: 20px;
    }

    .no-issues p {
      font-size: 20px;
      font-weight: 600;
      color: #2d3748;
    }

    @media (max-width: 768px) {
      body {
        padding: 16px;
      }

      .header {
        padding: 24px;
      }

      .header h1 {
        font-size: 24px;
      }

      .content {
        padding: 20px;
      }

      .summary {
        grid-template-columns: 1fr;
      }

      .action-buttons {
        flex-direction: column;
      }

      .btn {
        width: 100%;
        justify-content: center;
      }
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
        <p>Comprehensive analysis with security, quality, and best practice insights</p>
      </div>

      <div class="content">
        <div class="summary" id="summary">
          <!-- Summary stats will be injected here -->
        </div>

        <div class="code-section" id="codeSection" style="display: none;">
          <div class="code-header">📄 Analyzed Code</div>
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
    // Widget data will be injected by the server
    const reviewData = window.__REVIEW_DATA__ || {
      code: '',
      issues: []
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

      const issuesHTML = `
        <h2 class="section-title">🔧 Issues Found</h2>
        ${issues.map(issue => `
          <div class="issue-card ${issue.severity}">
            <div class="issue-header">
              <span class="issue-badge ${issue.severity}">${issue.severity}</span>
              <span class="issue-title">${escapeHtml(issue.title)}</span>
              <span class="issue-line">Line ${issue.line}</span>
            </div>
            <div class="issue-description">${escapeHtml(issue.description)}</div>
            ${issue.suggestion ? `<div class="issue-suggestion">${escapeHtml(issue.suggestion)}</div>` : ''}
          </div>
        `).join('')}
      `;

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
          prompt: 'Explain all the issues found in detail and why they matter for code quality and security'
        });
      }
    });

    document.getElementById('fixBtn')?.addEventListener('click', async () => {
      if (window.openai?.sendFollowUpMessage) {
        await window.openai.sendFollowUpMessage({
          prompt: 'Provide fixed code addressing all identified issues with explanations of each change'
        });
      }
    });

    document.getElementById('bestPracticesBtn')?.addEventListener('click', async () => {
      if (window.openai?.sendFollowUpMessage) {
        await window.openai.sendFollowUpMessage({
          prompt: 'Show best practices and design patterns relevant to this code, with examples'
        });
      }
    });
  </script>
</body>
</html>'''


def get_widget_html() -> str:
    """Return the enhanced code review widget HTML template."""
    return CODE_REVIEW_WIDGET
