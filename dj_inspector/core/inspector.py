from pathlib import Path
import logging
from typing import List

from dj_inspector.checkers.admin_checker import AdminURLChecker
from dj_inspector.checkers.setting_checker import SettingsChecker
from dj_inspector.utils.constants import COLORS, MESSAGES, Severity, SecurityCheckResult
import time
from rich.console import Console
from rich.progress import Progress

console = Console()
logger = logging.getLogger(__name__)


class DjangoSecurityInspector:
    def __init__(self, project_path: Path, settings_module: str):
        self.project_path: Path = project_path
        self.settings_module: str = settings_module
        self.checkers: List[SettingsChecker] = []
        self.results: List[SecurityCheckResult] = []

    def load_checks(self) -> None:
        """Load all security checks."""
        setting_check = SettingsChecker(
            project_path=self.project_path, settings_module=self.settings_module
        )
        admin_url_check = AdminURLChecker(project_path=self.project_path)
        self.checkers.extend([setting_check, admin_url_check])

    def _display_results(self) -> None:
        """Display security check results grouped by severity."""
        if not self.results:
            console.print(MESSAGES["no_issues"], style="green")
            return

        console.print(
            f"\n[bold]Checking settings module:[/bold] {self.settings_module}"
        )

        results_by_severity = {}
        passed_count = 0
        failed_count = 0

        for result in self.results:
            severity = result.security_check.severity
            if severity not in results_by_severity:
                results_by_severity[severity] = []
            results_by_severity[severity].append(result)
            if result.passed:
                passed_count += 1
            else:
                failed_count += 1

        # Display passed tests first
        passed_tests = [r for r in self.results if r.passed]
        if passed_tests:
            console.print("\n[bold green]Passed Checks:[/bold green]")
            for result in passed_tests:
                console.print(f"✓ {result.security_check.message}", style="green")

        # Display failed tests grouped by severity
        for severity in Severity:
            failed_tests = [
                r for r in results_by_severity.get(severity, []) if not r.passed
            ]
            if failed_tests:
                console.print(f"\n[bold]{severity.name} Issues:[/bold]")
                for result in failed_tests:
                    console.print(
                        f"✗ {result.security_check.message}", style=COLORS[severity]
                    )
                    console.print(
                        f"  Description: {result.security_check.description}",
                        style="dim",
                    )
                    console.print(
                        f"  Documentation: {result.security_check.official_documentation}",
                        style="blue underline",
                    )
                    console.print("")  # Add blank line between results

        # Display summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"✓ {passed_count} checks passed", style="green")
        console.print(f"✗ {failed_count} checks failed", style="red")

        critical_issues = len(
            [
                r
                for r in self.results
                if r.security_check.severity == Severity.CRITICAL and not r.passed
            ]
        )
        if critical_issues:
            console.print(
                MESSAGES["critical_found"].format(count=critical_issues),
                style="red bold",
            )
        console.print(MESSAGES["scan_complete"])

    def run(self) -> None:
        console.print(MESSAGES["scan_start"])
        self.load_checks()

        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Running security checks...", total=len(self.checkers)
            )

            for checker in self.checkers:
                try:
                    checker.run_check()
                    self.results.extend(checker.results)
                    progress.advance(task)
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error running checker: {e}")

        self._display_results()
