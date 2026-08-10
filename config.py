import os
from dotenv import load_dotenv

load_dotenv()

YAHOO_EMAIL = os.environ["YAHOO_EMAIL"]
YAHOO_APP_PASSWORD = os.environ["YAHOO_APP_PASSWORD"]

OPEN_AI_KEY = os.environ["OPEN_AI_KEY"]

YAHOO_IMAP_SERVER = "imap.mail.yahoo.com"
YAHOO_IMAP_PORT = 993

DATABASE_FILE = "internships.db"

INITIAL_SYNC_DAYS = 90