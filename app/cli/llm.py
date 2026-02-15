import keyring
import questionary
import logging
import os

SERVICE_NAME = "github-agent"
LLM_TOKEN_KEY = "llm_api_token"
LLM_MODEL_KEY = "llm_model"


def ask_llm_token():
    token = keyring.get_password(SERVICE_NAME, LLM_TOKEN_KEY)

    if token:
        set_llm_token_to_env(token)
        return

    token = questionary.password("Enter your LLM API token:").ask()

    if not token:
        logging.error("❌ LLM token is required")
        raise SystemExit(1)

    keyring.set_password(SERVICE_NAME, LLM_TOKEN_KEY, token)
    set_llm_token_to_env(token)
    logging.info("🔐 Token saved securely in system keychain")


def delete_token():
    try:
        keyring.delete_password(SERVICE_NAME, LLM_TOKEN_KEY)
        logging.info("🗑️ Token removed from system keychain")
    except keyring.errors.PasswordDeleteError:
        logging.warning("⚠️ No token found to delete")


def set_llm_token_to_env(token):
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)
    if selected_model == "OpenAI":
        os.environ["OPENAI_API_KEY"] = token
    elif selected_model == "Anthropic":
        os.environ["ANTHROPIC_API_KEY"] = token
    else:
        os.environ["GEMINI_API_KEY"] = token
