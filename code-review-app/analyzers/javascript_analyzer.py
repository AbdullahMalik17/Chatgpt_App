"""
JavaScript-specific code analyzer.
Detects common JavaScript anti-patterns and quality issues.
"""

import re
from .base import CodeAnalyzer, Issue, Severity


class JavaScriptAnalyzer(CodeAnalyzer):
    """Analyzer for JavaScript and TypeScript code quality."""

    def supported_languages(self) -> list[str]:
        """Return supported language identifiers."""
        return ["javascript", "typescript", "js", "ts"]

    def analyze(self, code: str) -> list[Issue]:
        """
        Perform comprehensive JavaScript code analysis.

        Args:
            code: JavaScript source code

        Returns:
            List of discovered issues
        """
        issues = []

        # Check for var usage
        issues.extend(self._check_var_usage(code))

        # Check for missing error handling
        issues.extend(self._check_error_handling(code))

        # Check for == instead of ===
        issues.extend(self._check_equality_operators(code))

        # Check for console.log in production code
        issues.extend(self._check_console_statements(code))

        # Check for missing JSDoc
        issues.extend(self._check_documentation(code))

        # Check for callback hell
        issues.extend(self._check_callback_nesting(code))

        # Check for missing semicolons
        issues.extend(self._check_semicolons(code))

        return issues

    def _check_var_usage(self, code: str) -> list[Issue]:
        """Detect usage of 'var' keyword."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if re.search(r'\bvar\s+', line):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    line=idx,
                    title="Variable Declaration: Use const/let",
                    description="The 'var' keyword is function-scoped and can lead to unexpected behavior. Use 'const' or 'let' for block-scoped variables.",
                    category="best-practices",
                    suggestion="Replace 'var' with 'const' (for values that won't change) or 'let' (for values that will change)."
                ))
                break  # Only report once
        return issues

    def _check_error_handling(self, code: str) -> list[Issue]:
        """Detect missing error handling for async operations."""
        issues = []
        has_try = 'try' in code
        has_catch = 'catch' in code
        has_async = ('fetch(' in code or 'await' in code or 'async' in code)

        if has_async and not (has_try and has_catch):
            issues.append(Issue(
                severity=Severity.WARNING,
                line=self.find_line_number(code, 'await') or self.find_line_number(code, 'fetch('),
                title="Missing Error Handling",
                description="Asynchronous operations should be wrapped in try-catch blocks to handle potential errors gracefully.",
                category="error-handling",
                suggestion="Wrap async operations in try-catch blocks or use .catch() for promises."
            ))
        return issues

    def _check_equality_operators(self, code: str) -> list[Issue]:
        """Detect usage of == instead of ===."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            # Match == but not === or ==
            if re.search(r'[^=!<>]==[^=]', line):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    line=idx,
                    title="Loose Equality: Use === Instead of ==",
                    description="Using == performs type coercion which can lead to unexpected results. Always use === for strict equality comparison.",
                    category="best-practices",
                    suggestion="Replace '==' with '===' for strict equality checks."
                ))
                break  # Only report once
        return issues

    def _check_console_statements(self, code: str) -> list[Issue]:
        """Detect console.log statements."""
        issues = []
        for idx, line in enumerate(code.split('\n'), 1):
            if 'console.log' in line or 'console.warn' in line or 'console.error' in line:
                issues.append(Issue(
                    severity=Severity.INFO,
                    line=idx,
                    title="Console Statement Detected",
                    description="Console statements should be removed from production code. Consider using a proper logging library.",
                    category="code-quality",
                    suggestion="Remove console statements or replace with a logging framework."
                ))
                break  # Only report once
        return issues

    def _check_documentation(self, code: str) -> list[Issue]:
        """Check for missing JSDoc documentation."""
        issues = []
        has_function = re.search(r'\bfunction\s+\w+', code) or re.search(r'const\s+\w+\s*=\s*\(.*\)\s*=>', code)
        has_jsdoc = '/**' in code

        if has_function and not has_jsdoc:
            issues.append(Issue(
                severity=Severity.INFO,
                line=1,
                title="Missing JSDoc Documentation",
                description="Functions should include JSDoc comments describing parameters, return values, and purpose.",
                category="documentation",
                suggestion="Add JSDoc comments above function declarations."
            ))
        return issues

    def _check_callback_nesting(self, code: str) -> list[Issue]:
        """Detect deeply nested callbacks (callback hell)."""
        issues = []
        max_nesting = 0
        current_nesting = 0

        for char in code:
            if char == '{':
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char == '}':
                current_nesting -= 1

        if max_nesting > 4:
            issues.append(Issue(
                severity=Severity.WARNING,
                line=1,
                title="Deep Nesting Detected",
                description=f"Code has {max_nesting} levels of nesting. This may indicate callback hell or overly complex logic.",
                category="code-quality",
                suggestion="Consider using async/await, extracting functions, or refactoring to reduce nesting."
            ))
        return issues

    def _check_semicolons(self, code: str) -> list[Issue]:
        """Check for potentially missing semicolons."""
        issues = []
        lines = code.split('\n')

        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            # Check lines that should typically end with semicolon
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                if re.match(r'(return|const|let|var)\s+.+[^;{}\s]$', stripped):
                    issues.append(Issue(
                        severity=Severity.INFO,
                        line=idx,
                        title="Potentially Missing Semicolon",
                        description="This line may be missing a semicolon. While ASI (Automatic Semicolon Insertion) exists, explicit semicolons improve code clarity.",
                        category="style",
                        suggestion="Add semicolon at end of statement."
                    ))
                    break  # Only report once
        return issues
