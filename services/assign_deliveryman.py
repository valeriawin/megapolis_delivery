man_cache = {}


def assign_deliveryman(zone):
    """ Args:
            zone: Delivery zone of an order

        Returns:
            Deliveryman ID or "not-assigned" if no deliverymen in zone

    """
    filtered_men = list(
        filter(
            lambda man: (man["properties"]["zone"] == zone),
            man_cache.values()
        )
    )

    if len(filtered_men) > 0:
        deliveryman = sorted(
            filtered_men,
            key=lambda man: len(man["properties"]["deliveries"])
        )[0]

        name = deliveryman["properties"]["name"]
        surname = deliveryman["properties"]["surname"]
        deliveryman_id = f"{name} {surname}"

        return deliveryman_id

    return "not-assigned"
