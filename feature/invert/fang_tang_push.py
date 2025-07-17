import requests
import re


def sc_send(send_key: str, title: str, desp: str = "", options: dict = None) -> dict:
    """
    Sends a notification using the server酱 (Server酱) or sctp services.

    Args:
        send_key (str): The API key for the notification service.
        title (str): The title of the notification.
        desp (str, optional): The description of the notification. Defaults to "".
        options (dict, optional): Additional options for the notification. Defaults to None.

    Returns:
        dict: The JSON response from the notification service.

    Raises:
        ValueError: If the `send_key` format is invalid for the `sctp` service.
    """

    if options is None:
        options = {}

    # Validate sctp format
    if send_key.startswith("sctp"):
        match = re.match(r"sctp(\d+)t", send_key)
        if match:
            num = match.group(1)
            url = f"https://{num}.push.ft07.com/send/{send_key}.send"
        else:
            raise ValueError("Invalid sendKey format for sctp (expected sctp<number>t)")
    else:
        url = f"https://sctapi.ftqq.com/{send_key}.send"

    params = {
        "title": title,
        "desp": desp,
        **options
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8"
    }

    response = requests.post(url, json=params, headers=headers)
    # Raise an exception for non-2xx status codes
    response.raise_for_status()
    return response.json()
