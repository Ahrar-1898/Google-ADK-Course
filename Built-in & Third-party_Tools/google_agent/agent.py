from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import google_search

root_agent = Agent(
    model='gemini-2.5-flash',  # must used gemini-3.5-flash for good results but right now i used gemini-2.5-flash because of the cost.
    name='root_agent',
    description="A helpful assistant that can search the web and answer user questions.",
    instruction=(
        "Answer user questions accurately and helpfully. "
        "Use Google Search when you need current information "
        "or need to verify facts. "
        "If you are unsure, say you don't know."
    ),
    tools=[google_search],
)
