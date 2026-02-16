import questionary
import keyring
import logging
import requests
import time

from app.cli.llm import ask_llm_token

WORKFLOW_OPTIONS = {
    "review_pr": "Review PR",
    "create_feature": "Create a new feature",
    "suggest_changes": "Add your suggestions to the Issue",
}
LLM_MODELS = ["Gemini", "OpenAI", "Anthropic"]
SERVICE_NAME = "github-agent"
LLM_MODEL_KEY = "llm_model"
LLM_TOKEN_KEY = "llm_api_token"


def ask_repo_url(agent_type):
    if agent_type == "create_feature":
        msg = "Enter the GitHub repository URL:"
    elif agent_type == "suggest_changes":
        msg = "Enter the GitHub Issue URL:"
    else:
        msg = "Enter the GitHub PR URL:"

    repo_url = questionary.text(
        msg,
    ).ask()

    if not repo_url:
        logging.error("⛔️ URL is required")
        raise SystemExit(1)

    if not repo_url.startswith("https://github.com/"):
        logging.error("⛔️ Invalid URL")
        raise SystemExit(1)

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
        logging.error("Mode is required")
        raise SystemExit(1)

    description = None
    if choice == "create_feature":
        description = questionary.text(
            "Enter the details of the feature you want to create:",
        ).ask()

        if not description:
            logging.error("Description is required")
            raise SystemExit(1)

    return choice, description


def ask_llm_model():
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)

    if selected_model:
        logging.info(f"Using LLM model {selected_model}")
        return selected_model

    model = questionary.select(
        "Select LLM model:",
        choices=LLM_MODELS,
    ).ask()

    if not model:
        logging.error("LLM model is required")
        raise SystemExit(1)

    keyring.set_password(SERVICE_NAME, LLM_MODEL_KEY, model)

    return model


def ask_github_token():
    token = keyring.get_password(SERVICE_NAME, "github_token")

    if token:
        return

    token = questionary.password("Enter your GitHub API token:").ask()

    if not token:
        logging.error("⛔️ GitHub token is required")
        raise SystemExit(1)

    if _validate_github_token(token):
        keyring.set_password(SERVICE_NAME, "github_token", token)
        time.sleep(1)
    else:
        logging.error("⛔️ Invalid GitHub token")
        raise SystemExit(1)


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
    model = ask_llm_model()
    if keyring.get_password(SERVICE_NAME, LLM_TOKEN_KEY):
        keyring.delete_password(SERVICE_NAME, LLM_TOKEN_KEY)

    ask_llm_token(model)


def _validate_github_token(token: str) -> bool:
    try:
        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False
