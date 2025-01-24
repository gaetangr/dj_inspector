import unittest
from pathlib import Path
from dj_inspector.checkers.admin_checker import AdminURLChecker
from dj_inspector.utils.constants import SecurityCheckResult, SecurityCheck, Severity

class TestAdminURLChecker(unittest.TestCase):
    def setUp(self):
        self.project_path = Path("test_project")
        self.checker = AdminURLChecker(self.project_path)

    def test_admin_url_check_passed(self):
        # Create a mock urls.py file with a secure admin URL
        urls_content = """
        from django.contrib import admin
        from django.urls import path

        urlpatterns = [
            path('secure-admin/', admin.site.urls),
        ]
        """
        urls_file = self.project_path / "urls.py"
        urls_file.parent.mkdir(parents=True, exist_ok=True)
        urls_file.write_text(urls_content)

        results = self.checker.run_check()
        self.assertTrue(results[0].passed)

    def test_admin_url_check_failed(self):
        # Create a mock urls.py file with an insecure admin URL
        urls_content = """
        from django.contrib import admin
        from django.urls import path

        urlpatterns = [
            path('admin/', admin.site.urls),
        ]
        """
        urls_file = self.project_path / "urls.py"
        urls_file.parent.mkdir(parents=True, exist_ok=True)
        urls_file.write_text(urls_content)

        results = self.checker.run_check()
        self.assertFalse(results[0].passed)

    def tearDown(self):
        # Clean up the mock urls.py file
        urls_file = self.project_path / "urls.py"
        if urls_file.exists():
            urls_file.unlink()
        if urls_file.parent.exists():
            urls_file.parent.rmdir()

if __name__ == "__main__":
    unittest.main()
