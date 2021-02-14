from stores import *
from stocklevels import *

MYLATITUDE = 53.16029
MYLONGITUDE = 8.2178513


def calculate_distance_between_coordinates(latitude1, longitude1, latitude2, longitude2):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


if __name__ == '__main__':
    stores = load_stores_from_file("german_stores.json")
    stores_with_stocklevel=get_kodak_stock_for_stores(KODAK_GOLD, stores)
    [str(store.storeNumber) for store in stores_chunk]
    # tuple = (stocklevel, calculate_distance_between_coordinates(MYLATITUDE, MYLONGITUDE, stocklevel.store.latitude,stocklevel.store.longitude))
    # stocklevels_distances.append(tuple)
    # sorted_by_second = sorted(stocklevels_distances, key=lambda tup: tup[1])
    # print(f"Distanz: {tup[1]} Store in {tup[0].store.address} besitzt {tup[0].stocklevel}")
