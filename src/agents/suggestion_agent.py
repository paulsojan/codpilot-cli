from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.tool_context import ToolContext

from src.agents.tools.github_mcp import github_mcp
from src.services.build_model_service import build_model


def finish_discussion(tool_context: ToolContext):
    """Signals that the agent has successfully contributed to the discussion."""
    tool_context.actions.escalate = True
    return {"status": "contribution_posted"}


base_agent = LlmAgent(
    name="IssueAdvisorAgent",
    model=build_model(),
    instruction="""
    You are a Technical Advisor specializing in GitHub Issues. Your goal is to provide deep technical insights on reported problems or feature requests.

    STEP 1: GATHER CONTEXT
    - Fetch the Issue description and ALL existing comments.
    - Search the codebase using relevant keywords from the issue to identify the specific files or functions involved.

    STEP 2: ANALYZE
    - Evaluate if the reported issue is a bug, a performance bottleneck, or a feature request.
    - Propose a technical strategy or root cause analysis based on the codebase search.
    - Acknowledge any previous comments to maintain a collaborative tone.

    STEP 3: POST COMMENT
    - Use the GitHub MCP tool to post your technical findings as a comment.

    STRICT RULES:
    - Do not look at Pull Requests. Never modify files or create branches.
    - Do not offer to draft code changes.
    """,
    output_key="worker_output",
    tools=[github_mcp()],
)

verifier_agent = LlmAgent(
    name="ActionVerifier",
    model=build_model(),
    instruction="""
    Review the 'worker_output'.

    If the output mentions it is a Pull Request:
       - Immediately call 'finish_discussion' to stop the loop.
    If the text indicates a GitHub comment was successfully submitted via a tool call, run 'finish_discussion'.
    If the text contains a technical analysis but NO evidence of a tool call (like 'comment_posted'),
    explicitly command the agent: 'I see your analysis. You must now use the GitHub MCP tool to post this as a comment on the issue.'
    """,
    tools=[finish_discussion],
)

suggestion_agent = LoopAgent(
    name="DiscussionAgent",
    sub_agents=[base_agent, verifier_agent],
    max_iterations=2,
)
