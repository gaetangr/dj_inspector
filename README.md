# dj-inspector

🛡️ Django Security Inspector: Advanced Security Analysis Tool

[![PyPI version](https://badge.fury.io/py/dj-inspector.svg)](https://badge.fury.io/py/dj-inspector)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-inspector.svg)](https://pypi.org/project/dj-inspector/)
[![Django versions](https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-blue)](https://pypi.org/project/dj-inspector/)

## Description

`dj-inspector` is a specialized security analysis tool for Django applications that detects vulnerabilities, misconfigurations, and security anti-patterns. It helps ensure your Django project follows security best practices while also checking for related quality issues.

## Security Features

### Core Security Checks
- 🔒 Security middleware validation
- 🔑 Secrets and credentials exposure
- 🛡️ XSS/CSRF vulnerabilities
- 🔍 SQL injection detection
- 🚫 Authentication bypass risks
- ⚠️ Security-related deprecation issues

### Additional Analysis
- 📊 Security-impacting performance issues
- 🔍 Anti-patterns affecting security
- 🛠️ Configuration validation

## Installation

```bash
pip install dj-inspector
```

## Quick Start

```bash
# Run security scan
dj-inspector /path/to/project

# Detailed security report in HTML
dj-inspector /path/to/project --output html

# Strict security checks
dj-inspector /path/to/project --strict
```

## Security Scan Example

```
🛡️ dj-inspector v1.0.0 security scan

CRITICAL ISSUES
❌ settings.py: SECRET_KEY exposed in code
❌ views/api.py: SQL injection vulnerability in raw query
❌ middleware.py: SecurityMiddleware not enabled

HIGH RISK
⚠️ settings.py: DEBUG enabled in production
⚠️ views/auth.py: Missing rate limiting on login
⚠️ models/user.py: Password hash algorithm outdated

MEDIUM RISK
⚡ views/profile.py: CSRF token missing
⚡ templates/form.html: XSS vulnerability in form rendering
⚡ urls.py: Admin URL not changed from default
```

## Key Security Features

- **Django Settings Analysis**
  - Security middleware configuration
  - Debug mode detection
  - Secret key exposure
  - Password policies
  - Session security settings

- **Authentication & Authorization**
  - Permission checks
  - Session configuration
  - Password handling
  - Token security
  - Rate limiting

- **Data Security**
  - SQL injection prevention
  - Sensitive data exposure
  - Encryption usage
  - Safe query patterns

- **Request Security**
  - CSRF protection
  - XSS prevention
  - HTTP security headers
  - Input validation

## Configuration

Create `dj-inspector.yaml`:

```yaml
security:
  # Security checks configuration
  critical_checks:
    - secret_key_exposure
    - sql_injection
    - auth_bypass
  
  custom_checks:
    - path: security_checks/
    
  ignore:
    - tests/*
    - development.py

reporting:
  min_severity: medium
  export_format: html
```

## CI/CD Security Integration

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Django Security Scan
        run: |
          pip install dj-inspector
          dj-inspector . --strict --fail-on high
```

## Security Best Practices

The tool checks against Django Security Best Practices including:
- OWASP Top 10 for Django
- Django Security Documentation
- Common Vulnerability Patterns
- Industry Standard Security Practices

## Contributing

Found a security issue or want to add more checks? Check our [Contributing Guidelines](CONTRIBUTING.md).

## License

MIT License - See [LICENSE](LICENSE) file for details.