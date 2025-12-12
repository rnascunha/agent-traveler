import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

from google.adk.runners import Runner
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.artifacts import FileArtifactService
from google.genai import types

from agent_traveler.agent import root_agent
from agent_traveler.libs.debug import print_event

load_dotenv()

APP_NAME = "agent-traveler"
USER_ID = "rafaelo"
SESSION = "default"


async def run_session(
    runner: Runner,
    user_queries: list[types.Part] | types.Part = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    app_name = runner.app_name
    session_service = runner.session_service
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except Exception as e:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    if user_queries:
        if type(user_queries) == str:
            user_queries = [user_queries]

        query = types.Content(role="user", parts=user_queries)

        async for event in runner.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("     Is FINAL RESPONSE")
                # text = event.content.parts[0].text
                # if text and text != "None":
                #     print(f"Model: > {text}")
            else:
                print("is NOT FINAL RESPONSE")

            print_event(event, show_deltas=False)

    else:
        print("No queries")


session_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

home_dir = os.path.expanduser("~")

db_url = f"sqlite+aiosqlite:////{home_dir}/Downloads/{session_name}.db"
session_service = DatabaseSessionService(db_url=db_url)
artifact_service = FileArtifactService(f"{home_dir}/Downloads")

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    artifact_service=artifact_service,
)

print(" Statefull agent initialized!")
print(f"    - Applcation: {APP_NAME}")
print(f"    - User: {USER_ID}")
print(f"    - Session: {session_service.__class__.__name__}")


def create_content_parts():
    files_path = [
        "./data/Confirmacao de reserva_RafaNessa.pdf",
        "./data/inter_Nessa.pdf",
        "./data/inter_Rafa.pdf",
        "./data/Nacional_Nessa.pdf",
        "./data/Nacional_Rafa.pdf",
    ]

    files_parts = [
        types.Part(
            text="Create a report based on the attached files. Rafael likes museums, Vanessa likes of good restaurants."
        )
    ]
    for file in files_path:
        with open(file, "rb") as f:
            raw = f.read()
        part = types.Part(inline_data=types.Blob(data=raw, mime_type="application/pdf"))
        files_parts.append(part)

    return files_parts


asyncio.run(
    run_session(
        runner,
        create_content_parts(),
        session_name,
    )
)
