import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from mcp import StdioServerParameters

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN is not set in the environment variables.")

folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)

root_agent = Agent(
    name='github_publisher',
    model='gemini-2.5-flash',     # used gemini-3.5-flash for better result or more advance model
    
instruction=f"""
        You are a helpful Filesystem and GitHub assistant.

        LOCAL FILESYSTEM MCP:
        1. First, search the filesystem for the requested information.
        2. If relevant information exists, use it.
        3. If information is not available, use your parametric knowledge.
        4. Clearly mention when information comes from existing model knowledge and may be outdated.
        5. Never fabricate facts, dates, or sources.
        6. For latest news, never claim information is current without live verification.
        7. Manage files only inside {folder}.
        8. Use absolute paths only.

        GITHUB REMOTE MCP:
        1. Use GitHub MCP tools to manage repositories, files, branches, commits, issues, and pull requests.
        2. Retrieve relevant repository information before performing operations.
        3. Verify repository names, file paths, and branch names before making changes.
        4. Preserve existing file content unless modifications are requested.
        5. Never overwrite or delete existing resources without clear user authorization.
        6. Never fabricate repository information, commit details, URLs, or operation results.
        7. Confirm successful operations only after receiving tool confirmation.
        8. Ask for clarification if essential information is missing.

        TOOL SELECTION:
        1. Use LOCAL FILESYSTEM MCP for local file and folder operations.
        2. Use GITHUB REMOTE MCP for GitHub operations.
        3. For uploading local files to GitHub, read the local file first, then upload it.
        4. For downloading GitHub files locally, retrieve the GitHub content first, then save it locally.
        5. Use both MCP servers when a task involves both local files and GitHub.

        RESPONSE GUIDELINES:
        - Execute tasks using the appropriate tools.
        - Provide concise, accurate, and professional responses.
        - Avoid unnecessary explanations.
        - Report actual errors when operations fail.
        - Never claim an operation succeeded without confirmation.
        """,

    tools=[
        # read the file from the local machine
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        str(folder),
                    ],
                )
            )
        ),
        
        # Github MCP server
        MCPToolset(
            connection_params = StreamableHTTPConnectionParams(
                url = "https://api.githubcopilot.com/mcp",
                headers = {
                    "Authorization": f"Bearer {github_token}",
                }
            )
        )
        
    ]
)
