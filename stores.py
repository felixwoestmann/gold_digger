import json
from stocklevels import KODAK_GOLD, KODAK_ULTRAMAX, KODAK_COLORPLUS


class Store:
    id = None
    countryCode = None
    storeNumber = None
    address = None
    latitude = None
    longitude = None
    stocklevel_gold = None
    stocklevel_colorplus = None
    stocklevel_ultramax = None

    def __init__(self, id, countrycode, storenumber, address, latitude, longitude):
        self.id = id
        self.countryCode = countrycode
        self.storeNumber = storenumber
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def get_stocklevel(self, product_number):
        switcher = {
            KODAK_GOLD: self.stocklevel_gold,
            KODAK_COLORPLUS: self.stocklevel_colorplus,
            KODAK_ULTRAMAX: self.stocklevel_ultramax
        }
        return switcher.get(product_number, "Not found")

    def add_stocklevel(self, new_stocklevel):
        if new_stocklevel.product_number == KODAK_GOLD:
            self.stocklevel_gold = new_stocklevel
        elif new_stocklevel.product_number == KODAK_COLORPLUS:
            self.stocklevel_colorplus = new_stocklevel
        elif new_stocklevel.product_number == KODAK_ULTRAMAX:
            self.stocklevel_ultramax = new_stocklevel


class StoreEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Store):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)


def fetch_store_coordinates(edge_one, edge_two):
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',
                     f"https://store-data-service.services.dmtech.com/stores/bbox/{edge_one},{edge_two}")
    return r.data


def fetch_german_stores():
    import json
    iceland = "64.7967375,-23.7289286"
    turkey = "39.0014506,30.6868348"
    store_data_json = json.loads(fetch_store_coordinates(iceland, turkey))
    # store_data_json keys(['totalElements', 'totalPages', 'size', 'page', 'stores'])
    german_stores = [tmp_store for tmp_store in store_data_json.get("stores") if tmp_store.get("countryCode") == "DE"]
    print(f"Fetched {store_data_json.get('totalElements')} stores total")
    german_stores_list = []
    for store in german_stores:
        s = Store(store.get("id"), store.get("countryCode"), store.get("storeNumber"), store.get("address"),
                  store.get("location").get("lat"), store.get("location").get("lon"))
        german_stores_list.append(s)
    print(f"Fetched {len(german_stores_list)} german stores")
    return german_stores_list


def save_stores_as_file(stores, filename):
    import json
    stores_json = json.dumps(stores, cls=StoreEncoder)
    f = open(filename, "w")
    f.write(stores_json)


def load_stores_from_file(filename):
    f = open(filename, "r")
    german_stores_list = []
    for store in json.load(f):
        s = Store(store.get("id"), store.get("countryCode"), store.get("storeNumber"), store.get("address"),
                  store.get("latitude"), store.get("longitude"))
        german_stores_list.append(s)
    return german_stores_list


def fetch_and_save_stores(): save_stores_as_file(fetch_german_stores(), "german_stores.json")

