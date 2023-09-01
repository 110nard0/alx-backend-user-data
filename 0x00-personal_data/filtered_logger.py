#!/usr/bin/env python3
"""Filtered Logger Module"""

from typing import List
import logging
import mysql.connector
import os
import re

# User PII fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates log message using regex operation"""
    for field in fields:
        pattern = rf'{field}=.*?{separator}'
        substitution = f"{field}={redaction}{separator}"
        message = re.sub(pattern, substitution, message)
    return message


def get_logger() -> logging.Logger:
    """Creates a Logger object with a StreamHandler"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a MySQL database connection object"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name
    )

    return db


def main():
    """Obtains and logs user details from a database"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        log_message = "; ".join([f"{key}={value}"
                                for key, value in row.items()])
        logger.info(log_message)

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter class instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records"""
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_message, self.SEPARATOR)


if __name__ == "__main__":
    main()
