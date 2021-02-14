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

def chunks_of_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_kodak_stock_for_stores(product_number, stores):
    import json
    import urllib3
    http = urllib3.PoolManager()
    for stores_chunk in chunks_of_list(stores,10):
        converted_list = [str(element.store_number) for element in stores_chunk]
        url_stores=",".join(converted_list)
        r = http.request('GET',
                     f"https://products.dm.de/store-availability/DE/products/dans/{product_number}/stocklevel?storeNumbers={url_stores}")
    stocklevel_data_json = json.loads(r.data)
    for store_data in stocklevel_data_json.get("storeAvailability"):
        stocklevel = stocklevel_data_json[0].get("stockLevel")
        Stocklevel(product_number, store, stocklevel)
    return stocklevel


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    myLatitude=53.16029
    myLongitude=8.2178513
    """ Load all DM Stores in Germany and save them as a file """
    # german_stores=fetch_german_dm_stores()
    # save_dm_stores_as_file(german_stores,"german_stores.json")
    """Load DM Stores from file"""
    stocklevels = []
    stores = load_dm_stores_from_file("german_stores.json")
    for store in stores:
        gold_stocklevel = get_kodak_gold_stock_for_store(store)
        #colorplus_stocklevel = get_kodak_colorplus_stock_for_store(store)
        #ultramax_stocklevel = get_kodak_ultramax_stock_for_store(store)
        if gold_stocklevel.stocklevel > 0: stocklevels.append(gold_stocklevel)
        #if colorplus_stocklevel.stocklevel > 0: stocklevels.append(colorplus_stocklevel)
        #if ultramax_stocklevel.stocklevel > 0: stocklevels.append(ultramax_stocklevel)
    stocklevels_distances=[]
    for stocklevel in stocklevels:
        print(f"Store: {stocklevel.store.storeNumber} in {stocklevel.store.address} besitzt {stocklevel.stocklevel} Packungen Kodak Gold 200")
        tuple=(stocklevel,calculate_distance_between_coordinates(myLatitude,myLongitude,stocklevel.store.latitude,stocklevel.store.longitude))
        stocklevels_distances.append(tuple)
    sorted_by_second = sorted(stocklevels_distances,key=lambda tup: tup[1])
    for tup in stocklevels_distances:
        print(f"Distanz: {tup[1]} Store in {tup[0].store.address} besitzt {tup[0].stocklevel}")