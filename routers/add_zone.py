"""
Adds a new zone to cache. Then returns to the user.

Functions:
    deliver(request_data: Feature)

Variables:
    router
    delivery_cache

"""

from fastapi import APIRouter
from geojson_pydantic import Feature

from services.zone_identification import zone_cache

router = APIRouter()


@router.post("/add_zone", response_model=Feature)
async def add_zone(request_data: Feature) -> Feature:
    """ Args:
            request_data: should contain a geojson feature information as JSON
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [13.38272, 52.46385],
                                    [13.42786, 52.46385],
                                    [13.42786, 52.48445],
                                    [13.38272, 52.48445],
                                    [13.38272, 52.46385]
                                ]
                            ]
                        },
                        "properties": {
                            "uuid": "a551cce6-b79d-4385-be27-d4d822b1e301"
                        }
                    }

        Returns:
            Delivery zone Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """
    zone_uuid = request_data.properties["uuid"]
    if zone_info := zone_cache.get(zone_uuid):
        return zone_info

    zone_cache[zone_uuid] = request_data

    return zone_cache[zone_uuid]
