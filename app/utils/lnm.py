import base64
from datetime import datetime


def get_timestamp():
    # format --> YYYYMMDDHHmmss
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return timestamp


def generate_password(business_shortcode: str, lnm_passkey: str):
    password = f"{business_shortcode}{lnm_passkey}{get_timestamp()}"
    encoded = base64.b64encode(bytes(password, encoding="utf8"))
    return encoded.decode("utf-8")
