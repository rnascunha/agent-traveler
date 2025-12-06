"""
Responsible to make all research based on the inputs of the user
"""

from google.adk.agents import Agent, ParallelAgent
from google.adk.tools import AgentTool


from agent_traveler.libs.constants import (
    DESTIONATION_AGENT_MODEL,
    WHAT_TO_PACK_MODEL,
    VERIFY_PROBLEM_AGENT_MODEL,
)

from agent_traveler.tools.search import google_search_grounding
from agent_traveler.tools.places import research_destination_callback

from .prompt import (
    what_to_pack_prompt,
    destination_prompt,
    verifify_problem_prompt,
    destination_tool_prompt,
)
from .types import DestinationList, WhatToPackList, ProblemList, Destination


# Agent tool to research about destination
destination_tool_agent = Agent(
    name="destination_tool_agent",
    description="Research about a destination",
    model=DESTIONATION_AGENT_MODEL,
    output_schema=Destination,
    instruction=destination_tool_prompt,
    tools=[google_search_grounding],
)

# Check all inputs and research about destinations
destination_agent = Agent(
    name="destination_agent",
    description="Research agent to get information about trips and places.",
    model=DESTIONATION_AGENT_MODEL,
    output_key="destination_data",
    output_schema=DestinationList,
    instruction=destination_prompt,
    tools=[AgentTool(destination_tool_agent)],
    after_agent_callback=research_destination_callback,
)

# based on the places and activities, gives advice about what to pack for the trip
what_to_pack_agent = Agent(
    model=WHAT_TO_PACK_MODEL,
    name="what_to_pack_agent",
    description="Make suggestion on what to bring for the trip",
    instruction=what_to_pack_prompt,
    output_key="what_to_pack_data",
    output_schema=WhatToPackList,
    tools=[google_search_grounding],
)

# verify problems and/or points of attention
verifify_problem_agent = Agent(
    name="verifify_problem_agent",
    description="Check about possible problems at the trip",
    model=VERIFY_PROBLEM_AGENT_MODEL,
    output_key="problem_data",
    output_schema=ProblemList,
    instruction=verifify_problem_prompt,
    tools=[google_search_grounding],
)

# Call all research agents in parallel
research_agent = ParallelAgent(
    name="research_agent",
    description="Responsible to make all necessary research about the trip",
    sub_agents=[destination_agent, what_to_pack_agent, verifify_problem_agent],
)
