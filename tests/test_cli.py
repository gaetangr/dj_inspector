import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from dj_inspector.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("dj_inspector.cli.DjangoSecurityInspector")
    def test_main_success(self, MockInspector):
        mock_inspector = MagicMock()
        MockInspector.return_value = mock_inspector

        result = self.runner.invoke(main, ["test_project", "test_settings"])

        self.assertEqual(result.exit_code, 0)
        MockInspector.assert_called_once_with("test_project", "test_settings")
        mock_inspector.run.assert_called_once()

    @patch("dj_inspector.cli.DjangoSecurityInspector")
    def test_main_failure(self, MockInspector):
        mock_inspector = MagicMock()
        mock_inspector.run.side_effect = Exception("Test error")
        MockInspector.return_value = mock_inspector

        result = self.runner.invoke(main, ["test_project", "test_settings"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: Test error", result.output)
        MockInspector.assert_called_once_with("test_project", "test_settings")
        mock_inspector.run.assert_called_once()

if __name__ == "__main__":
    unittest.main()
