from src.workflows.agent_workflow import agent_workflow
import typer
import asyncio
from src.cli.inputs import (
    ask_repo_url,
    ask_agent_type,
    ask_llm_model,
    ask_github_token,
)
from src.cli.llm import ask_llm_token
from rich.console import Console
from rich.panel import Panel
from rich import box
from importlib.metadata import version
from src.cli.spinner import run_with_spinner

console = Console()


def run():
    console.print(
        Panel(
            f"[bold cyan]CodPilot[/bold cyan] [green]v{version('codpilot')}[/green]\n"
            "[dim]Autonomous coding agent for GitHub[/dim]",
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 4),
        )
    )
    agent_type, description = ask_agent_type()
    repo_url = ask_repo_url(agent_type)
    model = ask_llm_model()
    ask_llm_token(model)
    ask_github_token()

    asyncio.run(
        run_with_spinner(
            agent_workflow(
                repo_url=repo_url, agent_type=agent_type, description=description
            )
        )
    )

    typer.echo("✅ Execution completed")
