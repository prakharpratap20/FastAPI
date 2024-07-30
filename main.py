from fastapi import FastAPI
from fastapi.exceptions import HTTPException


app = FastAPI()

BANDS = [
    {"id": 1, "name": "The Beatles", "genre": "Rock"},
    {"id": 2, "name": "Led Zeppelin", "genre": "Electronic"},
    {"id": 3, "name": "The Rolling Stones", "genre": "Rock"},
    {"id": 4, "name": "The Who", "genre": "Hip Hop"},
    {"id": 5, "name": "Pink Floyd", "genre": "Shoegaze"},
]


@app.get("/bands")
async def bands() -> list:
    return BANDS


@app.get("/bands/{band_id}", status_code=206)
async def band(band_id: int) -> dict:
    band = next((band for band in BANDS if band["id"] == band_id), None)
    if band is None:
        # status_code=404
        raise HTTPException(status_code=404, detail="Band not found")
    return band
