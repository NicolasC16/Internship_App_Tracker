import re


def extract_company(sender, subject, body):
    """
    Try to determine the company from the email.
    """

    text = (
        sender
        + " "
        + subject
        + " "
        + body[:3000]
    )

    # Amazon
    if "amazon" in text.lower():
        return "Amazon"

    # Virtu
    if "virtu" in text.lower():
        return "Virtu Financial"

    return "Unknown"


def extract_position(subject, body):
    """
    Try to determine the internship position.
    """

    text = subject + " " + body

    patterns = [

        r"for the ([^.]{5,150}?) position",

        r"application for (?:the )?([^.]{5,150})",

        r"applied for (?:the )?([^.]{5,150})",

        r"position:\s*([^\n]{5,150})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            position = match.group(1)

            return position.strip()

    return "Unknown"


def determine_status(subject, body):
    """
    Determine the current application status.
    """

    text = (
        subject
        + " "
        + body
    ).lower()

    if any(
        phrase in text
        for phrase in [
            "we regret to inform",
            "not moving forward",
            "will not be moving forward",
            "unfortunately",
            "not selected",
            "rejection"
        ]
    ):
        return "Rejected"

    if any(
        phrase in text
        for phrase in [
            "interview scheduled",
            "schedule an interview",
            "interview invitation",
            "invite you to interview"
        ]
    ):
        return "Interview"

    if any(
        phrase in text
        for phrase in [
            "offer",
            "pleased to offer",
            "offer letter"
        ]
    ):
        return "Offer"

    if any(
        phrase in text
        for phrase in [
            "application received",
            "received your application",
            "thank you for applying",
            "application has been submitted",
            "successfully applied"
        ]
    ):
        return "Applied"

    return "Unknown"


def extract_application(email_data):

    sender = str(
        email_data.get("sender")
        or ""
    )

    subject = str(
        email_data.get("subject")
        or ""
    )

    body = str(
        email_data.get("body")
        or ""
    )

    company = extract_company(
        sender,
        subject,
        body
    )

    position = extract_position(
        subject,
        body
    )

    status = determine_status(
        subject,
        body
    )

    return {
        "company": company,
        "position": position,
        "location": None,
        "application_date": email_data.get("date"),
        "status": status,
        "interview_date": None,
        "deadline": None,
        "recruiter_name": None,
        "recruiter_email": None,
        "next_action": None,
        "confidence": 0.50,
        "last_updated": email_data.get("date")
    }