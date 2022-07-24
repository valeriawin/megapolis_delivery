from fastapi import APIRouter, Request
from geojson_pydantic import Feature

from services.request_data_service import prepare_request_data

router = APIRouter()

delivery_cache = {}


@router.post("/deliver", response_model=Feature)
async def add_zone(request: Request) -> Feature:
    request_data = await prepare_request_data(request)

    for delivery_info in delivery_cache.values():
        if delivery_info == request_data:
            return delivery_info

    order_id = len(delivery_cache)
    delivery_cache[order_id] = request_data

    delivery_cache[order_id]["properties"]["zone"] = "non-zone"

    delivery_cache[order_id]["properties"]["deliveryman"] = "not-assigned"

    return delivery_cache[order_id]
