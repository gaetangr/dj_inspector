import ast
import logging
from typing import Any, List, Tuple
from pathlib import Path
from dj_inspector.utils.constants import (
    SECURITY_CHECKS,
    SecurityCheckResult,
    SecuritySetting,
)

logger = logging.getLogger(__name__)


class SettingsChecker:
    def __init__(self, project_path: Path, settings_module: str):
        self.project_path = project_path
        self.settings_module = settings_module
        self.results: List[SecurityCheckResult] = []

    def _find_setting_value(self, setting_name: str) -> Tuple[bool, Any]:
        settings_file = self.project_path / f"{self.settings_module}.py"
        if not settings_file.exists():
            logger.error(f"Settings file not found: {settings_file}")
            return False, None

        try:
            with open(settings_file, "r") as file:
                tree = ast.parse(file.read(), filename=str(settings_file))
        except Exception as e:
            logger.error(f"Error parsing settings file: {e}")
            return False, None

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == setting_name:

                        if isinstance(node.value, ast.Call):
                            call = node.value
                            if (
                                isinstance(call.func, ast.Name)
                                and call.func.id == "env"
                            ) or (
                                isinstance(call.func, ast.Attribute)
                                and isinstance(call.func.value, ast.Name)
                                and call.func.value.id == "env"
                            ):

                                if len(call.args) > 1:
                                    default_value = call.args[1]
                                    if isinstance(default_value, ast.Constant):
                                        return True, default_value.value
                                elif call.keywords:
                                    for keyword in call.keywords:
                                        if keyword.arg == "default":
                                            if isinstance(keyword.value, ast.Constant):
                                                return True, keyword.value.value
                                return True, None

                        elif isinstance(node.value, ast.Constant):
                            return True, node.value.value
                        elif isinstance(node.value, (ast.List, ast.Tuple)):
                            values = []
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant):
                                    values.append(elt.value)
                            return True, values
                        return True, None
        return False, None

    def _check_setting(self, setting: SecuritySetting) -> SecurityCheckResult:
        security_check = SECURITY_CHECKS[setting]
        found, value = self._find_setting_value(security_check.setting.value)
        passed = found and security_check.passed_function(value)
        return SecurityCheckResult(
            security_check=security_check,
            passed=passed,
        )

    def run_check(self) -> List[SecurityCheckResult]:
        for setting in SecuritySetting:
            try:
                result = self._check_setting(setting=setting)
                self.results.append(result)
            except KeyError:
                logger.warning(f"{setting.value} not implemented")
                continue
        return self.results
