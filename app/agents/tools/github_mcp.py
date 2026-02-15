import keyring
import requests
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

MCP_URL = "https://api.githubcopilot.com/mcp/"
SERVICE_NAME = "github-agent"
TOKEN_KEY = "github_token"


def validate_github_token(token: str) -> bool:
    try:
        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def github_mcp():
    token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)

    if not validate_github_token(token):
        raise RuntimeError("❌ GitHub token is invalid or expired.")

    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            url=MCP_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "X-MCP-Toolsets": "all",
                "X-MCP-Readonly": "false",
            },
        ),
    )
