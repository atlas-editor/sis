from email.utils import formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
import json

port, smtp_server, login, password, sender_email, sender_name = json.load(open('.env')).values()

def send_email(message, address, subject='(no subject)'):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
    text = MIMEText(message, 'plain')
    msg.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(login, password)
        if type(address) == list:
            for receiver in address:
                server.sendmail(msg['From'], receiver, msg.as_string())
        else:
            server.sendmail(msg['From'], address, msg.as_string())