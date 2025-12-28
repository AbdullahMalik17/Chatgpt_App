"""
Code Review and Analysis Tool - MCP Server
Professional implementation with modular architecture and comprehensive analysis.
"""

import os
import json
from typing import Optional
from datetime import datetime

import mcp.types as types
from mcp.server.fastmcp import FastMCP

# Import application modules
from config import get_config
from analyzers import AnalyzerFactory
from widgets import get_widget_html
from utils import setup_logger, get_logger

# Initialize configuration
try:
    config = get_config()
except ValueError as e:
    print(f"Configuration error: {e}")
    raise

# Initialize logging
logger = setup_logger(level=config.server.log_level.upper())
logger.info("Code Review Tool starting up...")

# Widget MIME type for ChatGPT
MIME_TYPE = "text/html+skybridge"

# Widget HTML template
CODE_REVIEW_WIDGET = get_widget_html()

# Widget registry
WIDGETS = {
    "code-review": {
        "uri": "ui://widget/code-review.html",
        "html": CODE_REVIEW_WIDGET,
        "title": "Code Review Dashboard",
    },
}

# Create FastMCP server
mcp = FastMCP("Code Review Tool", version="2.0.0")


@mcp.resource(
    uri="ui://widget/{widget_name}.html",
    name="Widget Resource",
    mime_type=MIME_TYPE
)
def widget_resource(widget_name: str) -> str:
    """
    Serve widget HTML for code review visualization.

    Args:
        widget_name: Identifier for the requested widget

    Returns:
        HTML content for the widget
    """
    logger.debug(f"Widget resource requested: {widget_name}")
    if widget_name in WIDGETS:
        return WIDGETS[widget_name]["html"]
    return WIDGETS["code-review"]["html"]


def _embedded_widget_resource(widget_id: str, analysis_data: dict) -> types.EmbeddedResource:
    """
    Create embedded widget resource with data injection for tool response.

    Args:
        widget_id: Widget identifier
        analysis_data: Analysis results to inject into widget

    Returns:
        EmbeddedResource with injected data
    """
    widget = WIDGETS[widget_id]

    # Inject data into widget HTML
    widget_html = widget["html"].replace(
        "window.__REVIEW_DATA__ || {",
        f"window.__REVIEW_DATA__ = {json.dumps(analysis_data)} || {{"
    )

    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=widget["uri"],
            mimeType=MIME_TYPE,
            text=widget_html,
            title=widget["title"],
        ),
    )


def listing_meta() -> dict:
    """
    Tool metadata for ChatGPT tool listing.

    Returns:
        Metadata dictionary for tool catalog
    """
    return {
        "openai.com/widget": {
            "uri": WIDGETS["code-review"]["uri"],
            "title": WIDGETS["code-review"]["title"]
        }
    }


def response_meta(analysis_data: dict) -> dict:
    """
    Response metadata with embedded widget containing analysis data.

    Args:
        analysis_data: Analysis results to embed

    Returns:
        Metadata dictionary with embedded widget resource
    """
    return {
        "openai.com/widget": _embedded_widget_resource("code-review", analysis_data)
    }


def validate_code_input(code: str, language: str) -> Optional[str]:
    """
    Validate code analysis input parameters.

    Args:
        code: Source code to validate
        language: Programming language identifier

    Returns:
        Error message if validation fails, None otherwise
    """
    if not code or not code.strip():
        return "Code parameter is required and cannot be empty"

    if len(code) > config.analysis.max_code_length:
        return f"Code exceeds maximum length of {config.analysis.max_code_length} characters"

    if not language or not language.strip():
        return "Language parameter is required"

    return None


@mcp.tool(
    annotations={
        "title": "Analyze Code",
        "description": "Comprehensive code analysis including quality, security, and best practices",
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

    This tool performs comprehensive static analysis using language-specific analyzers
    and cross-language security scanning. Results are presented in an interactive
    widget with detailed explanations and actionable suggestions.

    Args:
        code: The source code to analyze
        language: Programming language (javascript, python, typescript, etc.)

    Returns:
        Comprehensive code review with interactive widget visualization
    """
    logger.info(f"Code analysis requested for language: {language}")

    # Validate input
    validation_error = validate_code_input(code, language)
    if validation_error:
        logger.warning(f"Validation failed: {validation_error}")
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Error: {validation_error}"
                )
            ],
            isError=True
        )

    try:
        # Perform analysis using factory
        analysis_result = AnalyzerFactory.analyze_code(
            code=code,
            language=language,
            include_security=config.analysis.enable_security_scan
        )

        logger.info(
            f"Analysis complete: {analysis_result.total_issues} issues found "
            f"(Errors: {analysis_result.errors}, Warnings: {analysis_result.warnings}, "
            f"Suggestions: {analysis_result.suggestions})"
        )

        # Convert to dictionary for widget
        analysis_dict = analysis_result.to_dict()

        # Format text summary
        summary_text = f"""Code Analysis Complete ✓

Language: {language}
Total Issues: {analysis_result.total_issues}
├─ Errors: {analysis_result.errors}
├─ Warnings: {analysis_result.warnings}
└─ Suggestions: {analysis_result.suggestions}

{_generate_summary_insights(analysis_result)}

Review the interactive widget below for detailed results and actionable suggestions."""

        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=summary_text
                )
            ],
            structuredContent=analysis_dict,
            _meta=response_meta(analysis_dict),
        )

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Analysis failed: {str(e)}"
                )
            ],
            isError=True
        )


def _generate_summary_insights(analysis_result) -> str:
    """
    Generate human-readable insights from analysis results.

    Args:
        analysis_result: AnalysisResult object

    Returns:
        Formatted insights string
    """
    insights = []

    if analysis_result.errors > 0:
        insights.append(f"⚠️  Critical: {analysis_result.errors} error(s) require immediate attention")

    if analysis_result.warnings > 0:
        insights.append(f"⚡ Important: {analysis_result.warnings} warning(s) should be addressed")

    if analysis_result.suggestions > 0:
        insights.append(f"💡 Optional: {analysis_result.suggestions} suggestion(s) for improvement")

    if analysis_result.total_issues == 0:
        insights.append("✨ Excellent! No issues detected")

    return "\n".join(insights) if insights else ""


@mcp.tool(
    annotations={
        "title": "Security Scan",
        "description": "Security-focused vulnerability detection across multiple languages",
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def security_scan(
    code: str,
    language: str = "javascript"
) -> types.CallToolResult:
    """
    Perform security-focused analysis of code to identify vulnerabilities.

    This tool focuses exclusively on security issues including code injection,
    XSS vulnerabilities, weak cryptography, SQL injection, and other common
    security anti-patterns.

    Args:
        code: The source code to scan
        language: Programming language identifier

    Returns:
        Security vulnerability report with detailed findings
    """
    logger.info(f"Security scan requested for language: {language}")

    # Validate input
    validation_error = validate_code_input(code, language)
    if validation_error:
        logger.warning(f"Validation failed: {validation_error}")
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Error: {validation_error}"
                )
            ],
            isError=True
        )

    try:
        # Get security analyzer
        security_analyzer = AnalyzerFactory.get_security_analyzer()
        vulnerabilities = security_analyzer.analyze(code)

        # Sort by severity and line number
        vulnerabilities.sort(key=lambda x: (x.severity.value, x.line))

        # Create result structure
        from analyzers.base import AnalysisResult
        result = AnalysisResult(
            code=code,
            language=language,
            issues=vulnerabilities,
            metadata={
                'scan_type': 'security',
                'timestamp': datetime.now().isoformat(),
            }
        )

        logger.info(f"Security scan complete: {len(vulnerabilities)} vulnerabilities found")

        # Convert to dictionary
        result_dict = result.to_dict()

        # Format summary
        critical_count = sum(1 for v in vulnerabilities if v.severity.value == 'error')

        summary = f"""Security Scan Complete 🔒

Vulnerabilities Found: {len(vulnerabilities)}
├─ Critical: {critical_count}
└─ Warnings: {len(vulnerabilities) - critical_count}

{_generate_security_insights(vulnerabilities)}

Review the interactive widget for detailed vulnerability information and remediation steps."""

        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=summary
                )
            ],
            structuredContent=result_dict,
            _meta=response_meta(result_dict),
        )

    except Exception as e:
        logger.error(f"Security scan failed: {str(e)}", exc_info=True)
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Security scan failed: {str(e)}"
                )
            ],
            isError=True
        )


def _generate_security_insights(vulnerabilities: list) -> str:
    """
    Generate security-specific insights from vulnerability list.

    Args:
        vulnerabilities: List of Issue objects

    Returns:
        Formatted security insights
    """
    if not vulnerabilities:
        return "✅ No obvious security vulnerabilities detected"

    critical = sum(1 for v in vulnerabilities if v.severity.value == 'error')

    insights = []
    if critical > 0:
        insights.append(f"🚨 CRITICAL: {critical} severe security issue(s) detected")
        insights.append("   Immediate remediation required to prevent exploitation")
    else:
        insights.append("⚠️  Security improvements recommended")

    return "\n".join(insights)


@mcp.tool(
    annotations={
        "title": "List Supported Languages",
        "description": "Get list of programming languages supported by the analyzer",
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def list_supported_languages() -> types.CallToolResult:
    """
    Retrieve list of all programming languages supported by the code analyzer.

    Returns:
        List of supported language identifiers
    """
    logger.info("Supported languages list requested")

    try:
        languages = AnalyzerFactory.supported_languages()

        language_list = "\n".join([f"  • {lang}" for lang in languages])

        summary = f"""Supported Programming Languages

The code review tool supports the following languages:

{language_list}

Use any of these identifiers in the 'language' parameter when analyzing code.
Note: Security scanning works across all languages."""

        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=summary
                )
            ],
            structuredContent={"languages": languages}
        )

    except Exception as e:
        logger.error(f"Failed to list languages: {str(e)}", exc_info=True)
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ],
            isError=True
        )


if __name__ == "__main__":
    import uvicorn

    port = config.server.port
    host = config.server.host

    logger.info(f"Starting server on {host}:{port}")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     Code Review & Analysis Tool - MCP Server v2.0.0          ║
╠══════════════════════════════════════════════════════════════╣
║  Server: http://{host}:{port:<40}  ║
║  Status: ✓ Running                                           ║
║  Log Level: {config.server.log_level.upper():<49} ║
║                                                              ║
║  Supported Languages:                                        ║
║  {', '.join(AnalyzerFactory.supported_languages())[:56]:<57} ║
║                                                              ║
║  Next Steps:                                                 ║
║  1. Start ngrok: ngrok http {port:<34}  ║
║  2. Copy ngrok HTTPS URL                                     ║
║  3. Register in ChatGPT: https://chatgpt.com/apps           ║
║     MCP URL: https://YOUR-NGROK-URL/mcp                     ║
╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "main:mcp.app",
        host=host,
        port=port,
        reload=config.server.reload,
        log_level=config.server.log_level.lower()
    )
