from typing import Optional
from pydantic import BaseModel, Field


class POI(BaseModel):
    """A Point Of Interest suggested by the agent."""

    place: str = Field(description="Name of the attraction")
    address: str = Field(
        description="An address or sufficient information to geocode for a Lat/Lon"
    )
    lat: str = Field(
        description="Numerical representation of Latitude of the location (e.g., 20.6843)"
    )
    long: str = Field(
        description="Numerical representation of Longitude of the location (e.g., -88.5678)"
    )
    rating: str = Field(
        description="Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc)"
    )
    highlights: str = Field(description="Short description highlighting key features")
    image_url: str = Field(description="verified URL to an image of the destination")
    map_url: Optional[str] = Field(description="Verified URL to Google Map")
    place_id: Optional[str] = Field(description="Google Map place_id")


class POISuggestions(BaseModel):
    """Points of interest recommendation."""

    places: list[POI] = Field(description="""Points of interest recommendation.""")


class Destination(BaseModel):
    """A destination description the traveler will visit."""

    name: str = Field(description="A Destination's Name")
    country: str = Field(description="The Destination's Country Name")
    image: str = Field(description="verified URL to an image of the destination")
    brief: str = Field(
        description="A brief of the destination, about the place and/or history. Make it look interesting and informatitve"
    )
    highlights: str = Field(description="Short description highlighting key features")
    rating: str = Field(description="Numerical rating (e.g., 4.5)")
    # places: POISuggestions = Field(
    #     description="A list of points of interest to visit at the place. No more tham 5 places"
    # )


class DestinationList(BaseModel):
    """List of destionation the traveler will visit."""

    destination_data: list[Destination] = Field(
        description="""List of destionation the traveler will visit."""
    )


class WhatToPackList(BaseModel):
    """List of things to pack for the trip."""

    what_to_pack: list[str] = Field(description="List of things to pack for the trip.")


class PoblemList(BaseModel):
    """List of problems or points of attetion."""

    problem_data: list[str] = Field(
        description="""List of problems or points of attetion."""
    )
