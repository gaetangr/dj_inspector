import unittest
from unittest.mock import MagicMock
from dj_inspector.checkers.security_checker import SecurityChecker
from dj_inspector.utils.constants import SecurityCheckResult

class MockSecurityChecker(SecurityChecker):
    def run_check(self) -> list[SecurityCheckResult]:
        return [SecurityCheckResult(security_check=MagicMock(), passed=True)]

class TestSecurityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = MockSecurityChecker()

    def test_run_check(self):
        results = self.checker.run_check()
        self.assertIsInstance(results, list)
        self.assertIsInstance(results[0], SecurityCheckResult)
        self.assertTrue(results[0].passed)

if __name__ == "__main__":
    unittest.main()
