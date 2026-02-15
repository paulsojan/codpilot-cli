import typer
from app.cli.commands.run import run as run_command
from app.cli.inputs import reset_github_token, change_llm_model
import asyncio
import logging

app = typer.Typer(help="🤖 CodePilot CLI")

logging.basicConfig(level=logging.INFO)

app.command("run")(run_command)
app.command("reset-github-token", help="🔑 Reset the stored GitHub token.")(
    reset_github_token
)
app.command("reset-llm", help="🤖 Reset the LLM model.")(change_llm_model)


async def main():
    await app()


if __name__ == "__main__":
    asyncio.run(main())
