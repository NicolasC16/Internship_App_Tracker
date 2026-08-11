import os
from dotenv import load_dotenv

load_dotenv()

YAHOO_EMAIL = os.environ["YAHOO_EMAIL"]
YAHOO_APP_PASSWORD = os.environ["YAHOO_APP_PASSWORD"]

YAHOO_IMAP_SERVER = "imap.mail.yahoo.com"
YAHOO_IMAP_PORT = 993

DATABASE_FILE = "internships.db"

# How many recent emails to process
INITIAL_EMAIL_LIMIT = 50