from google.adk.agents import Agent, ParallelAgent

from agent_traveler.libs.types import json_response_config
from agent_traveler.libs.constants import (
    DESTIONATION_AGENT_MODEL,
    WHAT_TO_PACK_MODEL,
    VERIFY_PROBLEM_AGENT_MODEL,
)
from agent_traveler.tools.search import google_search_grounding

# from agent_traveler.tools.places import map_tool

from .prompt import what_to_pack_prompt, destination_prompt, verifify_problem_prompt

from .types import DestinationList, WhatToPackList, PoblemList

destination_agent = Agent(
    name="destination_agent",
    description="Research agent resposible the get information about trips and places.",
    model=DESTIONATION_AGENT_MODEL,
    output_key="destination_data",
    # output_schema=DestinationList,
    instruction=destination_prompt,
    generate_content_config=json_response_config,
    # tools=[google_search_grounding, map_tool],
    tools=[google_search_grounding],
)

what_to_pack_agent = Agent(
    model=WHAT_TO_PACK_MODEL,
    name="what_to_pack_agent",
    description="Make suggestion on what to bring for the trip",
    instruction=what_to_pack_prompt,
    output_key="what_to_pack",
    output_schema=WhatToPackList,
    generate_content_config=json_response_config,
    tools=[google_search_grounding],
)

verifify_problem_agent = Agent(
    name="verifify_problem_agent",
    description="Check about possible problems at the trip",
    model=VERIFY_PROBLEM_AGENT_MODEL,
    output_key="problem_data",
    output_schema=PoblemList,
    instruction=verifify_problem_prompt,
    generate_content_config=json_response_config,
    tools=[google_search_grounding],
)

research_agent = ParallelAgent(
    name="research_agent",
    description="Responsible to make all necessary research about the trip",
    sub_agents=[destination_agent, what_to_pack_agent, verifify_problem_agent],
)
