"""
Unit tests for code analyzers.
Tests language-specific and security analyzers.
"""

import pytest
from analyzers import (
    JavaScriptAnalyzer,
    PythonAnalyzer,
    SecurityAnalyzer,
    AnalyzerFactory,
    Severity,
)


class TestJavaScriptAnalyzer:
    """Test cases for JavaScript code analyzer."""

    def setup_method(self):
        """Initialize analyzer for each test."""
        self.analyzer = JavaScriptAnalyzer()

    def test_var_usage_detection(self):
        """Test detection of var keyword usage."""
        code = "var x = 10;"
        issues = self.analyzer.analyze(code)

        assert len(issues) > 0
        assert any("var" in issue.title.lower() for issue in issues)

    def test_eval_not_detected_by_js_analyzer(self):
        """Test that eval() is not flagged by JS analyzer (handled by security)."""
        code = "eval('some code');"
        issues = self.analyzer.analyze(code)

        # JS analyzer shouldn't flag eval - that's security analyzer's job
        eval_issues = [i for i in issues if "eval" in i.title.lower()]
        assert len(eval_issues) == 0

    def test_missing_error_handling(self):
        """Test detection of missing error handling."""
        code = """
async function fetchData() {
    const data = await fetch('/api/data');
    return data;
}
"""
        issues = self.analyzer.analyze(code)
        assert any("error" in issue.title.lower() for issue in issues)

    def test_console_log_detection(self):
        """Test detection of console.log statements."""
        code = "console.log('debug message');"
        issues = self.analyzer.analyze(code)

        assert any("console" in issue.title.lower() for issue in issues)


class TestPythonAnalyzer:
    """Test cases for Python code analyzer."""

    def setup_method(self):
        """Initialize analyzer for each test."""
        self.analyzer = PythonAnalyzer()

    def test_bare_except_detection(self):
        """Test detection of bare except clauses."""
        code = """
try:
    risky_operation()
except:
    pass
"""
        issues = self.analyzer.analyze(code)
        assert any("except" in issue.title.lower() for issue in issues)

    def test_mutable_default_detection(self):
        """Test detection of mutable default arguments."""
        code = "def func(items=[]):\n    pass"
        issues = self.analyzer.analyze(code)

        assert any("mutable" in issue.title.lower() for issue in issues)
        assert any(issue.severity == Severity.ERROR for issue in issues)

    def test_wildcard_import_detection(self):
        """Test detection of wildcard imports."""
        code = "from os import *"
        issues = self.analyzer.analyze(code)

        assert any("import" in issue.title.lower() for issue in issues)

    def test_none_comparison_detection(self):
        """Test detection of incorrect None comparisons."""
        code = "if x == None:\n    pass"
        issues = self.analyzer.analyze(code)

        assert any("none" in issue.title.lower() for issue in issues)


class TestSecurityAnalyzer:
    """Test cases for security analyzer."""

    def setup_method(self):
        """Initialize analyzer for each test."""
        self.analyzer = SecurityAnalyzer()

    def test_eval_detection(self):
        """Test detection of eval() usage."""
        code = "result = eval(user_input)"
        issues = self.analyzer.analyze(code)

        eval_issues = [i for i in issues if "eval" in i.title.lower()]
        assert len(eval_issues) > 0
        assert eval_issues[0].severity == Severity.ERROR

    def test_sql_injection_detection(self):
        """Test detection of SQL injection patterns."""
        code = 'query = "SELECT * FROM users WHERE id = " + user_id'
        issues = self.analyzer.analyze(code)

        assert any("sql" in issue.title.lower() for issue in issues)

    def test_weak_crypto_detection(self):
        """Test detection of weak cryptographic algorithms."""
        code = "import hashlib\nhash = hashlib.md5(password)"
        issues = self.analyzer.analyze(code)

        assert any("md5" in issue.title.lower() for issue in issues)

    def test_command_injection_detection(self):
        """Test detection of command injection risks."""
        code = "os.system(user_command)"
        issues = self.analyzer.analyze(code)

        assert any("command" in issue.title.lower() or "injection" in issue.title.lower() for issue in issues)

    def test_xss_detection(self):
        """Test detection of XSS vulnerabilities."""
        code = "element.innerHTML = userInput;"
        issues = self.analyzer.analyze(code)

        assert any("xss" in issue.title.lower() or "innerhtml" in issue.title.lower() for issue in issues)


class TestAnalyzerFactory:
    """Test cases for analyzer factory."""

    def test_get_javascript_analyzer(self):
        """Test retrieval of JavaScript analyzer."""
        analyzer = AnalyzerFactory.get_analyzer("javascript")
        assert analyzer is not None
        assert isinstance(analyzer, JavaScriptAnalyzer)

    def test_get_python_analyzer(self):
        """Test retrieval of Python analyzer."""
        analyzer = AnalyzerFactory.get_analyzer("python")
        assert analyzer is not None
        assert isinstance(analyzer, PythonAnalyzer)

    def test_language_aliases(self):
        """Test language alias resolution."""
        js_analyzer = AnalyzerFactory.get_analyzer("js")
        ts_analyzer = AnalyzerFactory.get_analyzer("typescript")
        python_analyzer = AnalyzerFactory.get_analyzer("py")

        assert js_analyzer is not None
        assert ts_analyzer is not None
        assert python_analyzer is not None

    def test_analyze_code_integration(self):
        """Test integrated code analysis."""
        code = "var x = eval(data);"
        result = AnalyzerFactory.analyze_code(code, "javascript", include_security=True)

        assert result.total_issues > 0
        assert result.errors > 0  # eval should be error
        assert len(result.issues) > 0

    def test_supported_languages(self):
        """Test supported languages listing."""
        languages = AnalyzerFactory.supported_languages()
        assert "javascript" in languages
        assert "python" in languages
        assert len(languages) > 0


class TestAnalysisResults:
    """Test cases for analysis result structures."""

    def test_issue_severity_counts(self):
        """Test issue counting by severity."""
        code = """
var x = 10;
eval('code');
console.log('test');
"""
        result = AnalyzerFactory.analyze_code(code, "javascript", include_security=True)

        assert result.total_issues == result.errors + result.warnings + result.suggestions
        assert result.errors >= 1  # eval
        assert result.total_issues > 1

    def test_issue_to_dict(self):
        """Test issue dictionary conversion."""
        from analyzers.base import Issue

        issue = Issue(
            severity=Severity.ERROR,
            line=10,
            title="Test Issue",
            description="Test description",
            category="test",
            suggestion="Fix it"
        )

        issue_dict = issue.to_dict()
        assert issue_dict["severity"] == "error"
        assert issue_dict["line"] == 10
        assert issue_dict["title"] == "Test Issue"

    def test_analysis_result_to_dict(self):
        """Test analysis result dictionary conversion."""
        code = "var test = 1;"
        result = AnalyzerFactory.analyze_code(code, "javascript")

        result_dict = result.to_dict()
        assert "code" in result_dict
        assert "language" in result_dict
        assert "issues" in result_dict
        assert "total_issues" in result_dict
