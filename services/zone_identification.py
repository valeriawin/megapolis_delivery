zone_cache = {}


def identify_zone(coord_x, coord_y):
    """ Args:
            coord_x - coordinate X of a Point
            coord_y - coordinate Y of a Point

        Returns:
            Delivery zone name or "non-zone" if zone is unidentified

    """
    for zone, zone_info in zone_cache.items():
        zone_coordinates = zone_info.geometry.coordinates[0]
        x_min = zone_coordinates[0][0]
        y_min = zone_coordinates[0][1]
        x_max = zone_coordinates[2][0]
        y_max = zone_coordinates[2][1]

        if x_min <= coord_x <= x_max and y_min <= coord_y <= y_max:
            return zone

    return "non-zone"
