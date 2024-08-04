import math
from geopy.distance import geodesic


def degrees_to_pixels(coord1, z):
    coordX = 360 / (2 ** (z + 8))
    coordY = math.cos(math.radians(coord1)) * 360 / (2 ** (z + 8))
    return coordX, coordY


def ab_distance(a, b):
    a, b = tuple(a), tuple(b)
    distance = geodesic(a, b).meters
    return distance
