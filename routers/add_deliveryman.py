"""
Requested deliveryman gets a zone according to coordinates.
Adds a new deliveryman to cache. Then returns to the user.

Functions:
    deliver(request_data: Feature)

Variables:
    router
    delivery_cache

"""

from fastapi import APIRouter
from geojson_pydantic import Feature

from services.zone_identification import identify_zone
from services.assign_deliveryman import man_cache

router = APIRouter()


@router.post("/add_deliveryman", response_model=Feature)
async def add_deliveryman(request_data: Feature) -> Feature:
    """ Args:
            request_data: should contain a geojson feature information as JSON
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [13.38272, 52.46385]
                        },
                        "properties": {
                            "uuid": "2c1bd651-6b36-4a4d-99bb-064afb130dbc"
                        }
                    }

        Returns:
            Delivery man Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """
    man_uuid = request_data.properties["uuid"]
    if man_info := man_cache.get(man_uuid):
        return man_info

    man_cache[man_uuid] = request_data

    coordinates = request_data.geometry.coordinates
    man_cache[man_uuid].properties["zone"] = identify_zone(*coordinates)

    man_cache[man_uuid].properties["deliveries"] = []

    return man_cache[man_uuid]
