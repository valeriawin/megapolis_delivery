from fastapi import APIRouter, Request
from geojson_pydantic import Feature

from services.request_data_service import prepare_request_data

router = APIRouter()

man_cache = {}


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

    for man_id in man_cache:
        if man_id == new_man_id:
            return man_cache[man_id]

    man_cache[new_man_id] = request_data

    man_cache[new_man_id]["properties"]["zone"] = "non-zone"
    man_cache[new_man_id]["properties"]["deliveries"] = []

    return man_cache[new_man_id]
