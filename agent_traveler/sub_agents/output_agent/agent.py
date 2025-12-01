from google.adk.agents import Agent, ParallelAgent

from ..report_agent.agent import report_agent

# from agent_traveler.tools.artifact import save_calendar_tool
# from .prompt import calendar_prompt

from agent_traveler.tools.calendar import create_calendar_callback

# calendar_agent = Agent(
#     name="calendar_agent",
#     description="Creates a caledar file output",
#     model="gemini-2.0-flash",
#     instruction=calendar_prompt,
#     tools=[save_calendar_tool],
# )


output_agent = ParallelAgent(
    name="output_agent",
    description="Call sub agents that will create the diferent outputs",
    # sub_agents=[report_agent, calendar_agent],
    sub_agents=[report_agent],
    after_agent_callback=create_calendar_callback,
)
