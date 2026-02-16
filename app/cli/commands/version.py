import typer
from importlib.metadata import version


def version_callback(value: bool):
    if value:
        typer.echo(f"codpilot v{version('codpilot')}")
        raise typer.Exit()
