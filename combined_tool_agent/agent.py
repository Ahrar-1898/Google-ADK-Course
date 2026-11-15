from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import google_search
from google.adk.tools.langchain_tool import LangchainTool
from google.genai import types
from langchain_tavily import TavilySearch

MODEL = "gemini-2.5-flash"


# 1. Function tool
def get_current_time(timezone: str) -> dict:
    """Get the current date and time in a given time zone.

    Use this whenever the user asks what time or date it is somewhere.

    Args:
        timezone: An IANA time zone name, e.g. "Asia/Kolkata",
            "America/New_York" or "Europe/London".

    Returns:
        A dict with "status" ("success" or "error"). On success it also has
        "timezone", "date", "time" and "weekday". On error it has
        "error_message".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "error_message": (
                f"Unknown time zone '{timezone}'. "
                "Use an IANA name like 'Asia/Kolkata'."
            ),
        }
    return {
        "status": "success",
        "timezone": timezone,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "weekday": now.strftime("%A"),
    }


# 2. Third-party tool: LangChain's Tavily search, wrapped for ADK
tavily_tool = LangchainTool(
    tool=TavilySearch(max_results=5, topic="general")
)


# 3. One agent with all four tools
root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description=(
        "A helpful assistant that can search the web, run Python code "
        "and tell the time anywhere."
    ),
    
    instruction=(
        "You are a reliable and intelligent AI assistant powered by "
        "Google ADK and Groq. Your job is to answer user questions "
        "accurately, clearly, and helpfully using the available tools.\n\n"

        "TOOL USAGE RULES:\n"

        "1. TAVILY SEARCH:\n"
        "- Use Tavily Search whenever the user asks for current information, "
        "recent news, latest developments, research, comparisons, "
        "or information that may have changed over time.\n"
        "- Use search results to verify facts rather than relying only "
        "on your internal knowledge.\n"
        "- For detailed research, examine multiple relevant results.\n"
        "- Never invent URLs, sources, statistics, or search findings.\n\n"

        "2. CURRENT TIME TOOL:\n"
        "- Always call get_current_time when the user asks for the "
        "current time, date, weekday, or day/night status in a location.\n"
        "- Identify the correct IANA timezone for the requested city.\n"
        "- Examples: Mumbai -> Asia/Kolkata, "
        "Zurich -> Europe/Zurich, London -> Europe/London, "
        "New York -> America/New_York.\n"
        "- Never guess or calculate the current time using your "
        "internal knowledge.\n"
        "- If the timezone is invalid, explain the error and ask "
        "for clarification when necessary.\n"
        "- When answering, mention the city, country, local time, "
        "date, weekday, and day/night status when relevant.\n\n"

        "3. GENERAL QUESTIONS:\n"
        "- Answer general conceptual and educational questions "
        "using your internal knowledge when appropriate.\n"
        "- Explain technical concepts step by step when needed.\n"
        "- Use simple, clear language and practical examples.\n"
        "- Do not perform unnecessary searches for stable concepts.\n\n"

        "ACCURACY AND RELIABILITY:\n"
        "- Never fabricate information or pretend a tool succeeded "
        "when it failed.\n"
        "- If a tool returns an error, explain the problem honestly.\n"
        "- Distinguish verified information from assumptions.\n"
        "- If information is insufficient, clearly say so.\n\n"

        "RESPONSE STYLE:\n"
        "- Give direct answers before additional explanations.\n"
        "- Use headings, bullet points, and tables when useful.\n"
        "- Keep simple answers concise.\n"
        "- Provide detailed explanations for complex questions.\n"
        "- Include relevant sources when using search results.\n"
        "- Avoid unnecessary repetition."
    ),

    tools=[google_search, tavily_tool, get_current_time],  # built-in + third-party + function
    code_executor=BuiltInCodeExecutor(),                    # code execution goes here, not in tools
    generate_content_config=types.GenerateContentConfig(
        tool_config=types.ToolConfig(include_server_side_tool_invocations=True),
    )
)