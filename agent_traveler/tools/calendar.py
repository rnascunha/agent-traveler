"""
Tool to create the ICS calendar file.
"""

from google.adk.tools import ToolContext
from .artifact import save_calendar_tool
from agent_traveler.libs.calendar import create_calendar

import logging


async def create_calendar_tool(
    tool_context: ToolContext,
):
    """
    Create a calendar ICS file and saves it as a artifact for the user

    Args:
        tool_context: The ADK tool context.
    """
    logging.debug("Entering 'create_calendar_tool'")
    try:
        calendar = create_calendar(tool_context.state.get("extracted_data", dict()))
        await save_calendar_tool(calendar.to_ical(), tool_context)
    except Exception as e:
        logging.error(f"Calender error: {e}")

    logging.debug("Exiting 'create_calendar_tool'")
