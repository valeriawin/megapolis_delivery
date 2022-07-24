from fastapi import APIRouter, Request
from geojson_pydantic import Feature

from services.request_data_service import prepare_request_data

router = APIRouter()

zone_cache = {}


@router.post("/add_zone", response_model=Feature)
async def add_zone(request: Request) -> Feature:
    request_data = await prepare_request_data(request)

    new_zone_name = request_data["properties"]["zone_name"]

    for zone_name in zone_cache:
        if zone_name == new_zone_name:
            return zone_cache[zone_name]

    zone_cache[new_zone_name] = request_data

    return zone_cache[new_zone_name]
