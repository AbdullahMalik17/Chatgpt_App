"""
Configuration Management System
Handles environment variables, application settings, and validation.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ServerConfig:
    """Server configuration parameters."""

    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True
    log_level: str = "info"

    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Initialize configuration from environment variables."""
        return cls(
            host=os.getenv("HOST", cls.host),
            port=int(os.getenv("PORT", cls.port)),
            reload=os.getenv("RELOAD", "true").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", cls.log_level).lower(),
        )


@dataclass
class AnalysisConfig:
    """Code analysis configuration parameters."""

    max_code_length: int = 50000
    enable_security_scan: bool = True
    enable_quality_scan: bool = True
    enable_performance_scan: bool = True
    strict_mode: bool = False

    @classmethod
    def from_env(cls) -> "AnalysisConfig":
        """Initialize configuration from environment variables."""
        return cls(
            max_code_length=int(os.getenv("MAX_CODE_LENGTH", cls.max_code_length)),
            enable_security_scan=os.getenv("ENABLE_SECURITY_SCAN", "true").lower() == "true",
            enable_quality_scan=os.getenv("ENABLE_QUALITY_SCAN", "true").lower() == "true",
            enable_performance_scan=os.getenv("ENABLE_PERFORMANCE_SCAN", "true").lower() == "true",
            strict_mode=os.getenv("STRICT_MODE", "false").lower() == "true",
        )


@dataclass
class OpenAIConfig:
    """OpenAI API configuration (optional for future enhancements)."""

    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        """Initialize configuration from environment variables."""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", cls.model),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", cls.temperature)),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", cls.max_tokens)),
        )


@dataclass
class AppConfig:
    """Application-wide configuration container."""

    server: ServerConfig
    analysis: AnalysisConfig
    openai: OpenAIConfig

    @classmethod
    def load(cls) -> "AppConfig":
        """Load complete application configuration."""
        return cls(
            server=ServerConfig.from_env(),
            analysis=AnalysisConfig.from_env(),
            openai=OpenAIConfig.from_env(),
        )

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if self.server.port < 1024 or self.server.port > 65535:
            errors.append(f"Invalid port number: {self.server.port}")

        if self.analysis.max_code_length < 1:
            errors.append(f"Invalid max_code_length: {self.analysis.max_code_length}")

        if self.openai.temperature < 0 or self.openai.temperature > 2:
            errors.append(f"Invalid OpenAI temperature: {self.openai.temperature}")

        return errors


# Singleton instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Retrieve application configuration singleton."""
    global _config
    if _config is None:
        _config = AppConfig.load()
        errors = _config.validate()
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
    return _config
