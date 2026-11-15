# Google ADK Course

Hands-on examples for learning Google's Agent Development Kit (ADK), from a basic agent to agents that use tools and external services.

## Learning path

| Step | Example | What it covers |
|---|---|---|
| 1 | `First-ADK_Agent/personal_bot` | A basic conversational agent |
| 2 | `Built-in & Third-party_Tools` | Google Search, code execution, and Tavily Search |
| 3 | `Function_Tools/world_clock_agent` | A custom Python function tool |
| 4 | `combined_tool_agent` | Combining built-in, third-party, and function tools |
| 5 | `course_refund_agent` | A tool-using agent with a sample refund workflow |
| 6 | `mcp_agent` | Connecting an agent to MCP servers |
| 7 | `coding_agent` | A coding agent with workspace tools |

## Setup

From the repository root, create a virtual environment and install the main dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the credentials needed by the example you want to run. For example:

```powershell
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GROQ_API_KEY = "your-groq-api-key"
$env:TAVILY_API_KEY = "your-tavily-api-key"
$env:GITHUB_TOKEN = "your-github-token" # mcp_agent
$env:GITHUB_PAT = "your-github-token"   # coding_agent (optional)
```

MCP examples use Node.js/npm to run their servers. Set only the credentials required by the agent you run; never commit API keys or tokens.

## Run an agent

Run ADK from the directory containing the agent package:

```powershell
Set-Location .\First-ADK_Agent
adk run personal_bot
```

For the other examples, use the corresponding directory and agent name:

| Directory | Agent |
|---|---|
| `Built-in & Third-party_Tools` | `google_agent`, `code_execution_agent`, or `tavily_search_tool` |
| `Function_Tools` | `world_clock_agent` |
| Repository root | `combined_tool_agent`, `course_refund_agent`, `mcp_agent`, or `coding_agent` |

For example, from the repository root:

```powershell
adk run combined_tool_agent
```

To open ADK's local development UI, run `adk web` from the same directory you would use for `adk run`. The refund example also needs its sample database initialized once:

```powershell
python -m course_refund_agent.setup_database
```

For agent-specific setup, see its README where available or inspect its requirements and configuration.

## Updating this README

Keep this page as the course overview. When a new lesson or agent is completed, add its row to the end of the learning path and update the run instructions if needed—preserve the existing sections rather than rewriting the README.
