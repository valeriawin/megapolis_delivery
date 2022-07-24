from fastapi import APIRouter, Request
from geojson_pydantic import Feature

from services.request_data_service import prepare_request_data
from services.zone_identification import zone_cache

router = APIRouter()


@router.post("/add_zone", response_model=Feature)
async def add_zone(request: Request) -> Feature:
    """ Args:
            request: body should contain a geojson feature information as JSON
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
    request_data = await prepare_request_data(request)

    new_zone_name = request_data["properties"]["zone_name"]

    for zone_name in zone_cache:
        if zone_name == new_zone_name:
            return zone_cache[zone_name]

    zone_cache[new_zone_name] = request_data

    return zone_cache[new_zone_name]
