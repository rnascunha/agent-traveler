from google.adk.agents.callback_context import CallbackContext
from agent_traveler.libs.extract_update_data import improve_extracted_data
from agent_traveler.libs.merge_destinatination_places import merge_data

import logging


async def extract_data_callback(callback_context: CallbackContext):
    """
    Get data extracted and improve it

    Args:
      callback_context: google ADK callback context

    Returns:
      None
    """
    logging.debug("Entering 'extract_data_callback'")
    extract_data = callback_context.state.get("extracted_data")
    data, places = await improve_extracted_data(extract_data)
    callback_context.state["extracted_data"] = data
    callback_context.state["places_data"] = places

    logging.debug("Exiting 'extract_data_callback'")
    return None


def merge_destination_place_callback(callback_context: CallbackContext):
    """
    Merge data from "places" to destinations/highlights to improve reports
    Args:
      callback_context: google ADK callback context

    Returns:
      None
    """
    logging.debug("Entering 'merge_destination_place_callback'")
    destinations = merge_data(callback_context.state)
    callback_context.state["destinations"] = destinations

    logging.debug("Exiting 'merge_destination_place_callback'")
    return None
