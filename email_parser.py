import email
from bs4 import BeautifulSoup


def html_to_text(html):
    """
    Convert HTML email content into readable text.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove elements that don't contain useful email text
    for element in soup([
        "script",
        "style",
        "head",
        "title"
    ]):
        element.decompose()

    text = soup.get_text(
        "\n",
        strip=True
    )

    return text


def get_email_body(msg):
    """
    Extract readable text from an email.

    Handles:
    - plain-text emails
    - HTML emails
    - multipart emails
    - emails with attachments
    """

    plain_text_parts = []
    html_parts = []

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()

            disposition = (
                part.get("Content-Disposition")
                or ""
            )

            # Ignore attachments
            if "attachment" in disposition.lower():
                continue

            # Ignore nested multipart containers
            if content_type not in (
                "text/plain",
                "text/html"
            ):
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

            try:
                decoded = payload.decode(
                    charset,
                    errors="replace"
                )
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode(
                    "utf-8",
                    errors="replace"
                )

            if content_type == "text/plain":

                plain_text_parts.append(
                    decoded
                )

            elif content_type == "text/html":

                html_parts.append(
                    html_to_text(decoded)
                )

    else:

        payload = msg.get_payload(
            decode=True
        )

        if payload:

            charset = (
                msg.get_content_charset()
                or "utf-8"
            )

            try:
                decoded = payload.decode(
                    charset,
                    errors="replace"
                )
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode(
                    "utf-8",
                    errors="replace"
                )

            if msg.get_content_type() == "text/html":

                html_parts.append(
                    html_to_text(decoded)
                )

            else:

                plain_text_parts.append(
                    decoded
                )

    # Prefer plain text when available.
    if plain_text_parts:

        text = "\n\n".join(
            plain_text_parts
        )

    elif html_parts:

        text = "\n\n".join(
            html_parts
        )

    else:

        text = ""

    return text.strip()


def parse_email(raw_email):

    msg = email.message_from_bytes(
        raw_email
    )

    return {
        "message_id": msg.get("Message-ID"),
        "sender": msg.get("From"),
        "subject": msg.get("Subject"),
        "date": msg.get("Date"),
        "body": get_email_body(msg)
    }

