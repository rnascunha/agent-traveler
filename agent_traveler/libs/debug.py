from google.adk.events import Event
from rich.console import Console


def print_event(event: Event, *, show_deltas: bool = True):
    console = Console()

    console.rule(f"[bold green]{event.author}")
    console.print(f"\tIs final: {event.is_final_response()}")
    console.print(f"\ttimestamp: {event.timestamp}")
    console.print(f"\tid: {event.id}")
    console.print(f"\tinvocation_id: {event.invocation_id}")
    if event.branch:
        console.print(f"\tbranch: {event.branch}")
    if event.partial:
        console.print(f"\tpartial: {event.partial}")
    if event.error_code:
        console.print(f"\terror_code: {event.error_code}", style="red bold")
    if event.error_message:
        console.print(f"\terror_message: {event.error_message}", style="red bold")

    if event.actions:
        if show_deltas and event.actions.state_delta:
            console.print(f"\t[b]State changes[/b]: {event.actions.state_delta}")
        if show_deltas and event.actions.artifact_delta:
            console.print(f"\t[b]Artifact saved[/b]: {event.actions.artifact_delta}")
        if event.actions.transfer_to_agent:
            console.print(
                f"[b]Signal[/b]: [i]Transfer to {event.actions.transfer_to_agent}[/i]"
            )
        if event.actions.escalate:
            console.print("\t[b]Signal[/b]: [i]Escalate (terminate loop)[/i]")
        if event.actions.skip_summarization:
            console.print("\t[b]Signal[/b]: [i]Skip summarization for tool result[/i]")

    calls = event.get_function_calls()
    if calls:
        for call in calls:
            tool_name = call.name
            arguments = call.args
            console.rule(
                f"\t[bold magenta]Tool call '[i]{tool_name}[/i]'",
                align="left",
                style="magenta",
            )
            console.print(f"\t{arguments}")

    responses = event.get_function_responses()
    if responses:
        for response in responses:
            tool_name = response.name
            result_dict = response.response
            console.rule(
                f"\t[bold blue]Tool response '[i]{tool_name}[/i]'",
                align="left",
                style="blue",
            )
            console.print(f"\t{result_dict}")

    console.rule(f"[bold green]END {event.author}")
