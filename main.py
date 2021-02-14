class Store_dm:
    def __init__(self, id, countryCode, storeNumber, address, latitude, longitude):
        self.id = id
        self.countryCode = countryCode
        self.storeNumber = storeNumber
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class Stocklevel:
    def __init__(self, dan, store, stocklevel):
        self.dan = dan
        self.store = store
        self.stocklevel = stocklevel


def fetch_dm_stores_coordinates(edgeone, edgetwo):
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',
                     f"https://store-data-service.services.dmtech.com/stores/bbox/{edgeone},{edgetwo}")
    return r.data


def fetch_dm_stores():
    import json
    island = "64.7967375,-23.7289286"
    turkey = "39.0014506,30.6868348"
    muenster1 = "52.09474984342242,7.274791566610219"
    muenster2 = "51.81838113459128,7.969270163522964"
    # store_data=fetch_dm_stores(muenster1,muenster2)
    store_data_json = json.loads(fetch_dm_stores_coordinates(island, turkey))
    # store_data_json keys(['totalElements', 'totalPages', 'size', 'page', 'stores'])
    german_stores = [store for store in store_data_json.get("stores") if store.get("countryCode") == "DE"]
    print(store_data_json.get("totalElements"))
    german_stores_list = []
    for store in german_stores:
        s = Store_dm(store.get("id"), store.get("countryCode"), store.get("storeNumber"), store.get("address"),
                     store.get("location").get("lat"), store.get("location").get("lon"))
        german_stores_list.append(s)
    print(len(german_stores_list))
    return german_stores_list


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    german_dm_stores = fetch_dm_stores()
    for store in german_dm_stores:
        stocklevel = get_kodak_gold_stock_for_store(store)
        if stocklevel.stocklevel > 0:
            print(f"Store: {stocklevel.store.storeNumber} in {stocklevel.store.address} besitzt {stocklevel.stocklevel} Packungen Kodak Gold 200")
