from google.adk.runners import App, Runner
from app.services.runner_service import RunnerService
from google.adk.sessions import InMemorySessionService
import uuid

session_service = InMemorySessionService()


async def agent_workflow(repo_url, agent_type, description=None):
    app = App(
        name="CodingAgentWorkflow",
        root_agent=get_agent_by_type(agent_type),
    )

    runner = get_runner(app)
    session_id = uuid.uuid4().hex
    await create_session(app, runner, session_id)

    runner_service = RunnerService(runner=runner, session_id=session_id)
    await runner_service.process(repo_url, description)


async def create_session(app, runner, session_id):
    return await runner.session_service.create_session(
        app_name=app.name, user_id="user", session_id=session_id
    )


def get_runner(app: App):
    return Runner(
        app=app,
        session_service=session_service,
    )


def get_agent_by_type(agent_type):
    if agent_type == "review_pr":
        from app.agents.pr_review_agent import pr_review_agent

        return pr_review_agent
    elif agent_type == "create_feature":
        from app.agents.feature_agent import feature_agent

        return feature_agent
    elif agent_type == "suggest_changes":
        from app.agents.suggestion_agent import suggestion_agent

        return suggestion_agent
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
