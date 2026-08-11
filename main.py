from yahoo_mail import YahooMail
from email_parser import parse_email

from database import (
    initialize_database,
    email_already_processed,
    save_email
)

from config import INITIAL_EMAIL_LIMIT

INTERNSHIP_KEYWORDS =  [

    "intern",
    "internship",

    "software engineering intern",
    "software engineering internship",

    "summer internship",
    "summer intern",

    "application",
    "interview",
    "candidate",
    "recruiter",
    "recruiting",
    "hiring",
    "assessment",
    "offer"
]

def might_be_internship_email(email_data):

    subject = str(
        email_data["subject"]
        or ""
    )

    body = str(
        email_data["body"]
        or ""
    )

    text = (
        subject + " " + body
    ).lower()

    for keyword in INTERNSHIP_KEYWORDS:

        if keyword in text:
            return True
        
    return False

def process_email(email_data):

    parsed = parse_email(
        email_data["raw"]
    )

    message_id = (
        parsed["message_id"]
    )

    print()

    print(
        "-----------------------------------"
    )

    print(f"From: {parsed['sender']}")

    #--------------------------------------
    # Duplicate Sender
    #--------------------------------------

    if email_already_processed(
        message_id
    ):

        print("Already processed.")

        return

    #--------------------------------------
    # Keyword Filtering
    #--------------------------------------

    if not might_be_internship_email(parsed):
        print("Not an internship email.")

        save_email(
            message_id,
            parsed["sender"],
            parsed["subject"],
            parsed["date"]
        )

        return

    #---------------------------------------
    # Potential Internship
    #---------------------------------------

    print(
        "Potential internship email!"
    )

    print()

    print("EMAIL PREVIEW")

    print(parsed["body"][:1000])

    # Save it for now
    save_email(
        message_id,
        parsed["sender"],
        parsed["subject"],
        parsed["date"]
    )

def main():

    print("==============================")
    print("Internship Email Tracker")
    print("==============================")

    initialize_database()

    yahoo = YahooMail()

    try:
        yahoo.connect()

        emails = yahoo.get_recent_emails(limit=INITIAL_EMAIL_LIMIT)

        print()
        print(f"Found {len(emails)} recent emails")

        for email_data in emails:

            process_email(
                email_data
            )

    finally:
        yahoo.close()

        print()
        print("Yahoo connection closed.")

if __name__ == "__main__":
    main()