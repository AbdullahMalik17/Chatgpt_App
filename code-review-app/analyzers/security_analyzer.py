"""
Security-focused code analyzer.
Detects common security vulnerabilities across multiple languages.
"""

import re
from .base import CodeAnalyzer, Issue, Severity


class SecurityAnalyzer(CodeAnalyzer):
    """Cross-language security vulnerability analyzer."""

    # Security patterns mapped to vulnerability descriptions
    SECURITY_PATTERNS = {
        r'\beval\s*\(': {
            'title': 'Code Injection Risk: eval() Usage',
            'description': 'Using eval() executes arbitrary code and is extremely dangerous. This creates a critical code injection vulnerability that attackers can exploit.',
            'suggestion': 'Remove eval() and use safer alternatives like JSON.parse() for data or explicit function calls.',
            'severity': Severity.ERROR,
        },
        r'\.innerHTML\s*=': {
            'title': 'XSS Vulnerability: innerHTML Assignment',
            'description': 'Directly assigning to innerHTML can execute malicious scripts if the content contains user input.',
            'suggestion': 'Use textContent for plain text or sanitize HTML with a library like DOMPurify.',
            'severity': Severity.ERROR,
        },
        r'document\.write\s*\(': {
            'title': 'XSS Vulnerability: document.write()',
            'description': 'document.write() can be exploited for cross-site scripting attacks if used with user input.',
            'suggestion': 'Use modern DOM manipulation methods like createElement() and appendChild().',
            'severity': Severity.WARNING,
        },
        r'\bexec\s*\(': {
            'title': 'Command Injection Risk: exec() Usage',
            'description': 'Using exec() to execute system commands or code can lead to command injection vulnerabilities.',
            'suggestion': 'Avoid exec() and use safer alternatives. If necessary, validate and sanitize all inputs.',
            'severity': Severity.ERROR,
        },
        r'\bMD5\b': {
            'title': 'Weak Cryptography: MD5 Hash',
            'description': 'MD5 is cryptographically broken and should not be used for security purposes. It is vulnerable to collision attacks.',
            'suggestion': 'Use SHA-256, SHA-3, or bcrypt for password hashing.',
            'severity': Severity.WARNING,
        },
        r'\bSHA1\b': {
            'title': 'Weak Cryptography: SHA-1 Hash',
            'description': 'SHA-1 is deprecated for security purposes and vulnerable to collision attacks.',
            'suggestion': 'Use SHA-256 or SHA-3 for cryptographic hashing.',
            'severity': Severity.WARNING,
        },
        r'SELECT\s+.*\s+FROM\s+.*\+': {
            'title': 'SQL Injection Risk: String Concatenation',
            'description': 'Building SQL queries with string concatenation can lead to SQL injection vulnerabilities.',
            'suggestion': 'Use parameterized queries or prepared statements instead.',
            'severity': Severity.ERROR,
        },
        r'f["\']SELECT.*\{': {
            'title': 'SQL Injection Risk: F-String SQL Query',
            'description': 'Using f-strings or string formatting for SQL queries can lead to SQL injection.',
            'suggestion': 'Use parameterized queries with placeholders (?, %s, or named parameters).',
            'severity': Severity.ERROR,
        },
        r'pickle\.loads?\(': {
            'title': 'Insecure Deserialization: Pickle',
            'description': 'Unpickling data from untrusted sources can lead to arbitrary code execution.',
            'suggestion': 'Use JSON for data serialization or verify the source of pickled data.',
            'severity': Severity.ERROR,
        },
        r'yaml\.load\(': {
            'title': 'Insecure Deserialization: YAML',
            'description': 'yaml.load() can execute arbitrary Python code. This is a critical security risk.',
            'suggestion': 'Use yaml.safe_load() instead, which only constructs simple Python objects.',
            'severity': Severity.ERROR,
        },
        r'os\.system\(': {
            'title': 'Command Injection Risk: os.system()',
            'description': 'Using os.system() with user input can lead to command injection attacks.',
            'suggestion': 'Use subprocess module with shell=False and list arguments instead.',
            'severity': Severity.ERROR,
        },
        r'subprocess\.call\([^,]+,\s*shell\s*=\s*True': {
            'title': 'Command Injection Risk: shell=True',
            'description': 'Using shell=True with subprocess makes the code vulnerable to shell injection attacks.',
            'suggestion': 'Use shell=False and pass arguments as a list instead.',
            'severity': Severity.ERROR,
        },
        r'random\.random\(\).*password|password.*random\.random\(\)': {
            'title': 'Weak Random Number Generation',
            'description': 'random.random() is not cryptographically secure and should not be used for security-sensitive operations.',
            'suggestion': 'Use secrets module or os.urandom() for cryptographic randomness.',
            'severity': Severity.WARNING,
        },
        r'http://': {
            'title': 'Insecure Protocol: HTTP',
            'description': 'Using HTTP instead of HTTPS transmits data in plaintext, exposing it to interception.',
            'suggestion': 'Use HTTPS URLs to ensure encrypted communication.',
            'severity': Severity.WARNING,
        },
        r'verify\s*=\s*False': {
            'title': 'SSL Verification Disabled',
            'description': 'Disabling SSL certificate verification makes the connection vulnerable to man-in-the-middle attacks.',
            'suggestion': 'Remove verify=False and ensure proper SSL certificate configuration.',
            'severity': Severity.ERROR,
        },
    }

    def supported_languages(self) -> list[str]:
        """Return supported language identifiers."""
        return ["javascript", "python", "typescript", "php", "java", "go", "ruby"]

    def analyze(self, code: str) -> list[Issue]:
        """
        Perform security-focused analysis on code.

        Args:
            code: Source code to analyze

        Returns:
            List of security issues
        """
        issues = []

        for pattern, details in self.SECURITY_PATTERNS.items():
            matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                issues.append(Issue(
                    severity=details['severity'],
                    line=line_number,
                    title=details['title'],
                    description=details['description'],
                    category="security",
                    suggestion=details['suggestion']
                ))

        return issues
