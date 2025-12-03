"""
Agent Traveler root agent.
"""

from google.adk.agents import SequentialAgent

from .sub_agents.validate_input_agent.agent import validate_input_agent
from .sub_agents.extract_data_agent.agent import extract_data_agent
from .sub_agents.research_agent.agent import research_agent
from .sub_agents.output_agent.agent import output_agent

from .sub_agents.report_agent.agent import report_agent

from datetime import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that logs when the agent starts processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    state = callback_context.state
    timestamp = datetime.now()
    state["request_start_time"] = timestamp.timestamp()
    print(f">>> Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    return None


def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    state = callback_context.state
    timestamp = datetime.now()
    duration = None
    if "request_start_time" in state:
        duration = (
            timestamp - datetime.fromtimestamp((state["request_start_time"]))
        ).total_seconds()

    if duration is not None:
        print(f">>> Duration: {duration:.2f} seconds")

    return None


root_agent = SequentialAgent(
    name="agent_traveler",
    description="A pipeline travel agent responsible to call the sub-agents sequentially",
    sub_agents=[
        validate_input_agent,
        extract_data_agent,
        research_agent,
        report_agent,
        output_agent,
    ],
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
