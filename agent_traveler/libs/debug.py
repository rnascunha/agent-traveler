from google.adk.events import Event
from pprint import pprint


def print_event(event: Event, *, show_deltas: bool = True):
    pprint(
        {
            "timestamp": event.timestamp,
            "author": event.author,
            "partial": event.partial,
            "id": event.id,
            "invocation_id": event.invocation_id,
            "error_code": event.error_code,
            "error_message": event.error_message,
            "branch": event.branch,
        }
    )

    if event.actions:
        if show_deltas and event.actions.state_delta:
            print(f"State changes: {event.actions.state_delta}")
        if show_deltas and event.actions.artifact_delta:
            print(f"Artifact saved: {event.actions.artifact_delta}")
        if event.actions.transfer_to_agent:
            print(f"  Signal: Transfer to {event.actions.transfer_to_agent}")
        if event.actions.escalate:
            print("  Signal: Escalate (terminate loop)")
        if event.actions.skip_summarization:
            print("  Signal: Skip summarization for tool result")

    calls = event.get_function_calls()
    if calls:
        for call in calls:
            tool_name = call.name
            arguments = call.args  # This is usually a dictionary
            print(f"  Tool: {tool_name}, Args: {arguments}")

    responses = event.get_function_responses()
    if responses:
        for response in responses:
            tool_name = response.name
            result_dict = response.response  # The dictionary returned by the tool
            print(f"  Tool Result: {tool_name} -> {result_dict}")
