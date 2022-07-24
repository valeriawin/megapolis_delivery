from fastapi import APIRouter, Request
from geojson_pydantic import Feature

router = APIRouter()

man_cache = {}


@router.post("/add_deliveryman", response_model=Feature)
async def add_deliveryman(request: Request) -> Feature:
    request_data = await request.json()

    name = request_data["properties"]["name"]
    surname = request_data["properties"]["surname"]
    new_man_id = f"{name} {surname}"

    for man_id in man_cache:
        if man_id == new_man_id:
            return man_cache[man_id]

    man_cache[new_man_id] = request_data

    man_cache[new_man_id]["properties"]["zone"] = "non-zone"
    man_cache[new_man_id]["properties"]["deliveries"] = []

    return man_cache[new_man_id]
