import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from dj_inspector.core.inspector import DjangoSecurityInspector
from dj_inspector.utils.constants import SecurityCheckResult, SecurityCheck, Severity

class TestDjangoSecurityInspector(unittest.TestCase):
    def setUp(self):
        self.project_path = Path("test_project")
        self.settings_module = "settings"
        self.inspector = DjangoSecurityInspector(self.project_path, self.settings_module)

    @patch("dj_inspector.core.inspector.SettingsChecker")
    @patch("dj_inspector.core.inspector.AdminURLChecker")
    def test_load_checks(self, MockAdminURLChecker, MockSettingsChecker):
        self.inspector.load_checks()
        self.assertEqual(len(self.inspector.checkers), 2)
        self.assertIsInstance(self.inspector.checkers[0], MockSettingsChecker)
        self.assertIsInstance(self.inspector.checkers[1], MockAdminURLChecker)

    @patch("dj_inspector.core.inspector.SettingsChecker.run_check")
    @patch("dj_inspector.core.inspector.AdminURLChecker.run_check")
    def test_run(self, mock_admin_run_check, mock_settings_run_check):
        mock_admin_run_check.return_value = [
            SecurityCheckResult(
                security_check=SecurityCheck(
                    setting="ADMIN_URL",
                    message="Admin URL should not be a common or easily guessable path",
                    severity=Severity.HIGH,
                    description="The admin URL should be unique and not easily guessable (minimum 10 characters)",
                    official_documentation="https://docs.djangoproject.com/en/stable/ref/settings/#admin-url",
                    passed_function=lambda value: len(value) > 10
                ),
                passed=True
            )
        ]
        mock_settings_run_check.return_value = [
            SecurityCheckResult(
                security_check=SecurityCheck(
                    setting="DEBUG",
                    message="DEBUG enabled in production",
                    severity=Severity.CRITICAL,
                    description="Debug mode must be disabled in production for security",
                    official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
                    passed_function=lambda value: value is False
                ),
                passed=False
            )
        ]

        self.inspector.run()
        self.assertEqual(len(self.inspector.results), 2)
        self.assertTrue(self.inspector.results[0].passed)
        self.assertFalse(self.inspector.results[1].passed)

if __name__ == "__main__":
    unittest.main()
