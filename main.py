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


def cli():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(
        description="Zeige alle dm Fillialen mit Kodak Filmen in der Nähe der angegebenen Addresse.")
    parser.add_argument("--address", required=True, help='dein Wohnort')
    parser.add_argument("--radius", help="Radius in km um den Wohnort indem gesucht wird. Standard: 40km")
    parser.add_argument("--filmtypes", nargs="+",
                        help="Nach welchen Filmtypen soll gesucht werden. Optionen: GOLD, COLORPLUS, ULTRAMAX. Standard: alle")
    args = parser.parse_args()
    address = args.address
    radius = 40
    filmtypes = ["GOLD", "COLORPLUS", "ULTRAMAX"]
    if args.radius:
        radius = args.radius
    if args.filmtypes:
        # sanitize input
        for type in args.filmtypes:
            if type not in filmtypes:
                exit(2)
            filmtypes = args.filmtypes
    return address, radius, filmtypes


if __name__ == '__main__':
    address, radius, filmtypes = cli()

    # stores = load_stores_from_file("german_stores.json")
    # print_distance_stores_with_product(args.Address, stores, KODAK_GOLD)
    # print_distance_stores_with_product(address, stores, KODAK_COLORPLUS)
    # print_distance_stores_with_product(address, stores, KODAK_ULTRAMAX)
    # stores_in30km_with_stocks = filter_stores_for_distance(populate_stores_with_all_stocks(stores), 40)
    # print(prepare_update_message(stores_in30km_with_stocks))
