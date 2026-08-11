import sqlite3

from config import DATABASE_FILE

def get_connection():

    return sqlite3.connect(
        DATABASE_FILE
    )

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    #----------------------------------
    # Emails Table
    #----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            sender TEXT,
            subject TEXT,
            date_received TEXT,
            processed INTEGER DEFAULT 0,
            application_id INTEGER)
    """)

    #---------------------------------
    # Applications Table
    #---------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT,
                    position TEXT,
                    location TEXT,
                    application_date TEXT,
                    status TEXT,
                    interview_date TEXT,
                    deadline TEXT,
                    recruiter_name TEXT,
                    recruiter_email TEXT,
                    next_action TEXT,
                    confidence REAL,
                    last_updated TEXT)
    """)

    connection.commit()
    connection.close()

def email_already_processed(message_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM emails
        WHERE message_id = ?
        """,
        (message_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None

def save_email(
        message_id,
        sender,
        subject,
        date_received,
        application_id=None
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO emails(
            message_id,
            sender,
            subject,
            date_received,
            processed,
            application_id
        )
        VALUES (?, ?, ?, ?, 1, ?)
        """,
        (
            message_id,
            sender,
            subject,
            date_received,
            application_id
        )
    )

    connection.commit()
    connection.close()

def save_application(
        company,
        position,
        location,
        application_date,
        status,
        interview_date,
        deadline,
        recruiter_name,
        recruiter_email,
        next_action,
        confidence,
        last_updated,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO applications(
        company,
        position,
        location,
        application_date,
        status,
        interview_date,
        deadline,
        recruiter_name,
        recruiter_email,
        next_action,
        confidence,
        last_updated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company,
            position,
            location,
            application_date,
            status,
            interview_date,
            deadline,
            recruiter_name,
            recruiter_email,
            next_action,
            confidence,
            last_updated,
        )
    )

    application_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return application_id