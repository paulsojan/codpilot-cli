import keyring
from google.adk.models.lite_llm import LiteLlm

SERVICE_NAME = "codpilot"
LLM_MODEL_KEY = "llm_model"


def build_model():
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)
    if selected_model == "OpenAI":
        return LiteLlm(model="openai/gpt-5-mini")
    elif selected_model == "Anthropic":
        return LiteLlm(model="anthropic/claude-3-7-sonnet-20250219", temperature=0)
    return "gemini-3-flash-preview"
