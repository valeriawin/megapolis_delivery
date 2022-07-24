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
                            "order": "iPhone 13 256gb"
                        }
                    }

        Returns:
            Delivery zone Feature

        Raises:
            HTTPException 400: If nothing passed
            HTTPException 422: If invalid parameters passed

    """

    for delivery_info in delivery_cache.values():
        if delivery_info == request_data:
            return delivery_info

    order_id = len(delivery_cache)
    delivery_cache[order_id] = request_data

    coordinates = delivery_cache[order_id].geometry.coordinates
    zone = identify_zone(*coordinates)
    delivery_cache[order_id].properties["zone"] = zone

    delivery_cache[order_id].properties["deliveryman"] = assign_deliveryman(
        delivery_cache[order_id].properties["zone"],
        order_id
    )

    return delivery_cache[order_id]
