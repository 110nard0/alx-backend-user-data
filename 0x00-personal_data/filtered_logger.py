#!/usr/bin/env python3
"""filtered_logger module"""

import logging
import re
from typing import List

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
 
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler = logging.StreamHandler
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
    return logger


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
