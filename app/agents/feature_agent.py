from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm
from app.agents.tools.github_mcp import github_mcp
import keyring

SERVICE_NAME = "github-agent"
LLM_MODEL_KEY = "llm_model"


def build_model():
    selected_model = keyring.get_password(SERVICE_NAME, LLM_MODEL_KEY)
    if selected_model == "OpenAI":
        return LiteLlm(model="openai/gpt-4.1-mini", temperature=0)
    elif selected_model == "Anthropic":
        return LiteLlm(model="anthropic/claude-3-7-sonnet-20250219", temperature=0)
    return "gemini-3-flash-preview"


def finish_task(tool_context: ToolContext):
    """Call this ONLY when a Pull Request URL has been successfully generated."""
    tool_context.actions.escalate = True
    return {"status": "complete"}


base_feature_agent = LlmAgent(
    name="CodeAnalyzerAgent",
    model=build_model(),
    instruction="""
    You are a coding agent.
    1. Analyze the repo. 2. Make changes. 3. Raise a Pull Request.

    IMPORTANT: If the chat history shows you already modified files but missed the PR,
    skip the analysis and call the PR tool immediately.
    """,
    output_key="worker_output",
    tools=[github_mcp()],
)

verifier_agent = LlmAgent(
    name="CodeVerifierAgent",
    model=build_model(),
    instruction="""
    Review the following output from the CodeAnalyzer:

    \"\"\"
    {{worker_output}}
    \"\"\"

    Task:
    - If a GitHub Pull Request URL is visible above, call 'finish_task' immediately.
    - If NO Pull Request URL is found, explicitly tell the worker: 'You failed to create a PR. Please execute the PR tool now.'
    """,
    tools=[finish_task],
)

feature_agent = LoopAgent(
    name="PrGenerationAgent",
    sub_agents=[base_feature_agent, verifier_agent],
    max_iterations=3,
)
