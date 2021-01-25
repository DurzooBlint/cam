import smtplib
import ssl
import datetime
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

        # Load config from file
        config = configparser.ConfigParser()
        config.read("config.conf")
        self.SMTP_SERVER = config['DEFAULT']['SMTP_SERVER']
        self.SMTP_PORT = config['DEFAULT']['SMTP_PORT']
        self.GMAIL_USERNAME = config['DEFAULT']['GMAIL_USERNAME']
        self.GMAIL_PASSWORD = config['DEFAULT']['GMAIL_PASSWORD']

    def send_email(self):
        # # Create Headers
        # headers = ["From: " + self.GMAIL_USERNAME, "Subject: " + self.subject, "To: " + self.recipient,
        #            "MIME-Version: 1.0", "Content-Type: text/html"]
        # headers = "\r\n".join(headers)
        #
        # # Connect to Gmail Server
        # session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        # session.ehlo()
        # session.starttls()
        # session.ehlo()
        #
        # # Login to Gmail
        # session.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)
        #
        # # Send Email & Exit
        # session.sendmail(self.GMAIL_USERNAME, self.recipient, headers + "\r\n\r\n" + self.body)
        # session.quit

        message = MIMEMultipart("alternative")
        message["Subject"] = "Guardian alert: Activity detected"
        message["From"] = self.GMAIL_USERNAME
        message["To"] = self.recipient

        # Create the plain-text and HTML version of your message
        html = """\
        <html>
          <body>
            <p>
                <b>Guardian Alert</b>
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.body, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT, context=context) as server:
            server.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)
            server.sendmail(
                self.GMAIL_USERNAME, self.recipient, message.as_string()
            )

    def log_email(self):
        with open('messaging.log', 'a', encoding='utf-8') as f:
            f.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}: Recipient:{self.recipient}, Subject:{self.subject}")
