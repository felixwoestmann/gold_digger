from stores import *
from stocklevels import *
from geo_service import *


def print_distance_stores_with_product(address, stores, product_number):
    stores_with_stocklevel = get_kodak_stock_for_stores(product_number, stores)
    stores_with_product = [store for store in stores_with_stocklevel if
                           store.get_stocklevel(product_number).stocklevel > 0]
    tuples = []
    for store_with_product in stores_with_product:
        tuples.append((
            store_with_product,
            calculate_distance_address_store(address, store_with_product)))
    sorted_by_second = sorted(tuples, key=lambda tuple: tuple[1])
    for tuple in sorted_by_second:
        print(
            f"Entfernung: {tuple[1]:.1f} km Stadt: {tuple[0].address['city']} Bestand: {tuple[0].get_stocklevel(product_number).stocklevel} Packungen {name_for_product_number.get(product_number, 'Not Found')}")


def prepare_update_message(address, stores):
    stores_with_gold = [store for store in stores if store.get_stocklevel(KODAK_GOLD).stocklevel > 0]
    stores_with_colorplus = [store for store in stores if store.get_stocklevel(KODAK_COLORPLUS).stocklevel > 0]
    stores_with_utramax = [store for store in stores if store.get_stocklevel(KODAK_ULTRAMAX).stocklevel > 0]
    string_list = ["In folgenden Stores sind in deiner Nähe wieder Kodak Filme verfügbar!"]
    if stores_with_gold:
        string_list.append("")
        string_list.append("Kodak Gold 3er")
        for store in stores_with_gold:
            string_list.append(
                f"Entfernung: {calculate_distance_address_store(address, store) :.1f} km "
                f"Stadt: {store.address['city']} Bestand: {store.get_stocklevel(KODAK_GOLD).stocklevel} "
                f"Packungen {name_for_product_number.get(KODAK_GOLD, 'Not Found')}")

    if stores_with_colorplus:
        string_list.append("")
        string_list.append("Kodak Colorplus")
        for store in stores_with_colorplus:
            string_list.append(
                f"Entfernung: {calculate_distance_address_store(address, store) :.1f} km "
                f"Stadt: {store.address['city']} Bestand: {store.get_stocklevel(KODAK_COLORPLUS).stocklevel} "
                f"Packungen {name_for_product_number.get(KODAK_COLORPLUS, 'Not Found')}")

    if stores_with_utramax:
        string_list.append("")
        string_list.append("Kodak Ultramax")
        for store in stores_with_utramax:
            string_list.append(
                f"Entfernung: {calculate_distance_address_store(address, store) :.1f} km "
                f"Stadt: {store.address['city']} Bestand: {store.get_stocklevel(KODAK_ULTRAMAX).stocklevel} "
                f"Packungen {name_for_product_number.get(KODAK_ULTRAMAX, 'Not Found')}")
    return "\n".join(string_list)


def populate_stores_with_all_stocks(stores):
    stores_with_gold = get_kodak_stock_for_stores(KODAK_GOLD, stores)
    stores_with_colorplus = get_kodak_stock_for_stores(KODAK_COLORPLUS, stores_with_gold)
    stores_with_ultramax = get_kodak_stock_for_stores(KODAK_ULTRAMAX, stores_with_colorplus)
    return stores_with_ultramax


def filter_stores_for_distance(address, stores, radius):
    tuples = []
    for store in stores:
        tuples.append((
            store,
            calculate_distance_address_store(address, store)))
    sorted_by_distance = sorted(tuples, key=lambda tuple: tuple[1])
    return [tup[0] for tup in sorted_by_distance if tup[1] <= radius]


if __name__ == '__main__':
    stores = load_stores_from_file("german_stores.json")
    address = "Prinzipalmarkt, Münster"
    print_distance_stores_with_product(address, stores, KODAK_GOLD)
    #print_distance_stores_with_product(address, stores, KODAK_COLORPLUS)
    #print_distance_stores_with_product(address, stores, KODAK_ULTRAMAX)
    # stores_in30km_with_stocks = filter_stores_for_distance(populate_stores_with_all_stocks(stores), 40)
    # print(prepare_update_message(stores_in30km_with_stocks))
