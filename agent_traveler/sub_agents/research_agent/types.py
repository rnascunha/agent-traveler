# from typing import Optional, List
from pydantic import BaseModel, Field


# class POI(BaseModel):
#     """A Point Of Interest suggested by the agent."""

#     place: str = Field(description="Name of the attraction")
#     address: str = Field(
#         description="An address or sufficient information to geocode for a Lat/Lon"
#     )
#     lat: str = Field(
#         description="Numerical representation of Latitude of the location (e.g., 20.6843)"
#     )
#     long: str = Field(
#         description="Numerical representation of Longitude of the location (e.g., -88.5678)"
#     )
#     rating: str = Field(
#         description="Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc)"
#     )
#     highlights: str = Field(description="Short description highlighting key features")
#     image_url: str = Field(description="verified URL to an image of the destination")
#     map_url: Optional[str] = Field(description="Verified URL to Google Map")
#     place_id: Optional[str] = Field(description="Google Map place_id")


# class POISuggestions(BaseModel):
#     """Points of interest recommendation."""

#     places: list[POI] = Field(description="""Points of interest recommendation.""")


class Destination(BaseModel):
    """A destination description the traveler will visit."""

    name: str = Field(description="A Destination's Name", default="")
    country: str = Field(description="The Destination's Country Name", default="")
    # image: str = Field(
    #     description="verified URL to an image of the destination", default=""
    # )
    brief: str = Field(
        description="A brief of the destination, about the place and/or history. Make it look interesting and informatitve",
        default="",
    )
    highlights: list[str] = Field(
        description="A list of places and attractions to visit. Just show the name of the places. No explanation needed",
        default=[],
    )
    rating: str = Field(description="Numerical rating (e.g., 4.5)", default="")


class DestinationList(BaseModel):
    """List of destionation the traveler will visit."""

    destination_data: list[Destination] = Field(
        description="List of destionation the traveler will visit.", default=""
    )


class WhatToPackList(BaseModel):
    """List of things to pack for the trip."""

    what_to_pack_data: list[str] = Field(
        description="List of things to pack for the trip.", default=[]
    )


class ProblemList(BaseModel):
    """List of problems or points of attetion."""

    problem_data: list[str] = Field(
        description="List of problems or points of attetion.", default=[]
    )
