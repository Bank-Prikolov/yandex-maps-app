import math
from geopy.distance import geodesic


def pixel_in_degrees(coord1, z):
    px_alongX = 360 / (2 ** (z + 8))
    px_alongY = math.cos(math.radians(coord1)) * 360 / (2 ** (z + 8))
    return px_alongX, px_alongY


def ab_distance(a, b):
    a, b = tuple(a), tuple(b)
    distance = geodesic(a, b).meters
    return distance
