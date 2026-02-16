import typer
from src.cli.commands.run import run as run_command
from src.cli.commands.version import version_callback
from src.cli.inputs import reset_github_token, change_llm_model

app = typer.Typer(help="🤖 CodPilot CLI")


@app.callback()
def get_version(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Get codpilot version.",
    ),
):
    pass


app.command("run", help="📀 Run the agent.")(run_command)
app.command("reset-github-token", help="🔑 Reset the stored GitHub token.")(
    reset_github_token
)
app.command("change-llm", help="🤖 Change the LLM model.")(change_llm_model)


if __name__ == "__main__":
    app()
