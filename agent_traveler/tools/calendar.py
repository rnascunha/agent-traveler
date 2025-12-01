import datetime
import pytz
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext
from google.genai import types

from .artifact import save_calendar_tool


def create_ics_file(trip_data):
    """Creates an ICS file from the trip data."""

    calendar = (
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Company//Your Product//EN\n"
    )

    timezone = pytz.timezone("UTC")

    # Flights
    for flight in trip_data["flights"]:
        start_datetime_str = f"{flight['departure_date']} {flight['departure_time']}"
        start_datetime_obj = datetime.datetime.strptime(
            start_datetime_str, "%d/%m/%Y %H:%M"
        )
        start_datetime_utc = timezone.localize(start_datetime_obj).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        end_datetime_str = f"{flight['arrival_date']} {flight['arrival_time']}"
        end_datetime_obj = datetime.datetime.strptime(
            end_datetime_str, "%d/%m/%Y %H:%M"
        )
        end_datetime_utc = timezone.localize(end_datetime_obj).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        summary = f"Flight {flight['flight_number']} ({flight['company_name']})"
        description = (
            f"Booking Reference: {flight['booking_reference']}\\n"
            f"Departure Airport: {flight['departure_airport']}\\n"
            f"Arrival Airport: {flight['arrival_airport']}\\n"
            f"Class: {flight['class_type']}\\n"
            f"Baggage: {flight['baggage']}\\n"
            f"Travelers: {', '.join(flight['travelers'])}"
        )
        location = flight["departure_airport"]

        calendar += f"BEGIN:VEVENT\n"
        calendar += f"DTSTART:{start_datetime_utc}\n"
        calendar += f"DTEND:{end_datetime_utc}\n"
        calendar += f"SUMMARY:{summary}\n"
        calendar += f"DESCRIPTION:{description}\n"
        calendar += f"LOCATION:{location}\n"
        calendar += f"END:VEVENT\n"

    # Hotels
    for hotel in trip_data["hotels"]:
        start_date_str = hotel["checkin_date"]
        start_datetime_obj = datetime.datetime.strptime(start_date_str, "%d/%m/%Y")
        start_datetime_utc = timezone.localize(start_datetime_obj).strftime(
            "%Y%m%dT000000Z"
        )

        end_date_str = hotel["checkout_date"]
        end_datetime_obj = datetime.datetime.strptime(end_date_str, "%d/%m/%Y")
        end_datetime_utc = timezone.localize(end_datetime_obj).strftime(
            "%Y%m%dT000000Z"
        )

        summary = f"Hotel: {hotel['name']}"
        description = (
            f"Address: {hotel['address']}\\n"
            f"Room Type: {hotel['room_type']}\\n"
            f"Board: {hotel['board']}\\n"
            f"Guests: {', '.join(hotel['guests'])} \\n"
            f"Description: {hotel['description']} \\n"
            f"Info: {hotel['info']}"
        )
        location = hotel["address"]

        calendar += f"BEGIN:VEVENT\n"
        calendar += f"DTSTART:{start_datetime_utc}\n"
        calendar += f"DTEND:{end_datetime_utc}\n"
        calendar += f"SUMMARY:{summary}\n"
        calendar += f"DESCRIPTION:{description}\n"
        calendar += f"LOCATION:{location}\n"
        calendar += f"END:VEVENT\n"

    # Car Rentals
    for car_rental in trip_data["car_rents"]:
        pickup_datetime_str = f"{car_rental['pickup_date']} {car_rental['pickup_time']}"
        pickup_datetime_obj = datetime.datetime.strptime(
            pickup_datetime_str, "%d/%m/%Y %H:%M"
        )
        pickup_datetime_utc = timezone.localize(pickup_datetime_obj).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        dropoff_datetime_str = (
            f"{car_rental['dropoff_date']} {car_rental['dropoff_time']}"
        )
        dropoff_datetime_obj = datetime.datetime.strptime(
            dropoff_datetime_str, "%d/%m/%Y %H:%M"
        )
        dropoff_datetime_utc = timezone.localize(dropoff_datetime_obj).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        summary = f"Car Rental: {car_rental['name']}"
        description = (
            f"Pickup Address: {car_rental['pickup_address']}\\n"
            f"Dropoff Address: {car_rental['dropoff_address']}\\n"
            f"Car Category: {car_rental['car_category']}\\n"
            f"Car Description: {car_rental['car_description']}\\n"
            f"Driver: {car_rental['driver']}\\n"
            f"Info: {car_rental['info']}"
        )
        location = car_rental["pickup_address"]

        calendar += f"BEGIN:VEVENT\n"
        calendar += f"DTSTART:{pickup_datetime_utc}\n"
        calendar += f"DTEND:{dropoff_datetime_utc}\n"
        calendar += f"SUMMARY:{summary}\n"
        calendar += f"DESCRIPTION:{description}\n"
        calendar += f"LOCATION:{location}\n"
        calendar += f"END:VEVENT\n"

    calendar += "END:VCALENDAR"
    return calendar


async def create_calendar_tool(
    tool_context: ToolContext,
):
    """
    Create a calendar ICS file and saves it as a artifact for the user

    Args:
        tool_context: The ADK tool context.
    """

    calendar = create_ics_file(tool_context.state.get("extracted_data", dict()))
    await save_calendar_tool(calendar, tool_context)
