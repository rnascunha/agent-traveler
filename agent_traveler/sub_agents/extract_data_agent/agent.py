"""
Responsible to receive the inputs and files, and validate that they
are correct inputs. The agent must reject if no valid input is received.
The model used at this agent must be able to process inputs like PDF,
text and others. If everything is OK, it passes to the next agent.
"""

from google.adk.agents import Agent

from agent_traveler.libs.constants import EXTRACT_DATA_AGENT_MODEL

from .prompt import prompt
from .types import DataExtracted

extract_data_agent = Agent(
    model=EXTRACT_DATA_AGENT_MODEL,
    name="extract_data_agent",
    description="Extract travel information from files",
    instruction=prompt,
    output_key="extracted_data",
    output_schema=DataExtracted,
)
