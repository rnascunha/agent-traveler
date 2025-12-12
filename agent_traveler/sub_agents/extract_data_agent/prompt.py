from agent_traveler.libs.dump_data import dump_data
from .types import Flight, Hotel, CarRent, Place, Traveler

prompt = """
You are a agent responsible to extract travel information from text and files. 

Your objective is to extract meaningful information from the data you received.
Try your best to get all the information, even if is incomplete. If the information is missing, put a empty string ("").
The ouput format MUST be JSON format. The information to get are described below.

Travelers information. Name of the travelers and general information about them:
{{
  travelers: [
    {{
{travelers}
    }}
  ]
}}

Flights information. Fligths date and time, airport name and address:
{{
  flights: [
    {{
{flights}
    }}
  ]
}}

Hotels information. Hotels/Airbnb bookings dates, local address, check-in and check-out times, and the place information:
{{
  hotels: [
    {{
{hotels}
    }}
  ]
}}

Car rent infomation. Car rents, with date and time, location to pick-up and drop-out. 
{{
  car_rents: [
    {{
{car_rents}
    }}
  ]
}}

After extracting all the necessary information, deliver a structure response in JSON format.
""".format(
    travelers=dump_data(Traveler, indent=4),
    flights=dump_data(Flight, indent=4),
    hotels=dump_data(Hotel, indent=4),
    car_rents=dump_data(CarRent, indent=4),
)
