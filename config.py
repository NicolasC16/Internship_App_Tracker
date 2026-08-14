# This file is responsible for configuring the information 
# needed to communicate with Yahoo.

import os
from dotenv import load_dotenv

load_dotenv()                                               #Loads the .env file

YAHOO_EMAIL = os.environ["YAHOO_EMAIL"]                     # Gets my yahoo email address from .env
YAHOO_APP_PASSWORD = os.environ["YAHOO_APP_PASSWORD"]       # Gets my yahoo app password from .env

YAHOO_IMAP_SERVER = "imap.mail.yahoo.com"                   # Store's Yahoo's IMAP server address
YAHOO_IMAP_PORT = 993                                       # Stores the port used for IMAP

DATABASE_FILE = "internships.db"                            # Sets the name for the SQLite database file

# How many recent emails to process
INITIAL_EMAIL_LIMIT = 50                                    