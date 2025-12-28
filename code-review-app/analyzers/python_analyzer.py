"""
Python-specific code analyzer.
Detects common Python anti-patterns and quality issues.
"""

import re
from .base import CodeAnalyzer, Issue, Severity


class PythonAnalyzer(CodeAnalyzer):
    """Analyzer for Python code quality."""

    def supported_languages(self) -> list[str]:
        """Return supported language identifiers."""
        return ["python", "py"]

    def analyze(self, code: str) -> list[Issue]:
        """
        Perform comprehensive Python code analysis.

        Args:
            code: Python source code

        Returns:
            List of discovered issues
        """
        issues = []

        # Check for bare except
        issues.extend(self._check_bare_except(code))

        # Check for mutable default arguments
        issues.extend(self._check_mutable_defaults(code))

        # Check for missing type hints
        issues.extend(self._check_type_hints(code))

        # Check for print statements
        issues.extend(self._check_print_statements(code))

        # Check for missing docstrings
        issues.extend(self._check_docstrings(code))

        # Check for wildcard imports
        issues.extend(self._check_wildcard_imports(code))

        # Check for using == None instead of is None
        issues.extend(self._check_none_comparison(code))

        return issues

    def _check_bare_except(self, code: str) -> list[Issue]:
        """Detect bare except clauses."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.match(r'\s*except\s*:', line):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    line=idx,
                    title="Bare Except Clause",
                    description="Using 'except:' without specifying an exception type catches all exceptions, including SystemExit and KeyboardInterrupt.",
                    category="error-handling",
                    suggestion="Specify the exception type: 'except Exception:' or catch specific exceptions."
                ))
        return issues

    def _check_mutable_defaults(self, code: str) -> list[Issue]:
        """Detect mutable default arguments."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.search(r'def\s+\w+\([^)]*=\s*[\[\{]', line):
                issues.append(Issue(
                    severity=Severity.ERROR,
                    line=idx,
                    title="Mutable Default Argument",
                    description="Using mutable objects (list, dict, set) as default arguments can lead to unexpected behavior. The default is shared across all function calls.",
                    category="best-practices",
                    suggestion="Use None as default and initialize the mutable object inside the function."
                ))
        return issues

    def _check_type_hints(self, code: str) -> list[Issue]:
        """Check for missing type hints."""
        issues = []
        function_count = len(re.findall(r'def\s+\w+\s*\(', code))
        typed_count = len(re.findall(r'def\s+\w+\s*\([^)]*:\s*\w+', code))

        if function_count > 0 and typed_count == 0:
            issues.append(Issue(
                severity=Severity.INFO,
                line=self.find_line_number(code, 'def '),
                title="Missing Type Hints",
                description="Functions lack type annotations. Type hints improve code readability and enable better IDE support.",
                category="documentation",
                suggestion="Add type hints for function parameters and return values."
            ))
        return issues

    def _check_print_statements(self, code: str) -> list[Issue]:
        """Detect print statements."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.search(r'\bprint\s*\(', line):
                issues.append(Issue(
                    severity=Severity.INFO,
                    line=idx,
                    title="Print Statement Detected",
                    description="Print statements should be removed from production code. Use the logging module instead.",
                    category="code-quality",
                    suggestion="Replace print() with logging.info() or logging.debug()."
                ))
                break  # Only report once
        return issues

    def _check_docstrings(self, code: str) -> list[Issue]:
        """Check for missing docstrings."""
        issues = []
        has_function = re.search(r'def\s+\w+', code)
        has_docstring = '"""' in code or "'''" in code

        if has_function and not has_docstring:
            issues.append(Issue(
                severity=Severity.INFO,
                line=1,
                title="Missing Docstrings",
                description="Functions and classes should include docstrings describing their purpose, parameters, and return values.",
                category="documentation",
                suggestion="Add docstrings following PEP 257 conventions."
            ))
        return issues

    def _check_wildcard_imports(self, code: str) -> list[Issue]:
        """Detect wildcard imports."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.search(r'from\s+\S+\s+import\s+\*', line):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    line=idx,
                    title="Wildcard Import",
                    description="Using 'from module import *' pollutes the namespace and makes it unclear where names come from.",
                    category="best-practices",
                    suggestion="Import specific names or use 'import module' instead."
                ))
        return issues

    def _check_none_comparison(self, code: str) -> list[Issue]:
        """Check for incorrect None comparisons."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.search(r'==\s*None|None\s*==', line):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    line=idx,
                    title="Use 'is None' Instead of '== None'",
                    description="Comparing to None should use 'is None' or 'is not None', not '==' or '!='.",
                    category="best-practices",
                    suggestion="Replace '== None' with 'is None'."
                ))
                break  # Only report once
        return issues
