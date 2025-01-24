import unittest
from dj_inspector.utils.constants import SecurityCheck, SecurityCheckResult, Severity, SecuritySetting

class TestSecurityCheck(unittest.TestCase):
    def test_security_check_initialization(self):
        security_check = SecurityCheck(
            setting=SecuritySetting.DEBUG,
            message="DEBUG enabled in production",
            severity=Severity.CRITICAL,
            description="Debug mode must be disabled in production for security",
            official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
            passed_function=lambda value: value is False,
        )
        self.assertEqual(security_check.setting, SecuritySetting.DEBUG)
        self.assertEqual(security_check.message, "DEBUG enabled in production")
        self.assertEqual(security_check.severity, Severity.CRITICAL)
        self.assertEqual(security_check.description, "Debug mode must be disabled in production for security")
        self.assertEqual(security_check.official_documentation, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug")
        self.assertTrue(callable(security_check.passed_function))

class TestSecurityCheckResult(unittest.TestCase):
    def test_security_check_result_initialization(self):
        security_check = SecurityCheck(
            setting=SecuritySetting.DEBUG,
            message="DEBUG enabled in production",
            severity=Severity.CRITICAL,
            description="Debug mode must be disabled in production for security",
            official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
            passed_function=lambda value: value is False,
        )
        result = SecurityCheckResult(security_check=security_check, passed=True)
        self.assertEqual(result.security_check, security_check)
        self.assertTrue(result.passed)

if __name__ == "__main__":
    unittest.main()
