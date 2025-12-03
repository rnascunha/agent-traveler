"""
Agent to call four tools to create/save the outputs based on all the
data gathered.
"""


from google.adk.agents import Agent
from .prompt import prompt
from agent_traveler.libs.constants import OUTPUT_AGENT_MODEL
from agent_traveler.tools.places import create_map_points
from agent_traveler.tools.calendar import create_calendar_tool
from agent_traveler.tools.artifact import save_report_tool, save_state_tool

output_agent = Agent(
    name="output_agent",
    description="Creates all the outputs from data extracted and researched",
    model=OUTPUT_AGENT_MODEL,
    instruction=prompt,
    tools=[create_map_points, create_calendar_tool, save_report_tool, save_state_tool],
)
