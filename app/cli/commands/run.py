from app.workflows.agent_workflow import agent_workflow
import logging
import asyncio
from app.cli.inputs import (
    ask_repo_url,
    ask_agent_type,
    ask_llm_model,
    ask_github_token,
)
from app.cli.llm import ask_llm_token
from rich.console import Console
from rich.panel import Panel
from rich import box
from importlib.metadata import version

console = Console()


def run():
    console.print(
        Panel(
            f"[bold cyan]CodePilot[/bold cyan] [green]v{version('codepilot')}[/green]\n"
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
        agent_workflow(
            repo_url=repo_url, agent_type=agent_type, description=description
        )
    )

    logging.info("✅ Execution completed")
