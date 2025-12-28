"""
Factory for creating appropriate code analyzers based on language.
Implements the Factory design pattern for analyzer instantiation.
"""

from typing import Optional
from .base import CodeAnalyzer, AnalysisResult
from .javascript_analyzer import JavaScriptAnalyzer
from .python_analyzer import PythonAnalyzer
from .security_analyzer import SecurityAnalyzer


class AnalyzerFactory:
    """Factory class for creating and managing code analyzers."""

    # Registry of available analyzers
    _analyzers: dict[str, CodeAnalyzer] = {
        'javascript': JavaScriptAnalyzer(),
        'python': PythonAnalyzer(),
        'security': SecurityAnalyzer(),
    }

    # Language aliases mapping
    _language_aliases = {
        'js': 'javascript',
        'ts': 'javascript',
        'typescript': 'javascript',
        'py': 'python',
    }

    @classmethod
    def get_analyzer(cls, language: str) -> Optional[CodeAnalyzer]:
        """
        Retrieve appropriate analyzer for the specified language.

        Args:
            language: Programming language identifier

        Returns:
            CodeAnalyzer instance or None if unsupported
        """
        normalized_language = cls._normalize_language(language)
        return cls._analyzers.get(normalized_language)

    @classmethod
    def get_security_analyzer(cls) -> CodeAnalyzer:
        """
        Retrieve the cross-language security analyzer.

        Returns:
            SecurityAnalyzer instance
        """
        return cls._analyzers['security']

    @classmethod
    def analyze_code(cls, code: str, language: str, include_security: bool = True) -> AnalysisResult:
        """
        Perform comprehensive code analysis using appropriate analyzers.

        Args:
            code: Source code to analyze
            language: Programming language
            include_security: Whether to include security analysis

        Returns:
            AnalysisResult containing all discovered issues
        """
        all_issues = []

        # Get language-specific analyzer
        language_analyzer = cls.get_analyzer(language)
        if language_analyzer:
            all_issues.extend(language_analyzer.analyze(code))

        # Add security analysis if requested
        if include_security:
            security_analyzer = cls.get_security_analyzer()
            all_issues.extend(security_analyzer.analyze(code))

        # Sort issues by line number and severity
        all_issues.sort(key=lambda x: (x.line, x.severity.value))

        return AnalysisResult(
            code=code,
            language=language,
            issues=all_issues,
            metadata={
                'analyzers_used': [
                    language if language_analyzer else None,
                    'security' if include_security else None
                ],
                'language_supported': language_analyzer is not None,
            }
        )

    @classmethod
    def supported_languages(cls) -> list[str]:
        """
        Get list of all supported programming languages.

        Returns:
            List of supported language identifiers
        """
        languages = set()
        for analyzer in cls._analyzers.values():
            if hasattr(analyzer, 'supported_languages'):
                languages.update(analyzer.supported_languages())
        return sorted(list(languages))

    @classmethod
    def _normalize_language(cls, language: str) -> str:
        """
        Normalize language identifier using aliases.

        Args:
            language: Raw language identifier

        Returns:
            Normalized language identifier
        """
        normalized = language.lower().strip()
        return cls._language_aliases.get(normalized, normalized)
