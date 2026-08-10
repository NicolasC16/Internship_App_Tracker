import imaplib

from config import (
    YAHOO_EMAIL,
    YAHOO_APP_PASSWORD,
    YAHOO_IMAP_SERVER,
    YAHOO_IMAP_PORT
)

class YahooMail:

    def __init__(self):

        self.mail = None

    def connect(self):

        print("Connecting to Yahoo")

        self.mail = imaplib.IMAP4_SSL(
            YAHOO_IMAP_SERVER,
            YAHOO_IMAP_PORT
        )

        self.mail.login(
            YAHOO_EMAIL,
            YAHOO_APP_PASSWORD
        )

        self.mail.select("INBOX")

        print("Connected to Yahoo.")

    def get_recent_emails(self, limit=50):

        status, messages = self.mail.search(
            None,
            "ALL"
        )

        if status != "OK":
            return[]

        email_ids = messages[0].split()

        #Get only the newest emails
        email_ids = email_ids[-limit:]

        emails = []

        for email_id in email_ids:

            status, data = self.mail.fetch(
                email_id,
                "(RFC822)"
            )

            if status != "OK":
                continue

            raw_email = data[0][1]

            emails.append({
                "id": email_id.decode(),
                "raw": raw_email
            })

            return emails

    def close(self):

        if self.mail:

            try:
                self.mail.close()
            except Exception:
                pass

            try:
                self.mail.logout()
            except Exception:
                pass