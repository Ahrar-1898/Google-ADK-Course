
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


# 1. Create a function that gets the current time in a given time zone
def get_current_time(timezone: str) -> dict:
    """Get the current date and time in a given time zone."""

    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "error_message": f"Unknown time zone '{timezone}'."
        }

    return {
        "status": "success",
        "timezone": timezone,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%I:%M %p"),
        "weekday": now.strftime("%A"),
    }


root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),  # must use a gemini-3.5-flash model for best results rather than a lite model
    name="clock_agent",
    description="Tells the current time and date anywhere in the world.",
    instruction=(
        "You tell users the current time and date in any city or country. "
        "Translate city names into their correct IANA timezones. "
        "For example, Zurich -> Europe/Zurich, "
        "Mumbai -> Asia/Kolkata, London -> Europe/London. "
        "Always call get_current_time before answering. "
        "Always mention the city, country, local time, date, weekday, "
        "and whether it is day or night. "
        "Never give only a day or night answer. "
        "Use the returned local time to determine day or night."
    ),
    tools=[get_current_time],
)
