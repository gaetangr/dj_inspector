import unittest
from pathlib import Path
from unittest.mock import patch, mock_open
from dj_inspector.checkers.setting_checker import SettingsChecker
from dj_inspector.utils.constants import SecurityCheckResult, SecuritySetting, Severity

class TestSettingsChecker(unittest.TestCase):
    def setUp(self):
        self.project_path = Path("test_project")
        self.settings_module = "settings"
        self.checker = SettingsChecker(self.project_path, self.settings_module)

    @patch("builtins.open", new_callable=mock_open, read_data="DEBUG = True")
    @patch("pathlib.Path.exists", return_value=True)
    def test_debug_setting(self, mock_exists, mock_open):
        result = self.checker._check_setting(SecuritySetting.DEBUG)
        self.assertFalse(result.passed)

    @patch("builtins.open", new_callable=mock_open, read_data="SECRET_KEY = 'django-insecure-1234567890'")
    @patch("pathlib.Path.exists", return_value=True)
    def test_secret_key_setting(self, mock_exists, mock_open):
        result = self.checker._check_setting(SecuritySetting.SECRET_KEY)
        self.assertFalse(result.passed)

    @patch("builtins.open", new_callable=mock_open, read_data="CSRF_COOKIE_SECURE = True")
    @patch("pathlib.Path.exists", return_value=True)
    def test_csrf_cookie_secure_setting(self, mock_exists, mock_open):
        result = self.checker._check_setting(SecuritySetting.CSRF_COOKIE_SECURE)
        self.assertTrue(result.passed)

    @patch("builtins.open", new_callable=mock_open, read_data="SESSION_COOKIE_SECURE = True")
    @patch("pathlib.Path.exists", return_value=True)
    def test_session_cookie_secure_setting(self, mock_exists, mock_open):
        result = self.checker._check_setting(SecuritySetting.SESSION_COOKIE_SECURE)
        self.assertTrue(result.passed)

    @patch("builtins.open", new_callable=mock_open, read_data="X_FRAME_OPTIONS = 'DENY'")
    @patch("pathlib.Path.exists", return_value=True)
    def test_x_frame_options_setting(self, mock_exists, mock_open):
        result = self.checker._check_setting(SecuritySetting.X_FRAME_OPTIONS)
        self.assertTrue(result.passed)

    def tearDown(self):
        settings_file = self.project_path / f"{self.settings_module}.py"
        if settings_file.exists():
            settings_file.unlink()
        if settings_file.parent.exists():
            settings_file.parent.rmdir()

if __name__ == "__main__":
    unittest.main()
