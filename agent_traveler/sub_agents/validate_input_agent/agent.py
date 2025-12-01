from google.adk.agents import Agent

from agent_traveler.libs.constants import VALIDATE_INPUT_AGENT_MODEL
from .prompt import prompt

validate_input_agent = Agent(
    name="validate_input_agent",
    model=VALIDATE_INPUT_AGENT_MODEL,
    description="Reponsable to accept and validate the user input",
    instruction=prompt,
    output_key="file_data",
)
