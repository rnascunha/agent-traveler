from agent_traveler.libs.functions import dump_data
from .types import Destination

destination_prompt = """
You are a agent specialized in research about trips and places.

Here is the information about the travelers trip:
<trip_data>
{extracted_data}
</trip_data>

For each city/destination you find at </trip_data>, make a reasearch about it. You must output a JSON data with the folloing information:
{{
    destination_data: [
        {{
{destination_schema}
        }},
    ]
}}

Use the agent tool `google_search_grounding` if necessary. Call this tool at most one (1) time per destination.
""".format(
    extracted_data="extracted_data", destination_schema=dump_data(Destination, indent=6)
)
# After the of your research, call the `map_tool` tool that will get the precise latitute and longitude of the places.

what_to_pack_prompt = """
Given a trip origin, a destination, and some rough idea of activities, suggests a handful of items to pack appropriate for the trip.

Trip data:
<trip_data>
{extracted_data}
</trip_data>

Return in JSON format, a list of items to pack, e.g.
{{
  what_to_pack: [ "walking shoes", "fleece", "umbrella" ]
}}

Use the agent tool `google_search_grounding` if necessary. Call this tool at most one  (1) time per destination.
"""

verifify_problem_prompt = """
You are a agent responsible to verify possible problems or points of attetion to the trip.

Trip data:
<trip_data>
{extracted_data}
</trip_data>

Possible problems that you can check:
- Gaps at booking. Dates at the trip without any booking;
- Overlaps at booking/flyghts. Check if a person has more than one booking or flight at the same day/time;
- Possible holidays. Most holidays places are close. Travelers must be notified about it if any holidays happen when they are there;
- Missing flights between far away city;
- Points of attention. Some examples:
    - If a traveler is a driver, and is a international trip, he/she must have a international driver license;
    - Some countries requires specific vaccines for specific contries. Based on the orign of the trip, you my now from what country travelers are. Provide links if possible;
    - Some countries requires visa for specific contries. Based on the orign of the trip, you my now from what country travelers are. Provide links if possible;

Use the `google_search_grounding` as you necessary to chek any of this information.

Return a JSON format as descriped bellow:
{{
  problem_data: ["Holidays at day 25/12 at Poland", "Driver Aline must check if have internatinal driver license", "From day 01/10 to 03/10 there is now booking registered" , ...]
}}
"""
