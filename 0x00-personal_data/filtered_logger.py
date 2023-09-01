#!/usr/bin/env python3
"""filtered logger module"""
import os
from typing import List
import re
import logging
from mysql import connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format a record"""
        filtered = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)  # nopep8
        log_record = logging.LogRecord("my_logger", logging.INFO, None, None, filtered, None, None)  # nopep8
        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(log_record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    """filter user data function"""
    for field in fields:
        sub_pattern = fr'{field}.*?(?={separator})'
        message = re.sub(sub_pattern, f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger Object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> connector.connection.MySQLConnection:
    """Get access to the database"""
    host = os.environ.get("PERSONAL_DATA_DB_HOST")
    user = os.environ.get("PERSONAL_DATA_DB_USERNAME")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection_state = connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return connection_state
