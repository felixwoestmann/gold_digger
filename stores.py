import json


class DmStore:
    id = None
    countryCode = None
    storeNumber = None
    address = None
    latitude = None
    longitude = None

    def __init__(self, id, countrycode, storenumber, address, latitude, longitude):
        self.id = id
        self.countryCode = countrycode
        self.storeNumber = storenumber
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class DmStoreEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, DmStore):
            return object.__dict__
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)


def fetch_dm_stores_coordinates(edgeone, edgetwo):
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',
                     f"https://store-data-service.services.dmtech.com/stores/bbox/{edgeone},{edgetwo}")
    return r.data


def fetch_german_dm_stores():
    import json
    iceland = "64.7967375,-23.7289286"
    turkey = "39.0014506,30.6868348"
    store_data_json = json.loads(fetch_dm_stores_coordinates(iceland, turkey))
    # store_data_json keys(['totalElements', 'totalPages', 'size', 'page', 'stores'])
    german_stores = [tmp_store for tmp_store in store_data_json.get("stores") if tmp_store.get("countryCode") == "DE"]
    print(f"Fetched {store_data_json.get('totalElements')} stores total")
    german_stores_list = []
    for store in german_stores:
        s = DmStore(store.get("id"), store.get("countryCode"), store.get("storeNumber"), store.get("address"),
                    store.get("location").get("lat"), store.get("location").get("lon"))
        german_stores_list.append(s)
    print(f"Fetched {len(german_stores_list)} german stores")
    return german_stores_list


def save_dm_stores_as_file(stores, filename):
    import json
    stores_json = json.dumps(stores, cls=DmStoreEncoder)
    f = open(filename, "w")
    f.write(stores_json)
