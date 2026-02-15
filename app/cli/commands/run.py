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


def run():
    try:
        agent_type, description = ask_agent_type()
        repo_url = ask_repo_url()
        ask_llm_model()
        ask_llm_token()
        ask_github_token()

        logging.info(f"📦 Repo: {repo_url}")
        logging.info(f"⚙️ Mode: {agent_type}")

        asyncio.run(
            agent_workflow(
                repo_url=repo_url, agent_type=agent_type, description=description
            )
        )

        logging.info("✅ Execution completed")

    except ValueError as e:
        logging.error(f"❌ {e}")
