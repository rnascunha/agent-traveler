"""
Tools to save the artifacts created.
"""

from google.adk.tools import ToolContext
import google.genai.types as types
import json


async def save_artifact_string(
    data: str, filename: str, mime_type: str, tool_context: ToolContext
):
    bytes = data.encode("utf-8")

    try:
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=types.Part.from_bytes(data=bytes, mime_type=mime_type),
        )
        message = (
            f"Successfully saved Python artifact '{filename}' as version {version}."
        )
        print(message)
        return {"status": "success", "version": version, "message": message}

    except ValueError as e:
        message = f"Error saving Python artifact: {e}. Is ArtifactService configured in Runner?"
        print(message)
        return {"status": "error", "message": message}
    except Exception as e:
        message = f"An unexpected error occurred during Python artifact save: {e}"
        print(message)
        return {"status": "error", "message": message}


async def save_report_tool(report: str, tool_context: ToolContext):
    """Save report to the persistent storage

    Arg:
        report: report to be saved
        tool_context: The ADK tool context.

    Returns:
        The status of the operation
    """
    return await save_artifact_string(
        report, "report.md", "text/markdown", tool_context
    )


async def save_calendar_tool(calendar: str, tool_context: ToolContext):
    """Save calendar to the persistent storage

    Arg:
        calendar: calendar to be saved
        tool_context: The ADK tool context.

    Returns:
        The status of the operation
    """
    return await save_artifact_string(
        calendar, "calendar.ics", "text/calendar", tool_context
    )


async def save_kml_tool(kml: str, tool_context: ToolContext):
    """Save KML map file to the persistent storage

    Arg:
        kml: KML map definition
        tool_context: The ADK tool context.

    Returns:
        The status of the operation
    """
    return await save_artifact_string(
        kml, "map.kml", "application/vnd.google-earth.kml+xml", tool_context
    )


async def save_state_tool(tool_context: ToolContext):
    """Save agents state

    Arg:
        tool_context: The ADK tool context.

    Returns:
        The status of the operation
    """
    state_json = json.dumps(tool_context.state.to_dict())
    return await save_artifact_string(
        state_json, "state.json", "application/json", tool_context
    )
