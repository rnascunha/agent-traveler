from agent_traveler.libs.functions import dump_data
from .types import Flight, Hotel, CarRent, Place, Traveler

prompt = """
You are a agent responsible to extract travel information from text and files. 

Information data:
<trip_info>
{file_data}
</trip_info>

Your objective is to extract meaningful information from the data </trip_info> you received.

Try your best to get all the information, even if is incomplete. If the information is missing, put a empty string ("").

The ouput format is JSON. The information to get are described below.

Travelers information:
{{
  travelers: [
    {{
{travelers}
    }}
  ]
}}

Flights information:
{{
  flights: [
    {{
{flights}
    }}
  ]
}}

Hotels information:
{{
  hotels: [
    {{
{hotels}
    }}
  ]
}}

Car rent infomation:
{{
  car_rents: [
    {{
{car_rents}
    }}
  ]
}}

Places information. Some places (like hotels, airports, car rent company) was already described above. It doesn't matter, put it again here:
{{
  places: [
    {{
{places}
    }}
  ]
}}

- Name of the travelers and general information about them;
- Places the travelers will visit, and days it will be there;
- Fligths date and time, airport name and address;
- Hotels/Airbnb bookings dates, local address, check-in and check-out times, and the place information;
- Car rents, with date and time, location to pick-up and drop-out. 
- Visit packages with name, dates and location.

After extracting all the necessary information, deliver a structure response in JSON format.
""".format(
    travelers=dump_data(Traveler, indent=4),
    flights=dump_data(Flight, indent=4),
    hotels=dump_data(Hotel, indent=4),
    car_rents=dump_data(CarRent, indent=4),
    places=dump_data(Place, indent=4),
    file_data="file_data?"
)


prompt2 = """
You are a agent responsible to extract travel information from text and files. 

Information data:
<trip_info>
{file_data?}
</trip_info>

Your objective is to extract meaningful information from the data </trip_info> you received.
The information you must extract is:
- Name of the travelers and general information about them;
- Places the travelers will visit, and days it will be there;
- Fligths date and time, airport name and address;
- Hotels/Airbnb bookings dates, local address, check-in and check-out times, and the place information;
- Car rents, with date and time, location to pick-up and drop-out. 
- Visit packages with name, dates and location.

After extracting all the necessary information, deliver a structure response in JSON format.
"""
