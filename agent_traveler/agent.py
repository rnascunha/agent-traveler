"""
Agent Traveler root agent.
"""

from google.adk.agents import SequentialAgent
from datetime import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .sub_agents.validate_input_agent.agent import validate_input_agent
from .sub_agents.extract_data_agent.agent import extract_data_agent
from .sub_agents.research_agent.agent import research_agent

from .sub_agents.report_agent.agent import report_agent

from .tools.places import create_map_points
from .tools.calendar import create_calendar_tool
from .tools.artifact import save_report_tool

import asyncio

import logging


async def create_save_files(callback_context: CallbackContext):
    logging.debug("Entering 'create_save_files'")
    tasks = [
        create_map_points(callback_context),
        create_calendar_tool(callback_context),
    ]
    report = callback_context.state.get("report_data")
    if report:
        tasks.append(save_report_tool(report, callback_context))

    logging.info("Saving files [waiting]")
    await asyncio.gather(*tasks)

    logging.debug("Exiting 'create_save_files'")
    return None


root_agent = SequentialAgent(
    name="agent_traveler",
    description="A pipeline travel agent responsible to call the sub-agents sequentially",
    sub_agents=[
        validate_input_agent,
        extract_data_agent,
        research_agent,
        report_agent,
    ],
    after_agent_callback=create_save_files,
)
