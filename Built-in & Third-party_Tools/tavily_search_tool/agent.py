from google.adk.agents.llm_agent import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch

# 1. Create the langchain TavilySearch tool

tavily_search = TavilySearch(
    max_results = 5,
    topic = "general"
)

# wrap it so ADK can use it as a tool
tavily_tool = LangchainTool(
    name="tavily_search",
    description="A tool for searching the web using TavilySearch",
    tool=tavily_search
)

# 3. Give it to an agent that can use it
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can search the web.',
    instruction=(
        "Answer user questions accurately. "
        "Use the Tavily search tool when you need current information "
        "or need to verify facts."

    ),
    tools=[tavily_tool],
)
