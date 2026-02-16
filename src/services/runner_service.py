from google.genai.types import Content, Part


class RunnerService:
    def __init__(self, runner, session_id):
        self.runner = runner
        self.session_id = session_id

    async def process(self, repo_url, description=None):
        final_text_parts = []

        if description:
            message = f"Here is the repository URL: {repo_url}\n\nHere are my instructions:\n{description}"
        else:
            message = f"Here is the repository URL: {repo_url}"

        async for event in self.runner.run_async(
            user_id="user",
            session_id=self.session_id,
            new_message=Content(parts=[Part(text=message)], role="user"),
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_text_parts.append(part.text)

            if event.is_final_response() and event.actions and event.actions.escalate:
                return (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )

        return (
            "".join(final_text_parts) if final_text_parts else "No response generated."
        )
