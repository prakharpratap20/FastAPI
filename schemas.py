from datetime import date
from enum import Enum
from pydantic import BaseModel


class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hiphop"
    SHOEGAZE = "shoegaze"
    METAL = "metal"


class Albums(BaseModel):
    title: str
    release_date: date


class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Albums] = []
