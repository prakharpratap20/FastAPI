from datetime import date
from enum import Enum
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship


class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip hop"
    SHOEGAZE = "shoegaze"
    METAL = "metal"


class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hiphop"
    SHOEGAZE = "Shoegaze"
    METAL = "Metal"


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
