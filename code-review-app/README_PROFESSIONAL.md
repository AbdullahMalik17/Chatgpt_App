# Code Review & Analysis Tool - Professional Edition

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-orange.svg)]()

## Overview

A production-grade ChatGPT application that provides comprehensive code analysis through an interactive widget interface. This tool employs static analysis techniques to identify code quality issues, security vulnerabilities, and adherence to best practices across multiple programming languages.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   ChatGPT Interface                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Interactive Widget Layer                    │
│  (HTML/CSS/JS with Dynamic Data Injection)              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP Server Layer                        │
│          (FastMCP + Python 3.12+)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌────────────────┐          ┌────────────────┐
│   Language     │          │   Security     │
│   Analyzers    │          │   Analyzer     │
│  (JS, Python)  │          │ (Cross-lang)   │
└────────────────┘          └────────────────┘
```

## Key Features

### Analysis Capabilities
- **Multi-Language Support**: JavaScript, TypeScript, Python with extensible architecture
- **Security Vulnerability Detection**: SQL injection, XSS, code injection, weak cryptography
- **Code Quality Assessment**: Anti-patterns, style violations, missing documentation
- **Best Practices Enforcement**: Language-specific recommendations and modern patterns

### Technical Excellence
- **Modular Architecture**: Separation of concerns with dedicated modules for analyzers, widgets, configuration
- **Configuration Management**: Environment-based configuration with validation
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Error Handling**: Robust validation and error recovery mechanisms
- **Type Safety**: Python type hints throughout the codebase

### Interactive Features
- **Visual Dashboard**: Real-time widget displaying analysis results with categorized issues
- **Actionable Insights**: Contextual suggestions with remediation guidance
- **Interactive Actions**: Explain issues, suggest fixes, view best practices

## Project Structure

```
code-review-app/
├── analyzers/                    # Code analysis engines
│   ├── __init__.py
│   ├── base.py                   # Abstract base classes
│   ├── javascript_analyzer.py   # JavaScript/TypeScript analyzer
│   ├── python_analyzer.py       # Python analyzer
│   ├── security_analyzer.py     # Cross-language security scanner
│   └── analyzer_factory.py      # Factory pattern implementation
│
├── config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py               # Environment-based configuration
│
├── widgets/                      # Interactive UI components
│   ├── __init__.py
│   └── code_review_widget.py    # Enhanced widget template
│
├── utils/                        # Utility modules
│   ├── __init__.py
│   └── logger.py                 # Logging configuration
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_analyzers.py
│   ├── test_config.py
│   └── test_integration.py
│
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── README.md                     # Quick start guide
├── README_PROFESSIONAL.md        # This file
├── QUICKSTART.md                 # 5-minute setup
└── DEPLOYMENT.md                 # Production deployment guide
```

## Prerequisites

### Required
- Python 3.12 or higher
- pip package manager
- ngrok account (for development/testing)
- ChatGPT Plus/Team/Enterprise subscription

### Optional
- OpenAI API key (for future AI-enhanced analysis)
- Docker (for containerized deployment)
- PostgreSQL (for future analytics features)

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd code-review-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Verify Installation

```bash
python -c "from config import get_config; print('Configuration valid')"
```

## Configuration

### Environment Variables

#### Server Configuration
```bash
HOST=0.0.0.0              # Server bind address
PORT=8001                  # Server port
RELOAD=true                # Auto-reload on code changes (dev only)
LOG_LEVEL=info             # Logging level (debug, info, warning, error)
```

#### Analysis Configuration
```bash
MAX_CODE_LENGTH=50000              # Maximum code length to analyze
ENABLE_SECURITY_SCAN=true          # Enable security vulnerability scanning
ENABLE_QUALITY_SCAN=true           # Enable code quality analysis
ENABLE_PERFORMANCE_SCAN=true       # Enable performance pattern detection
STRICT_MODE=false                  # Strict validation mode
```

#### OpenAI Configuration (Optional)
```bash
OPENAI_API_KEY=sk-...              # OpenAI API key
OPENAI_MODEL=gpt-4                 # Model identifier
OPENAI_TEMPERATURE=0.7             # Sampling temperature
OPENAI_MAX_TOKENS=2000             # Maximum response tokens
```

## Usage

### Development Mode

#### Terminal 1: Start MCP Server
```bash
python main.py
```

Expected output:
```
╔══════════════════════════════════════════════════════════════╗
║     Code Review & Analysis Tool - MCP Server v2.0.0          ║
╠══════════════════════════════════════════════════════════════╣
║  Server: http://0.0.0.0:8001                                 ║
║  Status: ✓ Running                                           ║
║  Log Level: INFO                                             ║
╚══════════════════════════════════════════════════════════════╝
```

#### Terminal 2: Expose via ngrok
```bash
ngrok http 8001
```

Copy the HTTPS forwarding URL.

### ChatGPT Registration

1. Navigate to [ChatGPT Apps](https://chatgpt.com/apps)
2. Enable Developer mode in Settings
3. Create new app:
   - **Name**: Code Review Tool
   - **MCP Server URL**: `https://YOUR-NGROK-URL/mcp`
   - **Authentication**: No Auth
4. Save configuration

### Example Interactions

#### Code Analysis
```
@Code Review Tool analyze this code:

function processUserInput(data) {
  var result = eval(data);
  document.innerHTML = result;
  return result;
}
```

#### Security Scan
```
@Code Review Tool perform security scan:

query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)
```

#### List Languages
```
@Code Review Tool list supported languages
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_analyzers.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### Adding New Language Analyzer

1. Create analyzer class in `analyzers/`:
```python
from .base import CodeAnalyzer, Issue, Severity

class NewLanguageAnalyzer(CodeAnalyzer):
    def supported_languages(self) -> list[str]:
        return ["newlang"]

    def analyze(self, code: str) -> list[Issue]:
        # Implement analysis logic
        return []
```

2. Register in `analyzer_factory.py`:
```python
_analyzers = {
    # ...
    'newlang': NewLanguageAnalyzer(),
}
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive production deployment instructions including:
- Docker containerization
- Cloud platform deployment (AWS, GCP, Azure)
- SSL/TLS configuration
- Monitoring and logging
- Scaling considerations

## API Reference

### Tools

#### `analyze_code`
Comprehensive code analysis including quality, security, and best practices.

**Parameters:**
- `code` (string, required): Source code to analyze
- `language` (string, optional): Programming language identifier (default: "javascript")

**Returns:**
- Interactive widget with categorized issues
- Structured analysis data
- Actionable recommendations

#### `security_scan`
Security-focused vulnerability detection.

**Parameters:**
- `code` (string, required): Source code to scan
- `language` (string, optional): Programming language identifier (default: "javascript")

**Returns:**
- Security vulnerability report
- Severity classifications
- Remediation guidance

#### `list_supported_languages`
Retrieve list of supported programming languages.

**Parameters:** None

**Returns:**
- List of language identifiers

## Performance Considerations

### Analysis Speed
- JavaScript/Python analysis: < 100ms for typical functions
- Security scanning: < 200ms for most code samples
- Widget rendering: Instant client-side

### Resource Requirements
- Memory: 50-100MB base + ~1MB per concurrent analysis
- CPU: Minimal (pattern matching only)
- Network: Lightweight JSON payloads

## Security Considerations

### Input Validation
- Maximum code length enforcement
- Parameter validation and sanitization
- HTML escaping in widget rendering

### Data Privacy
- No code persistence or storage
- No external API calls for analysis (pattern-based only)
- Optional OpenAI integration requires explicit configuration

## Troubleshooting

### Widget Not Displaying
1. Verify server logs for errors
2. Check ngrok tunnel status
3. Clear ChatGPT cache (recreate app with new ngrok URL)
4. Inspect browser console for errors

### Tools Not Available
1. Confirm server is running
2. Test MCP endpoint: `curl https://YOUR-NGROK-URL/mcp`
3. Verify app registration in ChatGPT settings
4. Try in new conversation

### Analysis Errors
1. Check code length against MAX_CODE_LENGTH
2. Verify language identifier is supported
3. Review server logs for exceptions
4. Enable DEBUG log level for detailed output

## Contributing

Contributions are encouraged. Please follow these guidelines:

1. Fork repository
2. Create feature branch
3. Implement changes with tests
4. Ensure code quality checks pass
5. Submit pull request with detailed description

## Roadmap

### Version 2.1
- [ ] OpenAI API integration for AI-enhanced analysis
- [ ] Additional language support (Java, Go, Ruby, PHP)
- [ ] Custom rule configuration
- [ ] Analysis history and trends

### Version 3.0
- [ ] Team collaboration features
- [ ] Integration with CI/CD pipelines
- [ ] Advanced security scanning with CVE database
- [ ] Performance profiling and optimization suggestions

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: GitHub Issues
- **Documentation**: See README.md and QUICKSTART.md
- **Community**: GitHub Discussions

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- MCP Protocol by [Anthropic](https://modelcontextprotocol.io)
- ChatGPT Apps by [OpenAI](https://platform.openai.com/docs)

---

**Version**: 2.0.0
**Last Updated**: 2025-12-28
**Maintainer**: Code Review Tool Team
