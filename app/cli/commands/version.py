import typer
from importlib.metadata import version


def version_callback(value: bool):
    if value:
        typer.echo(f"codepilot v{version('ai-coding-agent')}")
        raise typer.Exit()
