import questionary
import keyring
import logging
from app.cli.llm import ask_llm_token

WORKFLOW_OPTIONS = {
    "review_pr": "Review PR",
    "create_feature": "Create a new feature",
    "suggest_changes": "Add your suggestions to the PR/Issue",
}
LLM_MODELS = ["Gemini", "OpenAI", "Anthropic"]
SERVICE_NAME = "github-agent"
LLM_MODEL_KEY = "llm_model"
LLM_TOKEN_KEY = "llm_api_token"


def ask_repo_url():
    repo_url = questionary.text(
        "Enter the GitHub repository URL:",
    ).ask()

    if not repo_url:
        raise ValueError("⛔️ Repo URL is required")

    return repo_url


def ask_agent_type():
    choice = questionary.select(
        "Select mode:",
        choices=[
            questionary.Choice(title=label, value=key)
            for key, label in WORKFLOW_OPTIONS.items()
        ],
    ).ask()

    if not choice:
        raise ValueError("Mode is required")

    description = None
    if choice == "create_feature":
        description = questionary.text(
            "Enter the details of the feature you want to create:",
        ).ask()

        if not description:
            raise ValueError("Description is required")

    return choice, description


def ask_llm_model():
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)

    if selected_model:
        return selected_model

    model = questionary.select(
        "Select LLM model:",
        choices=LLM_MODELS,
    ).ask()

    if not model:
        raise ValueError("LLM model is required")

    keyring.set_password(SERVICE_NAME, LLM_MODEL_KEY, model)
    return model


def ask_github_token():
    token = keyring.get_password(SERVICE_NAME, "github_token")

    if token:
        return

    token = questionary.password("Enter your GitHub API token:").ask()

    if not token:
        raise ValueError("GitHub token is required")

    keyring.set_password(SERVICE_NAME, "github_token", token)


def reset_github_token():
    existing = keyring.get_password(SERVICE_NAME, "github_token")

    if not existing:
        logging.error("⚠️ No GitHub token found in keyring.")
        return

    confirm = questionary.confirm(
        "Are you sure you want to reset the stored GitHub token?"
    ).ask()

    if not confirm:
        logging.info("ℹ️ Token reset cancelled.")
        return

    keyring.delete_password(SERVICE_NAME, "github_token")
    logging.info("🗑️ GitHub token removed.")

    ask_github_token()
    logging.info("GitHub token has been reset successfully.")


def change_llm_model():
    existing = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)

    if not existing:
        logging.error("⚠️ No LLM model found.")
        return

    confirm = questionary.confirm(
        "Are you sure you want to change the LLM model?"
    ).ask()

    if not confirm:
        logging.info("ℹ️ Change LLM model cancelled.")
        return

    keyring.delete_password(SERVICE_NAME, LLM_MODEL_KEY)
    ask_llm_model()
    keyring.delete_password(SERVICE_NAME, LLM_TOKEN_KEY)
    ask_llm_token()
