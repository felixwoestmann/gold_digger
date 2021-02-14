from stores import *

class Stocklevel:
    def __init__(self, dan, store, stocklevel):
        self.dan = dan
        self.store = store
        self.stocklevel = stocklevel



def get_kodak_gold_stock_for_store(store):
    dans_kodak_gold = 405075
    stocklevel = get_kodak_stock_for_store(dans_kodak_gold, store.storeNumber)
    return Stocklevel(dans_kodak_gold, store, stocklevel)


def get_kodak_ultramax_stock_for_store(store):
    dans_kodak_ultramax = 276758
    stocklevel = get_kodak_stock_for_store(dans_kodak_ultramax, store.storeNumber)
    return Stocklevel(dans_kodak_ultramax, store, stocklevel)


def get_kodak_colorplus_stock_for_store(store):
    dans_kodak_colorplus = 724104
    stocklevel = get_kodak_stock_for_store(dans_kodak_colorplus, store.storeNumber)
    return Stocklevel(dans_kodak_colorplus, store, stocklevel)


def get_kodak_stock_for_store(product_number, store_number):
    import json
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',
                     f"https://products.dm.de/store-availability/DE/products/dans/{product_number}/stocklevel?storeNumbers={store_number}")
    stocklevel_data_json = json.loads(r.data)
    stocklevel = stocklevel_data_json.get("storeAvailability")[0].get("stockLevel")
    return stocklevel


def calculate_distance_between_coordinates(latitude1, longitude1, latitude2, longitude2):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    german_stores=fetch_german_dm_stores()
    save_dm_stores_as_file(german_stores,"german_stores.json")
#german_dm_stores = fetch_dm_stores()
# for store in german_dm_stores:
#     stocklevel = get_kodak_gold_stock_for_store(store)
#     if stocklevel.stocklevel > 0:
#         print(
#             f"Store: {stocklevel.store.storeNumber} in {stocklevel.store.address} besitzt {stocklevel.stocklevel} Packungen Kodak Gold 200")
