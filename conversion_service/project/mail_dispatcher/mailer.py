import smtplib
from urllib import request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
class MailDispatcher:
    def __init__(self, receiver, title, body):
        self.sender = "s.ayat@uniandes.edu.co"
        self.receiver = receiver
        self.title = title
        self.body = body
    
    def send_mail(self):
        if os.environ.get('BFAC_ENV') == "dev":
            self._send_api_mail()
            return
        pass
        

    def _send_api_mail(self):
        message = Mail(
            from_email=self.sender,
            to_emails=self.receiver,
            subject=self.title,
            html_content='<strong>{}</strong>'.format(self.body)
        )
        print("-> Intentando enviar correo: {}\n".format(message))
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)