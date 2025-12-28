"""
Base classes and data structures for code analysis.
Defines the abstract interface for all code analyzers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal
from enum import Enum


class Severity(str, Enum):
    """Issue severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    """Represents a single code issue discovered during analysis."""

    severity: Severity
    line: int
    title: str
    description: str
    category: str = "general"
    suggestion: str = ""

    def to_dict(self) -> dict:
        """Convert issue to dictionary representation."""
        return {
            "severity": self.severity.value,
            "line": self.line,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "suggestion": self.suggestion,
        }


@dataclass
class AnalysisResult:
    """Container for complete code analysis results."""

    code: str
    language: str
    issues: list[Issue] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def total_issues(self) -> int:
        """Calculate total number of issues."""
        return len(self.issues)

    @property
    def errors(self) -> int:
        """Count error-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.ERROR)

    @property
    def warnings(self) -> int:
        """Count warning-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.WARNING)

    @property
    def suggestions(self) -> int:
        """Count info-level issues."""
        return sum(1 for issue in self.issues if issue.severity == Severity.INFO)

    def to_dict(self) -> dict:
        """Convert analysis result to dictionary representation."""
        return {
            "code": self.code,
            "language": self.language,
            "issues": [issue.to_dict() for issue in self.issues],
            "total_issues": self.total_issues,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "metadata": self.metadata,
        }


class CodeAnalyzer(ABC):
    """
    Abstract base class for code analyzers.
    All language-specific analyzers must inherit from this class.
    """

    @abstractmethod
    def analyze(self, code: str) -> list[Issue]:
        """
        Analyze code and return list of discovered issues.

        Args:
            code: Source code to analyze

        Returns:
            List of Issue objects representing discovered problems
        """
        pass

    @abstractmethod
    def supported_languages(self) -> list[str]:
        """
        Return list of programming languages this analyzer supports.

        Returns:
            List of language identifiers (e.g., ['javascript', 'typescript'])
        """
        pass

    def find_line_number(self, code: str, pattern: str) -> int:
        """
        Utility method to find line number containing a pattern.

        Args:
            code: Complete source code
            pattern: Pattern to search for

        Returns:
            Line number (1-indexed) or 1 if not found
        """
        for idx, line in enumerate(code.split('\n'), 1):
            if pattern in line:
                return idx
        return 1
