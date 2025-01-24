import ast
import logging
from pathlib import Path
from typing import List
from dj_inspector.checkers.security_checker import SecurityChecker
from dj_inspector.utils.constants import SecurityCheckResult, SecurityCheck, Severity

logger = logging.getLogger(__name__)

ADMIN_URL_BLACKLIST = [
    "admin/",
    "administrator/",
    "django-admin/",
    "admin-panel/",
    "admin-console/",
    "admin-login/",
    "admin-login/",
]


class AdminURLChecker(SecurityChecker):
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.results: List[SecurityCheckResult] = []

    def run_check(self) -> List[SecurityCheckResult]:
        admin_url_check = SecurityCheck(
            setting="ADMIN_URL",
            message="Admin URL should not be a common or easily guessable path",
            severity=Severity.HIGH,
            description="The admin URL should be unique and not easily guessable (minimum 10 characters)",
            official_documentation="https://docs.djangoproject.com/en/stable/ref/settings/#admin-url",
            passed_function=lambda value: len(value) > 10
            and value not in ADMIN_URL_BLACKLIST,
        )

        urls_file = self.project_path / "config" / "urls.py"
        if not urls_file.exists():
            urls_file = self.project_path / "urls.py"

        admin_url = self.extract_admin_url(urls_file)
        passed = admin_url_check.passed_function(admin_url)
        result = SecurityCheckResult(security_check=admin_url_check, passed=passed)
        self.results.append(result)

        return self.results

    def extract_admin_url(self, urls_file: Path) -> str:
        with urls_file.open("r") as file:
            tree = ast.parse(file.read(), filename=str(urls_file))

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "path"
            ):
                if (
                    len(node.args) >= 2
                    and isinstance(node.args[0], ast.Str)
                    and isinstance(node.args[1], ast.Attribute)
                ):
                    if (
                        node.args[1].attr == "urls"
                        and node.args[1].value.attr == "site"
                        and node.args[1].value.value.id == "admin"
                    ):
                        return node.args[0].s
        return ""
