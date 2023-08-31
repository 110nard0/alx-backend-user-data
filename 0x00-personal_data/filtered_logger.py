#!/usr/bin/env python3
"""filtered_logger module"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates log message using regex operation"""
    for field in fields:
        pattern = rf'{field}=.*?{separator}'
        substitution = f"{field}={redaction}{separator}"
        message = re.sub(pattern, substitution, message)
    return message
