# dj-inspector

🛡️ Django Security Inspector: Advanced Security Analysis Tool


## Description

`dj-inspector` is a specialized security analysis tool for Django applications that detects vulnerabilities, misconfigurations, and security anti-patterns. It helps ensure your Django project follows security best practices while also checking for related quality issues.

## Installation

To install `dj-inspector`, you can use `pip`:

```sh
pip install dj-inspector
```

## Usage

Run the security analysis on your Django project:

```sh
python -m dj_inspector.cli <project_path> <settings_module>
```

### Examples

1. **Basic Usage**:

   ```sh
   python -m dj_inspector.cli /path/to/your/django/project production
   ```

   This command will run the security analysis on your Django project located at `/path/to/your/django/project` using the `production` settings module.

2. **Using a Virtual Environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install dj-inspector
   python -m dj_inspector.cli /path/to/your/django/project production
   ```

   This example demonstrates how to set up a virtual environment, install `dj-inspector`, and run the security analysis.

## Contributing

Found a security issue or want to add more checks? Check our [Contributing Guidelines](CONTRIBUTING.md).

## License

MIT License - See [LICENSE](LICENSE) file for details.
