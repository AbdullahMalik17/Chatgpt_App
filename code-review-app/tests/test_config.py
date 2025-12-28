"""
Unit tests for configuration management.
Tests environment loading and validation.
"""

import pytest
import os
from unittest.mock import patch
from config.settings import (
    ServerConfig,
    AnalysisConfig,
    OpenAIConfig,
    AppConfig,
)


class TestServerConfig:
    """Test cases for server configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ServerConfig()
        assert config.host == "0.0.0.0"
        assert config.port == 8001
        assert config.reload is True

    @patch.dict(os.environ, {"HOST": "127.0.0.1", "PORT": "9000"})
    def test_from_env(self):
        """Test loading from environment variables."""
        config = ServerConfig.from_env()
        assert config.host == "127.0.0.1"
        assert config.port == 9000


class TestAnalysisConfig:
    """Test cases for analysis configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AnalysisConfig()
        assert config.max_code_length == 50000
        assert config.enable_security_scan is True
        assert config.strict_mode is False

    @patch.dict(os.environ, {"MAX_CODE_LENGTH": "10000", "STRICT_MODE": "true"})
    def test_from_env(self):
        """Test loading from environment variables."""
        config = AnalysisConfig.from_env()
        assert config.max_code_length == 10000
        assert config.strict_mode is True


class TestAppConfig:
    """Test cases for application configuration."""

    def test_validation_invalid_port(self):
        """Test validation with invalid port."""
        config = AppConfig.load()
        config.server.port = 99999  # Invalid port

        errors = config.validate()
        assert len(errors) > 0
        assert any("port" in error.lower() for error in errors)

    def test_validation_invalid_code_length(self):
        """Test validation with invalid code length."""
        config = AppConfig.load()
        config.analysis.max_code_length = -1

        errors = config.validate()
        assert len(errors) > 0
        assert any("max_code_length" in error.lower() for error in errors)

    def test_validation_valid_config(self):
        """Test validation with valid configuration."""
        config = AppConfig.load()
        errors = config.validate()

        # Should have no errors with default values
        assert len(errors) == 0
