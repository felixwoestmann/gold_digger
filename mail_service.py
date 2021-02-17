import sendgrid
import os
from sendgrid.helpers.mail import *


def send_mail(to_mail, from_mail, subject, message):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_mail)
    to_email = To(to_mail)
    content = Content(message)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())



