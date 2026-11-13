# Google ADK — Quick Revision Notes

Short notes for understanding the examples in this repository and explaining them in an interview.

> **Scope:** ADK introduction, the first agent, and built-in/third-party tools. Function tools will be documented after that lesson is complete.

## 1. What is Google ADK?

**Google Agent Development Kit (ADK)** is a framework for building and running AI agents. An agent combines:

- **Model** — generates and reasons about responses.
- **Instructions** — tell the agent how to behave.
- **Tools (optional)** — let it search, run code, or use other services.

ADK connects these parts and manages the tool-call flow. Use it to move from a simple chat agent to agents that can take useful actions.

**Simple flow:** User asks → model decides whether a tool is needed → ADK runs the tool → model responds with the result.

## 2. Models used in this repository

| Model choice | When to use |
|---|---|
| **Gemini 3.5 Flash** | Preferred for better results, if this model ID is available for your Google account and ADK setup. |
| **Gemini 2.5 Flash** | Used in the Google Search and code-execution examples; a lower-cost option, but responses may be less capable. |
| **Groq model** | The first agent uses `groq/openai/gpt-oss-120b` through LiteLLM. Useful for free-tier/low-cost practice when available; quality and quotas can vary. |

Model names and free-tier access can change. Confirm the current model ID and provider limits before relying on them. The code currently runs **Gemini 2.5 Flash** in two examples; the first agent uses **Groq**.

## 3. First ADK agent

File: [`First-ADK_Agent/personal_bot/agent.py`](First-ADK_Agent/personal_bot/agent.py)

```python
root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge.",
)
```

- `model`: language model used by the agent.
- `name`: agent's programmatic name.
- `description`: short summary of the agent's purpose.
- `instruction`: guidance for the agent's responses.
- `root_agent`: entry-point variable discovered by ADK.

This is a basic conversational agent. It has **no tools**, so it cannot search the web or execute code through an ADK tool.

## 4. Built-in and third-party tools

A **tool** gives an agent a capability beyond generating text. The model chooses when to call an available tool; ADK (or an adapter) runs it and returns its result.

### Built-in examples

- **Google Search** — [`google_agent/agent.py`](Built-in%20%26%20Third-party_Tools/google_agent/agent.py) registers ADK's `google_search` tool to find current information. Uses `gemini-2.5-flash`.
- **Code execution** — [`code_execution_agent/agent.py`](Built-in%20%26%20Third-party_Tools/code_execution_agent/agent.py) configures ADK's `BuiltInCodeExecutor` for calculations and data analysis. Uses `gemini-2.5-flash`.

**Safety:** Model-generated code is untrusted. Run it in an appropriately restricted environment and protect credentials, files, and network access.

### Third-party example: Tavily Search

File: [`tavily_search_tool/agent.py`](Built-in%20%26%20Third-party_Tools/tavily_search_tool/agent.py)

1. `TavilySearch` creates the external search tool.
2. ADK's `LangchainTool` adapter wraps it.
3. The wrapper is added to the agent's `tools` list.

Unlike ADK's Google Search tool, Tavily is an external service and needs its own package and API credential.

| | Built-in | Third-party |
|---|---|---|
| Example | Google Search, code executor | Tavily Search |
| Provided by | ADK integration | External provider/library |
| Consider | Model compatibility and provider setup | Extra dependency, credentials, cost, and service limits |

## 5. Run the examples

`requirements.txt` lists the packages used by the examples. Create and activate a virtual environment, then install them:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the required provider credentials securely in your environment: Groq for the first agent, Google/Gemini for the Gemini examples, and Tavily for the Tavily example. **Never commit API keys.**

Run from the parent directory of the agent package:

```powershell
Set-Location .\First-ADK_Agent
adk run personal_bot

Set-Location "..\Built-in & Third-party_Tools"
adk run google_agent
```

Replace `google_agent` with `code_execution_agent` or `tavily_search_tool` to run those examples. Use `adk web` from the same directory to open the local development UI.

## 6. Interview revision

**What is ADK?**
ADK is a framework for building AI agents from a model, instructions, and optional tools. It manages how an agent uses its tools and returns a response.

**What does the first agent do?**
It uses a Groq-hosted model through LiteLLM and answers user questions using its instruction. It has no search or code-execution tools.

**Built-in vs. third-party tools?**
Built-in tools are provided through ADK integrations, such as Google Search. Third-party tools come from external providers; this project connects Tavily to ADK using a LangChain adapter.

**Quick recall:** Google Search = current web information · Code executor = calculations/data work · Tavily = external search service.
