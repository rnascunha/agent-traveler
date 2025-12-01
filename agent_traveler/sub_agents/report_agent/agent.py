from google.adk.agents import Agent
from agent_traveler.libs.constants import REPORT_AGENT_MODEL

from agent_traveler.tools.artifact import save_report_tool
from agent_traveler.tools.calendar import create_calendar_tool
from .prompt import prompt

report_agent = Agent(
    model=REPORT_AGENT_MODEL,
    name="report_agent",
    description="Summarize and report trip data agent",
    instruction=prompt,
    output_key="report_data",
    tools=[save_report_tool, create_calendar_tool],
)
