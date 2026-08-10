import email
from bs4 import BeautifulSoup

def get_email_body(msg):
    """
    Extract readable text from an email.
    Handles plain-text and HTML emails
    """

    text = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()
            disposition = str(
                part.get("Content-Disposition")
            )

            # Ignore attachments
            if "attachment" in disposition:
                continue

            payload = part.get_payload(
                decode=True
            )

            if not payload:
                continue

            charset = (
                part.get_content_charset()
                or "utf-8"
            )

            decoded = payload.decode(
                charset,
                errors="replace"
            )

            if content_type == "text/html":

                text += BeautifulSoup(
                    decoded,
                    "html.parser"
                ).get_text(
                    " ",
                    strip=True
                )
    else:
        payload = msg.get_payload(
            decode = True
        )

        if payload:

            charset = (
                msg.get_content_charset()
                or "utf-8"
            )

            text = payload.decode(
                charset,
                errors="replace"
            )

    return text.strip()


def parse_email(raw_email):

    msg = email.message_from_bytes(
        raw_email
    )

    return{
        "message_id": msg.get("Message-ID"),
        "sender": msg.get("From"),
        "subject": msg.get("Subject"),
        "date": msg.get("Date"),
        "body": get_email_body
    }