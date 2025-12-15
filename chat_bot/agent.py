from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from google.adk.planners.built_in_planner import BuiltInPlanner
from google.genai import types


root_agent = Agent(
    model="gemini-2.5-flash",
    name="chat_bot",
    description="You are a chat bot for general things",
    instruction="""You resposibility is give the most accurate possible anwser for the any of the user questions.
  Be polite. Use `google_search` tool as necessary. If you don't know the anwser or need more information, ask the user for clarification.""",
    tools=[google_search],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, thinking_budget=2048
        )
    ),
)
