from yahoo_mail import YahooMail
from email_parser import parse_email

from database import (
    initialize_database,
    email_already_processed,
    save_email,
    save_application
)

from config import INITIAL_EMAIL_LIMIT

from application_extractor import extract_application

# --------------------------------------
# Internship / Employment Indicators
# --------------------------------------

STRONG_INTERNSHIP_KEYWORDS = [

    "internship",
    "intern position",
    "intern role",
    "intern/co-op",
    "internship program",

    "software engineering intern",
    "software engineer intern",
    "software development engineer intern",

    "summer intern",
    "summer internship",

    "recruiter",
    "recruiting team",

    "job application",
    "employment application",

    "application for the position",
    "application for the role",

    "application has been received",
    "application has been submitted",

    "thank you for applying to",
    "thanks for applying to",

    "interview invitation",
    "interview scheduled",

    "coding assessment",
    "technical assessment",

    "candidate for",
    "candidate status",

    "hiring team",
    "hiring manager",

    "offer letter",
    "employment offer"
]


SUPPORTING_INTERNSHIP_KEYWORDS = [

    "position",
    "role",
    "job",
    "career",
    "hiring",
    "candidate",
    "recruiter",
    "recruiting",
    "interview",
    "assessment",
    "application",
    "offer",
    "applying",
    "Applying"
]


# --------------------------------------
# Known Non-Employment Topics
# --------------------------------------

NON_EMPLOYMENT_KEYWORDS = [

    "scholarship",
    "financial aid",
    "student loan",
    "housing",
    "lease",
    "rent",
    "resident portal",
    "apartment",
    "roommate",
    "bank account",
    "credit card",
    "membership",
    "member portal",
    "donation",
    "fundraising",
    "just posted"
]

def might_be_internship_email(email_data):

    subject = str(
        email_data.get("subject")
        or ""
    )

    body = str(
        email_data.get("body")
        or ""
    )

    text = (
        subject
        + "\n"
        + body
    ).lower()

    print()
    print("========== KEYWORD DEBUG ==========")

    print("SUBJECT:")
    print(subject)

    print()
    print("NON-EMPLOYMENT MATCHES:")

    non_employment_matches = []

    for keyword in NON_EMPLOYMENT_KEYWORDS:

        if keyword.lower() in text:

            non_employment_matches.append(keyword)

    print(non_employment_matches)

    print()
    print("STRONG MATCHES:")

    strong_matches = []

    for keyword in STRONG_INTERNSHIP_KEYWORDS:

        if keyword.lower() in text:

            strong_matches.append(keyword)

    print(strong_matches)

    print()
    print("SUPPORTING MATCHES:")

    supporting_matches = []

    for keyword in SUPPORTING_INTERNSHIP_KEYWORDS:

        if keyword.lower() in text:

            supporting_matches.append(keyword)

    print(supporting_matches)

    print()
    print("====================================")

    if non_employment_matches:

        print(
            "REJECTED BECAUSE OF:",
            non_employment_matches
        )

        return False

    if len(strong_matches) >= 1:

        print("ACCEPTED: Strong keyword match")

        return True

    if len(supporting_matches) >= 3:

        print("ACCEPTED: Supporting keyword match")

        return True

    print("REJECTED: Not enough employment keywords")

    return False

def might_be_internship_email(email_data):

    subject = str(
        email_data.get("subject")
        or ""
    )

    body = str(
        email_data.get("body")
        or ""
    )

    text = (
        subject
        + "\n"
        + body
    ).lower()

    print()
    print("========== KEYWORD DEBUG ==========")

    print("SUBJECT:")
    print(subject)

    print()
    print("NON-EMPLOYMENT MATCHES:")

    non_employment_matches = []

    for keyword in NON_EMPLOYMENT_KEYWORDS:

        if keyword.lower() in text:

            non_employment_matches.append(keyword)

    print(non_employment_matches)

    print()
    print("STRONG MATCHES:")

    strong_matches = []

    for keyword in STRONG_INTERNSHIP_KEYWORDS:

        if keyword.lower() in text:

            strong_matches.append(keyword)

    print(strong_matches)

    print()
    print("SUPPORTING MATCHES:")

    supporting_matches = []

    for keyword in SUPPORTING_INTERNSHIP_KEYWORDS:

        if keyword.lower() in text:

            supporting_matches.append(keyword)

    print(supporting_matches)

    print()
    print("====================================")

    if non_employment_matches:

        print(
            "REJECTED BECAUSE OF:",
            non_employment_matches
        )

        return False

    if len(strong_matches) >= 1:

        print("ACCEPTED: Strong keyword match")

        return True

    if len(supporting_matches) >= 3:

        print("ACCEPTED: Supporting keyword match")

        return True

    print("REJECTED: Not enough employment keywords")

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
    print(f"Subject: {parsed['subject']}")

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

    #---------------------------------------
    # Extract Application Information
    #---------------------------------------

    application = extract_application(parsed)

    print()

    print("APPLICATION INFORMATION")

    print(f"Company: {application['company']}")

    print(f"Position: {application['position']}")

    print(f"Status: {application['status']}")

    print(
        f"Application Date: "
        f"{application['application_date']}"
    )

    #---------------------------------------
    # Save Application
    #---------------------------------------

    application_id = save_application(
        application["company"],
        application["position"],
        application["location"],
        application["application_date"],
        application["status"],
        application["interview_date"],
        application["deadline"],
        application["recruiter_name"],
        application["recruiter_email"],
        application["next_action"],
        application["confidence"],
        application["last_updated"],
    )

    print()

    print(
        f"Application saved with ID: "
        f"{application_id}"
    )

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