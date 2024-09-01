from datetime import date
from enum import Enum
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship


class GenreURLChoices(Enum):
    """
    Enum for genre choices in the URL path parameter for the /bands endpoint.
    """
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip hop"
    SHOEGAZE = "shoegaze"
    METAL = "metal"


class GenreChoices(Enum):
    """
    Enum for genre choices in the Band model.
    """
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hiphop"
    SHOEGAZE = "Shoegaze"
    METAL = "Metal"


class AlbumBase(SQLModel):
    """
    Pydantic model for the Album model.
    """
    title: str
    release_date: date
    band_id: int | None = Field(foreign_key="band.id")


class Album(AlbumBase, table=True):
    """
    SQLModel for the Album model.
    """
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    """
    Pydantic model for the Band model with a validator for the genre field.
    """
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    """
    Pydantic model for creating a Band instance with an optional list of AlbumBase instances.
    """
    albums: list[AlbumBase] | None = None

    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()


class Band(BandBase, table=True):
    """
    SQLModel for the Band model with a relationship to the Album model.
    """
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
