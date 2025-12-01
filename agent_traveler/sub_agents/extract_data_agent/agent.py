from google.adk.agents import Agent
from agent_traveler.libs.types import json_response_config

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
    generate_content_config=json_response_config,
)
