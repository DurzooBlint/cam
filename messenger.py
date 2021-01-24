import smtplib
import time
import datetime
import configparser


class Email:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

        # Load config from file
        self.load_config(self)
        config = configparser.ConfigParser()
        config.read("config.conf")
        self.SMTP_SERVER = config['DEFAULT']['SMTP_SERVER']
        self.SMTP_PORT = config['DEFAULT']['SMTP_PORT']
        self.GMAIL_USERNAME = config['DEFAULT']['GMAIL_USERNAME']
        self.GMAIL_PASSWORD = config['DEFAULT']['GMAIL_PASSWORD']

    def send_email(self):
        # Create Headers
        headers = ["From: " + self.GMAIL_USERNAME, "Subject: " + self.subject, "To: " + self.recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        # Connect to Gmail Server
        session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        # Login to Gmail
        session.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)

        # Send Email & Exit
        session.sendmail(self.GMAIL_USERNAME, self.recipient, headers + "\r\n\r\n" + self.body)
        session.quit

    def log_email(self):
        with open('messaging.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}: Recipient:{self.recipient}, Subject:{self.subject}")
