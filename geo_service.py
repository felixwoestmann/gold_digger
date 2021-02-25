address_coordinate_cache = {}


def calculate_distance_address_store(address, store):
    address_latitude, address_longitude = get_coordinates_for_address(address)
    return calculate_distance_between_coordinates(address_latitude, address_longitude, store.latitude, store.longitude)


def calculate_distance_between_coordinates(latitude1, longitude1, latitude2, longitude2):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(latitude1))
    lon1 = radians(float(longitude1))
    lat2 = radians(float(latitude2))
    lon2 = radians(float(longitude2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def get_coordinates_for_address(address):
    import json
    import urllib3
    http = urllib3.PoolManager()
    # Cache the coordinates

    if address not in address_coordinate_cache:
        r = http.request('GET',
                         f"https://nominatim.openstreetmap.org/search/{address}?format=json")
        location_data = json.loads(r.data)
        address_coordinate_cache[address] = (location_data[0]["lat"], location_data[0]["lon"])
    return address_coordinate_cache[address]
