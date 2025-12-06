from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

default_values = {
    "target_tz": "America/Sao_Paulo",
    "checkin_time": "14:00",
    "checkout_time": "11:00",
    "pickup_time": "10:00",
    "dropoff_time": "10:00",
    "prodid": "-//Senor Mondo//Calendar//EN",
}

format_flight_string = "%d/%m/%Y %H:%M"
format_car_rental_string = "%d/%m/%Y %H:%M"
format_hotel_string = "%d/%m/%Y %H:%M"


def create_flight_event(flight):
    check_flight_data = all(
        flight.get(f)
        for f in ["departure_date", "departure_time", "arrival_date", "arrival_time"]
    )
    if not check_flight_data:
        print(flight)
        return None

    try:
        event = Event()
        event.add(
            "summary", f"Flight {flight['flight_number']} ({flight['company_name']})"
        )

        description = "\n".join(
            [
                f"Booking Reference: {flight.get('booking_reference', "")}",
                f"Departure Airport: {flight.get('departure_airport', "")}",
                f"Arrival Airport: {flight.get('arrival_airport', "")}",
                f"Class: {flight.get('class_type', "")}",
                f"Baggage: {flight.get('baggage', "")}",
                f"Passengers: {', '.join(flight.get('travelers', []))}",
            ]
        )
        event.add("description", description)
        event.add("location", flight["departure_airport"])

        start_datetime = datetime.strptime(
            f"{flight['departure_date']} {flight['departure_time']}",
            format_flight_string,
        ).replace(
            tzinfo=ZoneInfo(
                flight.get("departure_timezone", default_values["target_tz"])
            )
        )
        event.add("dtstart", start_datetime)

        endt_datetime = datetime.strptime(
            f"{flight['arrival_date']} {flight['arrival_time']}", format_flight_string
        ).replace(
            tzinfo=ZoneInfo(flight.get("arrival_timezone", default_values["target_tz"]))
        )
        event.add("dtend", endt_datetime)

        # # Create event time
        event.add("dtstamp", datetime.now(ZoneInfo("UTC")))
        event.add("uid", f'flight-{start_datetime.strftime("%Y%m%d%H%M")}@example.com')

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add(
            "description",
            f"Flight {flight['flight_number']} ({flight['company_name']})",
        )
        alarm.add("trigger", timedelta(days=-3))

        alarm2 = Alarm()
        alarm2.add("action", "DISPLAY")
        alarm2.add(
            "description",
            f"Flight {flight['flight_number']} ({flight['company_name']})",
        )
        alarm2.add("trigger", timedelta(hours=-3))

        event.add_component(alarm)
        event.add_component(alarm2)

        return event
    except Exception as e:
        return None


def create_hotel_event(hotel):
    check_hotel_data = all(hotel.get(f) for f in ["checkin_date", "checkout_date"])
    if not check_hotel_data:
        return None

    try:
        event = Event()

        event.add("summary", f"Hotel: {hotel['name']}")
        description = "\n".join(
            [
                f"Address: {hotel.get('address', "")}",
                f"Room Type: {hotel.get('room_type', "")}",
                f"Board: {hotel.get('board', "")}",
                f"Guests: {', '.join(hotel.get('guests', []))}",
                f"Description: {hotel.get('description', '')}",
                f"Info: {hotel.get('info', '')}",
            ]
        )
        event.add("description", description)
        event.add("location", hotel["address"])

        timezone = ZoneInfo(
            hotel["timezone"] if hotel.get("timezone") else default_values["target_tz"]
        )
        checkin_time = (
            hotel["checkin_time"]
            if hotel["checkin_time"]
            else default_values["checkin_time"]
        )
        start_datetime = datetime.strptime(
            f"{hotel['checkin_date']} {checkin_time}",
            format_hotel_string,
        ).replace(tzinfo=timezone)
        event.add("dtstart", start_datetime)

        checkout_time = (
            hotel["checkout_time"]
            if hotel["checkout_time"]
            else default_values["checkout_time"]
        )
        end_datetime = datetime.strptime(
            f"{hotel['checkout_date']} {checkout_time}",
            format_hotel_string,
        ).replace(tzinfo=timezone)
        event.add("dtend", end_datetime)

        # Create event time
        event.add("dtstamp", datetime.now(ZoneInfo("UTC")))
        event.add("uid", f'hotel-{start_datetime.strftime("%Y%m%d%H%M")}@example.com')

        return event
    except Exception as e:
        return None


def create_car_rental_event(car_rental):
    check_car_rental_event = all(car_rental[f] for f in ["pickup_date", "dropoff_date"])
    if not check_car_rental_event:
        return None

    try:
        event = Event()

        event.add("summary", f"Car Rental: {car_rental['name']}")
        description = "\n".join(
            [
                f"Pickup Address: {car_rental.get('pickup_address','')}",
                f"Dropoff Address: {car_rental.get('dropoff_address','')}",
                f"Car Category: {car_rental.get('car_category','')}",
                f"Car Description: {car_rental.get('car_description','')}",
                f"Driver: {car_rental.get('driver','')}",
                f"Info: {car_rental.get('info','')}",
            ]
        )
        event.add("description", description)
        event.add("location", car_rental.get("pickup_address", ""))

        pickup_datetime = datetime.strptime(
            f"{car_rental['pickup_date']} {car_rental.get('pickup_time', default_values["pickup_time"])}",
            format_car_rental_string,
        ).replace(
            tzinfo=ZoneInfo(
                car_rental.get("pickup_timezone", default_values["target_tz"])
            )
        )
        event.add("dtstart", pickup_datetime)

        dropoff_datetime = datetime.strptime(
            f"{car_rental['dropoff_date']} {car_rental.get('dropoff_time', default_values["dropoff_time"])}",
            format_car_rental_string,
        ).replace(
            tzinfo=ZoneInfo(
                car_rental.get("dropoff_timezone", default_values["target_tz"])
            )
        )
        event.add("dtend", dropoff_datetime)

        # Create event time
        event.add("dtstamp", datetime.now(ZoneInfo("UTC")))
        event.add(
            "uid", f'car-rental-{pickup_datetime.strftime("%Y%m%d%H%M")}@example.com'
        )

        return event
    except Exception as e:
        return None


def create_calendar(trip_data: dict[str, any], prodid=""):
    cal = Calendar()

    cal.add("prodid", prodid if prodid else default_values["prodid"])
    cal.add("version", "2.0")

    for flight in trip_data["flights"]:
        event = create_flight_event(flight)
        if event:
            cal.add_component(event)

    for hotel in trip_data["hotels"]:
        event = create_hotel_event(hotel)
        cal.add_component(event)

    for car_rental in trip_data["car_rents"]:
        event = create_car_rental_event(car_rental)
        cal.add_component(event)

    return cal
