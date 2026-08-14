# This file is responsible for converting the raw email into
# something that the program can work with.

import email
from bs4 import BeautifulSoup


def html_to_text(html):                                     # Creates a function that accepts HTML
    """
    Convert HTML email content into readable text.
    """

    soup = BeautifulSoup(                                   # Parses a raw HTML string and converts it into a searchable Python object
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

    text = soup.get_text(                                   # Extracts the actual visible text
        "\n",
        strip=True
    )

    return text                                             # Returns the cleaned text


def get_email_body(msg):
    """
    Extract readable text from an email.

    Handles:
    - plain-text emails
    - HTML emails
    - multipart emails
    - emails with attachments
    """

    plain_text_parts = []                                       # Stores text/plain emails
    html_parts = []                                             # Stores text/html emails

    if msg.is_multipart():                                      # Checks if the email is multiple parts

        for part in msg.walk():                                 # Walk through every part of the email

            content_type = part.get_content_type()              # Check the type of content

            disposition = (                                     # Checks if the part is an attachment
                part.get("Content-Disposition")
                or ""
            )

            # Ignore attachments
            if "attachment" in disposition.lower():
                continue

            # Ignore anything that isnt readable email text. 
            if content_type not in (
                "text/plain",
                "text/html"
            ):
                continue

            # Extracts the actual bytes from the email part.
            payload = part.get_payload(
                decode=True
            )

            # If there is no content then skip.
            if not payload:
                continue

            # Determines how bytes should be decoded. 
            charset = (
                part.get_content_charset()
                or "utf-8"
            )

            # Converts bytes into Python text
            try:
                decoded = payload.decode(
                    charset,
                    errors="replace"
                )
            # If the specified character encoding does not exists, try UTF-8 instead. 
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode(
                    "utf-8",
                    errors="replace"
                )

            # If the content type is plain text, store it in the list
            if content_type == "text/plain":

                plain_text_parts.append(decoded)

            # If the content type is HTML, convert into readable text, then store it in the list.
            elif content_type == "text/html":
                html_parts.append(html_to_text(decoded))

    else:   #Non-multipart emails

        payload = msg.get_payload(decode=True)          # Get the email body.

        if payload:

            charset = (msg.get_content_charset() or "utf-8")

            try:
                decoded = payload.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode("utf-8", errors="replace")

            # If HTML, then convert to readable text and store, if plain text, then store.
            if msg.get_content_type() == "text/html":
                html_parts.append(html_to_text(decoded))
            else:
                plain_text_parts.append(decoded)

    # Prefer plain text when available.
    if plain_text_parts:

        text = "\n\n".join(plain_text_parts)

    elif html_parts:

        text = "\n\n".join(html_parts)

    else:

        text = ""

    return text.strip()         # Removes unnecessary whitespace


def parse_email(raw_email):     # This is the main parser function.

    msg = email.message_from_bytes(raw_email)   # Converts the raw email bytes from Yahoo into a Python email object and stores it.

    # Creates a clean dictionary that stores email content. 
    return {
        "message_id": msg.get("Message-ID"),
        "sender": msg.get("From"),
        "subject": msg.get("Subject"),
        "date": msg.get("Date"),
        "body": get_email_body(msg)
    }

