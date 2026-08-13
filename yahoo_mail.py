"""This file is responsible for controlling the connection and 
communication with Yahoo. It does not decode or evaluate the information within an email.
Instead it takes the raw data from an email and shares it to the rest of the program
for the data to be decoded and stored."""

import imaplib

from config import (                                # Import Yahoo configuration values from config.py
    YAHOO_EMAIL,
    YAHOO_APP_PASSWORD,
    YAHOO_IMAP_SERVER,
    YAHOO_IMAP_PORT
)

class YahooMail:

    def __init__(self):

        self.mail = None

    def connect(self):                              # Creates a function used to connect to Yahoo

        print("Connecting to Yahoo")

        self.mail = imaplib.IMAP4_SSL(              # Connects to Yahoo through it's server and port
            YAHOO_IMAP_SERVER,
            YAHOO_IMAP_PORT
        )

        self.mail.login(                            # Logs into Yahoo using my email and app password
            YAHOO_EMAIL,
            YAHOO_APP_PASSWORD
        )

        self.mail.select("INBOX")                   # Selects the inbox folder for email evaluation

        print("Connected to Yahoo.")

    def get_recent_emails(self, limit=50):          # Function used for getting recent emails

        status, messages = self.mail.search(        # Searches all of the emails within the limit
            None,
            "ALL"
        )

        if status != "OK":                          # If the search fails then return an empty list
            return[]

        email_ids = messages[0].split()             # Splits the returned bytes containing the IDs

        #Get only the newest emails
        email_ids = email_ids[-limit:]              # -limit means start 50 emails from the end then go to the end

        emails = []

        for email_id in email_ids:                  # Goes through each email ID

            status, data = self.mail.fetch(         # RFC822 asks for the entire email
                email_id,
                "(RFC822)"
            )

            if status != "OK":                      # If retrieval of a specific email fails, move on to the next
                continue

            raw_email = data[0][1]                  # Pulls the raw email bytes out of Yahoo's response

            emails.append({                         # Adds a dictionary that stores the email id and raw email to the emails list
                "id": email_id.decode(),
                "raw": raw_email
            })

        return emails                               # Returns the emails list

    def close(self):                                # Defines the function that closes and ends the communication with Yahoo

        if self.mail:                               # Check for a connection with Yahoo

            try:                                    # Closes the selected mailbox        
                self.mail.close()
            except Exception:
                pass

            try:                                    # Logs out of Yahoo
                self.mail.logout()
            except Exception:
                pass