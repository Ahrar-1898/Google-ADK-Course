
from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can write and run Python code to answer user questions.',
    instruction=(
        "Answer user questions accurately and helpfully. "
        "When a question involves calculations, data analysis, "
        "or anything that benefits from running code, write Python "
        "and execute it to find the answer. "
        "Then explain the results to the user clearly."
    ),
    code_executor=BuiltInCodeExecutor(),
)
