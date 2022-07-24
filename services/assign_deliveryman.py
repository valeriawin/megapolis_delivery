"""
Assign deliveryman to a new order.

Functions:
    assign_deliveryman(zone, order_id)

Variables:
    man_cache

"""

man_cache = {}


def assign_deliveryman(zone_uuid: str, order_uuid: str) -> str:
    """ Args:
            zone_uuid: Delivery zone of an order uuid
            order_uuid: Delivery order uuid

        Returns:
            Deliveryman ID or "not-assigned" if no deliverymen in zone

    """
    filtered_men = list(
        filter(
            lambda man: (man.properties["zone_uuid"] == zone_uuid),
            man_cache.values()
        )
    )

    if len(filtered_men) > 0:
        deliveryman = sorted(
            filtered_men,
            key=lambda man: len(man.properties["deliveries"])
        )[0]

        man_uuid = deliveryman.properties["uuid"]
        man_cache[man_uuid].properties["deliveries"].append(order_uuid)

        return man_uuid

    return "not-assigned"
