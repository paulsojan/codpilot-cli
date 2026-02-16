import keyring
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

MCP_URL = "https://api.githubcopilot.com/mcp/"
SERVICE_NAME = "codpilot"
TOKEN_KEY = "github_token"


def github_mcp():
    token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)

    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            timeout=120,
            url=MCP_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "X-MCP-Toolsets": "all",
                "X-MCP-Readonly": "false",
            },
        ),
    )
