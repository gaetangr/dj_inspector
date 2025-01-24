import click
from pathlib import Path
from rich.console import Console
from dj_inspector.core.inspector import DjangoSecurityInspector

console = Console()


@click.command()
@click.argument("project_path", type=click.Path(exists=True, path_type=Path))
@click.argument("settings_module", type=str)
def main(project_path: Path, settings_module: str) -> None:
    """
    Check Django project security settings.

    PROJECT_PATH: Path to the Django project
    SETTINGS_MODULE: Settings module to check (e.g. production, local)
    """
    try:
        inspector = DjangoSecurityInspector(project_path, settings_module)
        inspector.run()
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")


if __name__ == "__main__":
    main()
