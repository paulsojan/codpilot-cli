from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.tool_context import ToolContext

from src.agents.tools.github_mcp import github_mcp
from src.services.build_model_service import build_model


def finish_review(tool_context: ToolContext):
    """Call this ONLY when the final PR summary and recommendation (Approve/Request Changes) have been posted."""
    tool_context.actions.escalate = True
    return {"status": "review_submitted"}


base_review_agent = LlmAgent(
    name="PullRequestReviewWorker",
    model=build_model(),
    instruction="""
        You are a senior software engineer.

        TASK:
        1. Use github_mcp to get the PR diff.
        2. Review files one by one.
        3.  Identify issues in:
            - Correctness
            - Edge cases
            - Security
            - Performance
            - Readability & maintainability
            - Architecture & consistency
            - Tests (missing or insufficient)
        4. For each issue, use the 'post_inline_comment' tool.

        RULES
        - NO POSITIVE FEEDBACK: Never post "Good," "Consistent," or "Correct." If code is good, skip it.
        - NO CHATTER: Do not explain your process.
        - For code improvement comment must include a ```suggestion``` block.

        IMPORTANT: Check the chat history. If you have already commented on certain files,
        DO NOT repeat them. Move to the next file in the diff.

        When finished with ALL files, provide a 'Final Summary' and call the tool to submit the overall review.
        """,
    output_key="review_output",
    tools=[github_mcp()],
)

review_verifier_agent = LlmAgent(
    name="ReviewVerifierAgent",
    model=build_model(),
    instruction="""
        You are an auditor. Examine the 'review_output' provided below:

        REVIEW_LOG:
        {{review_output}}

        CHECKLIST:
        - Did the worker post a final summary? (Yes/No)
        - Did the worker submit a formal recommendation (Approve/Reject)? (Yes/No)

        IF BOTH ARE YES: Call 'finish_review' immediately.
        IF NO: Tell the worker exactly what is missing (e.g., 'You reviewed the files but forgot to submit the final Approval').
    """,
    tools=[finish_review],
)

pr_review_agent = LoopAgent(
    name="AutonomousPrReviewer",
    sub_agents=[base_review_agent, review_verifier_agent],
    max_iterations=5,
)
