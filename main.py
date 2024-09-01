from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import GenreURLChoices, BandCreate, Band, Album
from typing import Annotated
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from db import init_db, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# lifespan is a context manager that will be called when the app starts and stops
app = FastAPI(lifespan=lifespan)


# BANDS = [
#     {"id": 1, "name": "The Beatles", "genre": "Rock", "albums": [
#         {"title": "Please Please Me", "release_date": "1963-03-22"},
#         {"title": "With the Beatles", "release_date": "1963-11-22"},
#     ]},
#     {"id": 2, "name": "Led Zeppelin", "genre": "Electronic"},
#     {"id": 3, "name": "The Rolling Stones", "genre": "Rock", "albums": [
#         {"title": "Sticky Fingers", "release_date": "1971-04-23"},
#         {"title": "Exile on Main St.", "release_date": "1972-05-12"},
#     ]},
#     {"id": 4, "name": "The Who", "genre": "Hiphop"},
#     {"id": 5, "name": "Pink Floyd", "genre": "Shoegaze", "albums": [
#         {"title": "The Dark Side of the Moon", "release_date": "1973-03-01"},
#         {"title": "Wish You Were Here", "release_date": "1975-09-12"},
#     ]},
#     {"id": 6, "name": "The Doors", "genre": "Rock"},
#     {"id": 7, "name": "Queen", "genre": "Rock", "albums": [
#         {"title": "A Night at the Opera", "release_date": "1975-11-21"},
#         {"title": "A Day at", "release_date": "1976-12-10"},
#     ]},
#     {"id": 8, "name": "The Velvet Underground", "genre": "Metal"},
# ]


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]

    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get("/bands/{band_id}")
async def band(
    band_id: Annotated[int, Path(title="The band ID")],
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        # status_code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band


# @app.get("/bands/genre/{genre}")
# async def bands_by_genre(genre: GenreURLChoices) -> list[dict]:
#     band = [b for b in BANDS if b["genre"].lower() == genre.value]
#     return band


@app.post("/bands")
async def create_band(
        band_data: BandCreate,
        session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band
            )
            session.add(album_obj)

    session.commit()
    session.refresh(band)
    return band
