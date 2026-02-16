from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.tool_context import ToolContext
from src.agents.tools.github_mcp import github_mcp
from src.services.build_model_service import build_model


def finish_task(tool_context: ToolContext):
    """Call this ONLY when a Pull Request URL has been successfully generated."""
    tool_context.actions.escalate = True
    return {"status": "complete"}


base_feature_agent = LlmAgent(
    name="CodeAnalyzerAgent",
    model=build_model(),
    instruction="""
    You are a coding agent.
    1. Analyze the repo. 2. Make changes. 3. Raise a Draft Pull Request.

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
