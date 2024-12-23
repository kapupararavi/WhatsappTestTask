"""
Contains function(s) those are used inside API or for the process.
"""

from typing import Optional
import requests
from django.conf import settings


def send_wa_message(to: str, text_content: Optional[str] = None):
    """
    Send the whatsapp message using its API, requires `to` phone number.
    if the `text_content` parameter not provided or is `None` then the
    default `hello_world` template will be sent.

    Args:
        to (str): Phone number in string (a valid whatsapp phone number string)
        text_content (Optional,str): text message, default is `None` to send template

    Returns:
        (requests.)
    """
    # text_content = None  # For debug purpose

    endpoint = f"https://graph.facebook.com/v21.0/{settings.WA_BUSINESS_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WA_ACCESS_TOKEN}"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": None,
    }
    template = {
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": settings.DEFAULT_WA_LANGUAGE_CODE
            }
        }
    }
    text_message = {
        "type": "text",
        "text": {
            "body": text_content
        }
    }
    if text_content is None:
        data.update(template)
    else:
        data.update(text_message)
    res = requests.post(endpoint, json=data, headers=headers, timeout=30)
    res.raise_for_status()
    return res
