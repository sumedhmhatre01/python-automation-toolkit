from laptop_automation.core.exceptions import (
    AutomationError,
    ConfigurationError,
)


def test_automation_error_is_exception():
    error = AutomationError("Test error")

    assert isinstance(error, Exception)


def test_configuration_error_inherits_automation_error():
    error = ConfigurationError("Invalid configuration")

    assert isinstance(error, AutomationError)
