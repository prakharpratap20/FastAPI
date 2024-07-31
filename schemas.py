from datetime import date
from enum import Enum
from pydantic import BaseModel, validator


class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hiphop"
    SHOEGAZE = "shoegaze"
    METAL = "metal"


class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hiphop"
    SHOEGAZE = "Shoegaze"
    METAL = "Metal"


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []


class BandCreate(BandBase):
    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()


class BandWithID(BandBase):
    id: int
