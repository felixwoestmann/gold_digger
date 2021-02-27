import sendgrid
import os
from sendgrid.helpers.mail import *
from stocklevels import *
from geo_service import *


def send_mail(to_mail, from_mail, subject, message):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_mail)
    to_email = To(to_mail)
    content = Content(message)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())


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
