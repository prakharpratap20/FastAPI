from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band

app = FastAPI()


BANDS = [
    {"id": 1, "name": "The Beatles", "genre": "Rock", "albums": [
        {"title": "Please Please Me", "release_date": "1963-03-22"},
        {"title": "With the Beatles", "release_date": "1963-11-22"},
    ]},
    {"id": 2, "name": "Led Zeppelin", "genre": "Electronic"},
    {"id": 3, "name": "The Rolling Stones", "genre": "Rock", "albums": [
        {"title": "Sticky Fingers", "release_date": "1971-04-23"},
        {"title": "Exile on Main St.", "release_date": "1972-05-12"},
    ]},
    {"id": 4, "name": "The Who", "genre": "Hip Hop"},
    {"id": 5, "name": "Pink Floyd", "genre": "Shoegaze", "albums": [
        {"title": "The Dark Side of the Moon", "release_date": "1973-03-01"},
        {"title": "Wish You Were Here", "release_date": "1975-09-12"},
    ]},
    {"id": 6, "name": "The Doors", "genre": "Rock", "albums": [
        {"title": "The Doors", "release_date": "1967-01-04"},
        {"title": "Strange Days", "release_date": "1967-09-25"},
    ]},
    {"id": 7, "name": "Queen", "genre": "Rock", "albums": [
        {"title": "A Night at the Opera", "release_date": "1975-11-21"},
        {"title": "A Day at", "release_date": "1976-12-10"},
    ]},
    {"id": 8, "name": "The Velvet Underground", "genre": "Metal"},
]


@app.get("/bands")
async def bands() -> list[Band]:
    return [Band(**b) for b in BANDS]


@app.get("/bands/{band_id}")
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        # status_code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands/genre/{genre}")
async def bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    band = [band for band in BANDS if band["genre"].lower() == genre.value]
    return band
