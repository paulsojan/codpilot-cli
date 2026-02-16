import keyring
import questionary
import os
import subprocess
import typer

SERVICE_NAME = "github-agent"
LLM_TOKEN_KEY = "llm_api_token"
LLM_MODEL_KEY = "llm_model"


def ask_llm_token(model):
    token = keyring.get_password(SERVICE_NAME, LLM_TOKEN_KEY)

    if token:
        set_llm_token_to_env(token)
        return

    token = questionary.password(
        f"🔑 Enter your {model} token:",
    ).ask()

    if not token:
        typer.echo("❌ LLM token is required")
        raise SystemExit(1)

    if ping_model(model, token):
        keyring.set_password(SERVICE_NAME, LLM_TOKEN_KEY, token)
        set_llm_token_to_env(token)
        typer.echo("🔐 Token saved securely in system keychain.")


def set_llm_token_to_env(token):
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)
    if selected_model == "OpenAI":
        os.environ["OPENAI_API_KEY"] = token
    elif selected_model == "Anthropic":
        os.environ["ANTHROPIC_API_KEY"] = token
    else:
        os.environ["GEMINI_API_KEY"] = token


def ping_model(model, token):
    typer.echo("🤖 Pinging {}".format(model))
    try:
        if model == "OpenAI":
            cmd = [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "https://api.openai.com/v1/models",
                "-H",
                f"Authorization: Bearer {token}",
            ]

        elif model == "Anthropic":
            cmd = [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "https://api.anthropic.com/v1/models",
                "-H",
                f"x-api-key: {token}",
                "-H",
                "anthropic-version: 2023-06-01",
            ]

        elif model == "Gemini":
            cmd = [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                f"https://generativelanguage.googleapis.com/v1beta/models?key={token}",
            ]

        else:
            typer.echo("❌ Unknown model provider")
            raise SystemExit(1)

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout.strip() == "200":
            typer.echo("✅ Model ping successful.")
            return True
        else:
            typer.echo("❌ Model ping failed. Invalid token.")
            raise SystemExit(1)

    except Exception as e:
        typer.echo(f"Error: {e}")
        raise SystemExit(1)
