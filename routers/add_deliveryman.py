from fastapi import APIRouter, Request
from geojson_pydantic import Feature

from services.request_data_service import prepare_request_data
from services.zone_identification import identify_zone
from services.assign_deliveryman import man_cache

router = APIRouter()


@router.post("/add_deliveryman", response_model=Feature)
async def add_deliveryman(request: Request) -> Feature:
    """ Args:
            request: body should contain a geojson feature information as JSON
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [13.38272, 52.46385]
                        },
                        "properties": {
                            "name": "jeff",
                            "surname": "smith"
                        }
                    }

        Returns:
            Delivery man Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """
    request_data = await prepare_request_data(request)

    name = request_data["properties"]["name"]
    surname = request_data["properties"]["surname"]
    new_man_id = f"{name} {surname}"

    for man_id, man_info in man_cache.items():
        if man_id == new_man_id:
            return man_info

    man_cache[new_man_id] = request_data

    coordinates = request_data["geometry"]["coordinates"]
    man_cache[new_man_id]["properties"]["zone"] = identify_zone(*coordinates)

    man_cache[new_man_id]["properties"]["deliveries"] = []

    return man_cache[new_man_id]
