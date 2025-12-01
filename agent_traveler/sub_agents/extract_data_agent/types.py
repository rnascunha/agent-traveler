from pydantic import BaseModel, Field


class Traveler(BaseModel):
    name: str = Field(description="Full name of the traveler")
    age: str = Field(description="Age of the traveler")
    passport: str = Field(description="Passport number")
    preferences: list[str] = Field(
        description="List of preferences or limitations of the traveler"
    )
    info: str = Field(description="Any general information about the traveler")


class Place(BaseModel):
    name: str = Field(
        description="Name of the place that the traveler will be. The name can be a place, city, airport, hotel, attraction, car rental company or others"
    )
    address: str = Field(
        description="Full address of the place, like zipcode, city, country"
    )
    type: str = Field(
        description="Type of the place the user will be. E.g. hotel, airport, car rental, night club or other"
    )
    place_id: str = Field(description="Place identication at Google Maps")
    map_url: str = Field(description="Map to access to place directly at Google Maps")
    lat: str = Field(description="Latitute of the place")
    long: str = Field(description="Longitute of the place")


class Hotel(BaseModel):
    name: str = Field(description="Hotel name")
    address: str = Field(
        description="Full address of the hotel, with zipcode, city, country (if provided)"
    )
    checkin_date: str = Field(description="Date of the check in, e.g. 23/10/2024")
    checkin_time: str = Field(
        description="Time of the check in, with timezone (if provided), e.g. 11:00 (+3:00)"
    )
    checkout_date: str = Field(description="Date of the check out, e.g. 23/10/2024")
    checkout_time: str = Field(
        description="Time of the check out, with timezone (if provided), e.g. 11:00 (+3:00)"
    )
    description: str = Field(description="Description of the hotel")
    guests: list[str] = Field(description="List with the name of the guests")
    room_type: str = Field(description="Type of the room, e.g. luxury")
    board: str = Field(description="Board type, e.g. half board, full board")
    info: str = Field(
        description="General information about the hotel, policy and room"
    )


class CarRent(BaseModel):
    name: str = Field(description="Car rental company name")
    pickup_address: str = Field(
        description="Full address of the car rental to pickup the car, with zipcode, city, country (if provided)"
    )
    pickup_date: str = Field(description="Date to pickup the car, e.g. 23/10/2023")
    pickup_time: str = Field(
        description="Time to pickup the car with timezone, e.g. 10:00 (-2:00)"
    )
    dropoff_address: str = Field(
        description="Full address of the car rental to dropoff the car, with zipcode, city, country (if provided)"
    )
    dropoff_date: str = Field(description="Date to pickup the car, e.g. 23/10/2023")
    dropoff_time: str = Field(
        description="Time to pickup the car with timezone, e.g. 10:00 (-2:00)"
    )
    car_category: str = Field(description="Category of the car")
    car_description: str = Field(
        description="Car description, like models, air conditioner..."
    )
    info: str = Field(
        description="General information about conditions, requirements..."
    )
    driver: str = Field(description="Driver name")


class Flight(BaseModel):
    company_name: str = Field(description="Airline name")
    booking_reference: str = Field(description="The booking reservation identification")
    flight_number: str = Field(description="Flight number identication")
    departure_airport: str = Field(
        description="Airport name and identication of the departure"
    )
    departure_date: str = Field(description="Date of the departure, e.g. 13/09/2023")
    departure_time: str = Field(
        description="Time of the departure with timezone, e.g. 06:05 (+5:00)"
    )
    arrival_airport: str = Field(
        description="Airport name and identication of the arrival"
    )
    arrival_date: str = Field(description="Date of the arrival, e.g. 13/09/2023")
    arrival_time: str = Field(
        description="Time of the arrival with timezone, e.g. 06:05 (+5:00)"
    )
    class_type: str = Field(description="Flight class")
    baggage: str = Field(description="Baggage type included at the ticket")
    travelers: list[str] = Field(description="List of travelers names")
    info: str = Field(description="General information about the flight")


class DataExtracted(BaseModel):
    travelers: list[Traveler] = Field(description="List of travelers with information")
    flights: list[Flight] = Field(description="List of flights with information")
    hotels: list[Hotel] = Field(description="List of hotels with informations")
    car_rents: list[CarRent] = Field(description="List of car rents")
    places: list[Place] = Field(description="List of places the traveler will visit")
