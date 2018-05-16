__all__ = ["cookie_to_dict", "dict_to_cookie", "merge_cookie",
           "rawdata_to_cookies"]


def cookie_to_dict(cookie):
    pass


def dict_to_cookie(dic):
    pass


def merge_cookie(*cookies):
    pass


line_sep = "\r\n"


def rawdata_to_cookies(data):
    if not isinstance(data, str):
        # Try to decode data with default utf-8
        # Not promise success
        data = data.decode()
    for line in data.split(line_sep):
        pass
