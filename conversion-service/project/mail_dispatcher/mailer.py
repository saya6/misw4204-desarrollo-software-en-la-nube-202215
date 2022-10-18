import smtplib

class MailDispatcher:
    def __init__(self, receiver, title, body):
        self.sender = "no-reply@blazin-fast-converter"
        self.receiver = receiver
        self.title = title
        self.body = body
    
    def send_mail(self):
        email = f'''from: {self.sender}
        to: {self.receiver}
        subject: {self.title}

        {self.body}'''

        smtp = smtplib.SMTP(host='mail_server', port=25)
        smtp.sendmail(from_addr=self.sender, to_addrs=self.receiver, msg=email)
