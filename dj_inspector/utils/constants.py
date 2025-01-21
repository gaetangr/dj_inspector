from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable


class SecuritySetting(Enum):
    DEBUG = "DEBUG"
    SECRET_KEY = "SECRET_KEY"
    CSRF_COOKIE_SECURE = "CSRF_COOKIE_SECURE"
    SESSION_COOKIE_SECURE = "SESSION_COOKIE_SECURE"
    X_FRAME_OPTIONS = "X_FRAME_OPTIONS"
    SECURE_HSTS_SECONDS = "SECURE_HSTS_SECONDS"
    SECURE_CONTENT_TYPE_NOSNIFF = "SECURE_CONTENT_TYPE_NOSNIFF"
    SECURE_HSTS_INCLUDE_SUBDOMAINS = "SECURE_HSTS_INCLUDE_SUBDOMAINS"
    SECURE_HSTS_PRELOAD = "SECURE_HSTS_PRELOAD"
    SECURE_REFERRER_POLICY = "SECURE_REFERRER_POLICY"
    SECURE_SSL_REDIRECT = "SECURE_SSL_REDIRECT"
    SECURE_BROWSER_XSS_FILTER = "SECURE_BROWSER_XSS_FILTER"
    CSRF_TRUSTED_ORIGINS = "CSRF_TRUSTED_ORIGINS"


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SecurityCheck:
    setting: SecuritySetting
    message: str
    severity: Severity
    description: str
    official_documentation: str
    passed_function: Callable[[Any], bool]


@dataclass
class SecurityCheckResult:
    security_check: SecurityCheck
    passed: bool


class Severity(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    INFO = auto()


MESSAGES = {
    "scan_start": "🛡️  Starting security scan...",
    "scan_complete": "✨ Security scan complete",
    "critical_found": "❌ Found {count} critical security issues",
    "no_issues": "✅ No security issues found",
    "not_valid_project": "❌ No valid Django project found",
}

COLORS = {
    Severity.CRITICAL: "bright_red",
    Severity.HIGH: "red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "blue",
    Severity.INFO: "white",
}


SECURITY_CHECKS = {
    SecuritySetting.DEBUG: SecurityCheck(
        setting=SecuritySetting.DEBUG,
        message="DEBUG enabled in production",
        severity=Severity.CRITICAL,
        description="Debug mode must be disabled in production for security",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#debug",
        passed_function=lambda value: value is False,
    ),
    SecuritySetting.SECRET_KEY: SecurityCheck(
        setting=SecuritySetting.SECRET_KEY,
        message="SECRET_KEY should not be the default value",
        severity=Severity.CRITICAL,
        description="The SECRET_KEY setting must be unique and kept secret",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key",
        passed_function=lambda value: isinstance(value, str)
        and len(value) > 20
        and not value.startswith("django-insecure-"),
    ),
    SecuritySetting.CSRF_COOKIE_SECURE: SecurityCheck(
        setting=SecuritySetting.CSRF_COOKIE_SECURE,
        message="CSRF_COOKIE_SECURE not set to True",
        severity=Severity.HIGH,
        description="CSRF cookies must be secure in production",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-secure",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.SESSION_COOKIE_SECURE: SecurityCheck(
        setting=SecuritySetting.SESSION_COOKIE_SECURE,
        message="SESSION_COOKIE_SECURE not set to True",
        severity=Severity.HIGH,
        description="Session cookies must be secure in production",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#session-cookie-secure",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.X_FRAME_OPTIONS: SecurityCheck(
        setting=SecuritySetting.X_FRAME_OPTIONS,
        message="X_FRAME_OPTIONS not properly set",
        severity=Severity.MEDIUM,
        description="The X_FRAME_OPTIONS setting must be set to 'DENY' or 'SAMEORIGIN' to prevent clickjacking",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#x-frame-options",
        passed_function=lambda value: isinstance(value, str)
        and value.upper() in ["DENY", "SAMEORIGIN"],
    ),
    SecuritySetting.SECURE_HSTS_SECONDS: SecurityCheck(
        setting=SecuritySetting.SECURE_HSTS_SECONDS,
        message="SECURE_HSTS_SECONDS not set or too low",
        severity=Severity.HIGH,
        description="The SECURE_HSTS_SECONDS setting must be set to at least 1 year (31536000 seconds)",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-seconds",
        passed_function=lambda value: isinstance(value, int) and value >= 31536000,
    ),
    SecuritySetting.SECURE_CONTENT_TYPE_NOSNIFF: SecurityCheck(
        setting=SecuritySetting.SECURE_CONTENT_TYPE_NOSNIFF,
        message="SECURE_CONTENT_TYPE_NOSNIFF not set to True",
        severity=Severity.MEDIUM,
        description="The SECURE_CONTENT_TYPE_NOSNIFF setting must be set to True to prevent MIME type sniffing",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-content-type-nosniff",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.SECURE_HSTS_INCLUDE_SUBDOMAINS: SecurityCheck(
        setting=SecuritySetting.SECURE_HSTS_INCLUDE_SUBDOMAINS,
        message="SECURE_HSTS_INCLUDE_SUBDOMAINS not set to True",
        severity=Severity.MEDIUM,
        description="The SECURE_HSTS_INCLUDE_SUBDOMAINS setting must be set to True to include subdomains in HSTS",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-include-subdomains",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.SECURE_HSTS_PRELOAD: SecurityCheck(
        setting=SecuritySetting.SECURE_HSTS_PRELOAD,
        message="SECURE_HSTS_PRELOAD not set to True",
        severity=Severity.MEDIUM,
        description="The SECURE_HSTS_PRELOAD setting must be set to True to enable HSTS preload",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-preload",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.SECURE_REFERRER_POLICY: SecurityCheck(
        setting=SecuritySetting.SECURE_REFERRER_POLICY,
        message="SECURE_REFERRER_POLICY not properly set",
        severity=Severity.MEDIUM,
        description="The SECURE_REFERRER_POLICY setting must be set to an appropriate value",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-referrer-policy",
        passed_function=lambda value: isinstance(value, str)
        and value.lower()
        in [
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
        ],
    ),
    SecuritySetting.SECURE_SSL_REDIRECT: SecurityCheck(
        setting=SecuritySetting.SECURE_SSL_REDIRECT,
        message="SECURE_SSL_REDIRECT not set to True",
        severity=Severity.HIGH,
        description="The SECURE_SSL_REDIRECT setting must be set to True to redirect all HTTP requests to HTTPS",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-ssl-redirect",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.SECURE_BROWSER_XSS_FILTER: SecurityCheck(
        setting=SecuritySetting.SECURE_BROWSER_XSS_FILTER,
        message="SECURE_BROWSER_XSS_FILTER not set to True",
        severity=Severity.MEDIUM,
        description="The SECURE_BROWSER_XSS_FILTER setting must be set to True to enable the browser's XSS filter",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#secure-browser-xss-filter",
        passed_function=lambda value: value is True,
    ),
    SecuritySetting.CSRF_TRUSTED_ORIGINS: SecurityCheck(
        setting=SecuritySetting.CSRF_TRUSTED_ORIGINS,
        message="CSRF_TRUSTED_ORIGINS not properly set",
        severity=Severity.MEDIUM,
        description="The CSRF_TRUSTED_ORIGINS setting must be a non-empty list of trusted origins",
        official_documentation="https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins",
        passed_function=lambda value: isinstance(value, (list, tuple))
        and len(value) > 0
        and all(
            isinstance(origin, str) and origin.startswith(("http://", "https://"))
            for origin in value
        ),
    ),
}
