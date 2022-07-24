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
                            "zone_name": "south east"
                        }
                    }

        Returns:
            Delivery zone Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """

    new_zone_name = request_data.properties["zone_name"]

    for zone_name, zone_info in zone_cache.items():
        if zone_name == new_zone_name:
            return zone_info

    zone_cache[new_zone_name] = request_data

    return zone_cache[new_zone_name]
