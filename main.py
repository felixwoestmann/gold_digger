from stores import *
from stocklevels import *
from geo_service import *
import argparse


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


def filter_stores_for_distance(address, stores, radius):
    tuples = []
    for store in stores:
        tuples.append((
            store,
            calculate_distance_address_store(address, store)))
    sorted_by_distance = sorted(tuples, key=lambda tuple: tuple[1])
    return [tup[0] for tup in sorted_by_distance if tup[1] <= radius]


def print_stores_sorted_by_distance(address, stores, product_number):
    tuples = []
    for store in stores:
        tuples.append((
            store,
            calculate_distance_address_store(address, store)))
    for tuple in sorted(tuples, key=lambda tuple: tuple[1]):
        print(
            f"Entfernung: {tuple[1]:.1f} km Stadt: {tuple[0].address['city']} Bestand: {tuple[0].get_stocklevel(product_number).stocklevel} Packungen {name_for_product_number.get(product_number, 'Not Found')}")


def cli_argparser():
    parser = argparse.ArgumentParser(
        description="Zeige alle dm Filialen mit einem Bestand an Kodak Filmen in der Nähe der angegebenen Addresse")
    parser.add_argument("--address", required=True, help="Adresse in deren Umkreis gesucht wird")
    parser.add_argument("--radius", type=float, help="Radius in km um die Adresse. default: 40km")
    parser.add_argument("--filmtypes", nargs="+",
                        help="Filmtypen nach denen gesucht wird. Optionen: GOLD, COLORPLUS, ULTRAMAX. dafault: alle")
    args = parser.parse_args()
    # init vars with default values
    radius = 40
    filmtypes = ["GOLD", "COLORPLUS", "ULTRAMAX"]
    if args.radius:
        radius = args.radius
    if args.filmtypes:
        # sanitize input
        for type in args.filmtypes:
            if type not in filmtypes:
                print(f"Can't recognize {type}")
                exit(2)
            filmtypes = args.filmtypes
    return args.address, radius, filmtypes


if __name__ == '__main__':
    address, radius, filmtypes = cli_argparser()
    stores = load_stores_from_file("german_stores.json")
    filtered_stores_distance = filter_stores_for_distance(address, stores, radius)
    print(
        f"Suche in {len(filtered_stores_distance)} dm Filialen in {radius} km Radius um {address} nach {','.join(filmtypes)} gesucht")
    if "GOLD" in filmtypes:
        print("Kodak Gold ist verfügbar in folgenden Filialen:")
        stores_with_stock = get_kodak_stock_for_stores(KODAK_GOLD, filtered_stores_distance)
        print_stores_sorted_by_distance(address, stores_with_stock, KODAK_GOLD)
        print("\n")
    if "COLORPLUS" in filmtypes:
        print("Kodak Colorplus ist verfügbar in folgenden Filialen:")
        stores_with_stock = get_kodak_stock_for_stores(KODAK_COLORPLUS, filtered_stores_distance)
        print_stores_sorted_by_distance(address, stores_with_stock, KODAK_COLORPLUS)
        print("\n")
    if "ULTRAMAX" in filmtypes:
        print("Kodak Ultramax ist verfügbar in folgenden Filialen:")
        stores_with_stock = get_kodak_stock_for_stores(KODAK_ULTRAMAX, filtered_stores_distance)
        print_stores_sorted_by_distance(address, stores_with_stock, KODAK_ULTRAMAX)
        print("\n")
    # print_distance_stores_with_product(args.Address, stores, KODAK_GOLD)
    # print_distance_stores_with_product(address, stores, KODAK_COLORPLUS)
    # print_distance_stores_with_product(address, stores, KODAK_ULTRAMAX)
    # stores_in30km_with_stocks = filter_stores_for_distance(populate_stores_with_all_stocks(stores), 40)
    # print(prepare_update_message(stores_in30km_with_stocks))
