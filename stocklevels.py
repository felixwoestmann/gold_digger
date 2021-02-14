KODAK_GOLD = 405075
KODAK_ULTRAMAX = 276758
KODAK_COLORPLUS = 724104

name_for_product_number = {
    KODAK_GOLD: "Kodak Gold 3er",
    KODAK_COLORPLUS: "Kodak Colorplus",
    KODAK_ULTRAMAX: "Kodak Ultramax"
}


class Stocklevel:
    def __init__(self, product_number, stocklevel):
        self.product_number = product_number
        self.stocklevel = stocklevel


def get_kodak_stock_for_store(product_number, store_number):
    import json
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',
                     f"https://products.dm.de/store-availability/DE/products/dans/{product_number}/stocklevel"
                     f"?storeNumbers={store_number}")
    stocklevel_data_json = json.loads(r.data)
    return Stocklevel(product_number, stocklevel_data_json.get("storeAvailability")[0].get("stockLevel"))


def chunks_of_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_kodak_stock_for_stores(product_number, stores):
    import json
    import urllib3
    stores_to_return = []
    http = urllib3.PoolManager()
    for stores_chunk in chunks_of_list(stores, 40):
        converted_list = [str(store.storeNumber) for store in stores_chunk]
        url_stores = ",".join(converted_list)
        r = http.request('GET',
                         f"https://products.dm.de/store-availability/DE/products/dans/{product_number}/stocklevel"
                         f"?storeNumbers={url_stores}")
        stocklevel_data_json = json.loads(r.data)
        for item in stocklevel_data_json.get("storeAvailability"):
            store = next(store for store in stores if store.storeNumber == item.get("store").get("storeNumber"))
            store.add_stocklevel(Stocklevel(product_number, item.get("stockLevel")))
            stores_to_return.append(store)
    return stores_to_return
