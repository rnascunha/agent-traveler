"""
Responsible to gather all the extracted and researched information and
output a document (markdown format).
"""

from google.adk.agents import Agent
from agent_traveler.libs.constants import REPORT_AGENT_MODEL

from .prompt import prompt

report_agent = Agent(
    model=REPORT_AGENT_MODEL,
    name="report_agent",
    description="Summarize and report trip data agent",
    instruction=prompt,
    output_key="report_data",
)
