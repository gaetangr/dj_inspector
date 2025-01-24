import unittest
from dj_inspector.utils.constants import SecurityCheck, SecurityCheckResult, SecuritySetting, Severity

class TestSecurityCheck(unittest.TestCase):
    def setUp(self):
        self.security_check = SecurityCheck(
            setting=SecuritySetting.DEBUG,
            message="DEBUG enabled in production",
            severity=Severity.CRITICAL,
            description="Debug mode must be disabled in production for security",
            official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
            passed_function=lambda value: value is False,
        )

    def test_security_check_attributes(self):
        self.assertEqual(self.security_check.setting, SecuritySetting.DEBUG)
        self.assertEqual(self.security_check.message, "DEBUG enabled in production")
        self.assertEqual(self.security_check.severity, Severity.CRITICAL)
        self.assertEqual(self.security_check.description, "Debug mode must be disabled in production for security")
        self.assertEqual(self.security_check.official_documentation, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug")
        self.assertTrue(callable(self.security_check.passed_function))

    def test_security_check_passed_function(self):
        self.assertTrue(self.security_check.passed_function(False))
        self.assertFalse(self.security_check.passed_function(True))

class TestSecurityCheckResult(unittest.TestCase):
    def setUp(self):
        self.security_check = SecurityCheck(
            setting=SecuritySetting.DEBUG,
            message="DEBUG enabled in production",
            severity=Severity.CRITICAL,
            description="Debug mode must be disabled in production for security",
            official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
            passed_function=lambda value: value is False,
        )
        self.result_passed = SecurityCheckResult(security_check=self.security_check, passed=True)
        self.result_failed = SecurityCheckResult(security_check=self.security_check, passed=False)

    def test_security_check_result_attributes(self):
        self.assertEqual(self.result_passed.security_check, self.security_check)
        self.assertTrue(self.result_passed.passed)
        self.assertFalse(self.result_failed.passed)

if __name__ == "__main__":
    unittest.main()
