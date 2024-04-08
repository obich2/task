import math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = [float(i) for i in a]
    b_lon, b_lat = [float(i) for i in b]
    print(a_lon - b_lon, a_lat - b_lat)
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    d = math.sqrt(dx * dx + dy * dy)

    return d
