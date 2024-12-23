"""
Contains the utilities/functions for the app/project.
"""

import uuid
import random
import string


def get_uuid4():
    """
    Returns:
        (str) uuid4
    """
    return uuid.uuid4().hex


def get_random_letters(length: int):
    """
    Returns the text that contains random letters, this can
    contain A-Z, a-z and 0-9.

    Returns:
        (str) random letters string
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
