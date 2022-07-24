"""
Requested order gets a zone according to coordinates and a deliveryman.
Adds a new order to cache. Then returns to the user.

Functions:
    deliver(request_data: Feature)

Variables:
    router
    delivery_cache

"""

from fastapi import APIRouter
from geojson_pydantic import Feature

from services.zone_identification import identify_zone
from services.assign_deliveryman import assign_deliveryman

router = APIRouter()

delivery_cache = {}


@router.post("/deliver", response_model=Feature)
async def deliver(request_data: Feature) -> Feature:
    """ Args:
            request_data: should contain a geojson feature information as JSON
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [13.38272, 52.46385]
                        },
                        "properties": {
                            "uuid": "66ce9b2b-1a71-4209-8e86-0fa2e457d4f1"
                        }
                    }

        Returns:
            Delivery zone Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """
    order_uuid = request_data.properties["uuid"]
    if delivery_info := delivery_cache.get(order_uuid):
        return delivery_info

    delivery_cache[order_uuid] = request_data

    coordinates = delivery_cache[order_uuid].geometry.coordinates
    zone_uuid = identify_zone(*coordinates)
    delivery_cache[order_uuid].properties["zone_uuid"] = zone_uuid

    delivery_cache[order_uuid].properties["deliveryman"] = assign_deliveryman(
        zone_uuid,
        order_uuid
    )

    return delivery_cache[order_uuid]
