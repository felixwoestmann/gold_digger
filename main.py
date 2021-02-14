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

def print_distance_stores_with_gold(stores):
    stores_with_stocklevel = get_kodak_stock_for_stores(KODAK_GOLD, stores)
    stores_with_gold = [store for store in stores_with_stocklevel if store.stocklevel_gold.stocklevel > 0]
    tuples = []
    for store_with_gold in stores_with_gold:
        tuples.append((
            store_with_gold,
            calculate_distance_between_coordinates(MYLATITUDE,
                                                   MYLONGITUDE,
                                                   store_with_gold.latitude,
                                                   store_with_gold.longitude)))
    sorted_by_second = sorted(tuples, key=lambda tuple: tuple[1])
    for tuple in sorted_by_second:
        print(
            f"Entfernung: {tuple[1]:.1f} km Stadt: {tuple[0].address['city']} Bestand: {tuple[0].stocklevel_gold.stocklevel} Packungen Gold")


if __name__ == '__main__':
    stores = load_stores_from_file("german_stores.json")
    print_distance_stores_with_gold(stores)