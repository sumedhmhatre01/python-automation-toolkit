class AutomationError(Exception):
    """Base exception for the automation toolkit."""


class ConfigurationError(AutomationError):
    """Raised when configuration is invalid."""


class FileOperationError(AutomationError):
    """Raised when a file operation fails."""


class ValidationError(AutomationError):
    """Raised when input validation fails."""


class CommandExecutionError(AutomationError):
    """Raised when an external command fails."""
