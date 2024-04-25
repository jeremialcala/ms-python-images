import re
from constants import BASE64_EXPRESSION


def is_base64(base64_string):
    return re.match(BASE64_EXPRESSION, base64_string)
