import re

response_sep = "\r\n\r\n"


def raw_response_to_header_body(rawdata):
    # return header, body
    if isinstance(rawdata, bytes):
        # Try to decode data with utf-8
        # Not promise success
        rawdata = rawdata.decode()
    result = rawdata.split(response_sep)
    return result[0], response_sep.join(result[1:])


_HEADER_KEY = r"\w\d!#%&'~_`><@,:/\$\*\+\-\.\^\|\)\(\?\}\{\="
_HEADER_VALUE = _HEADER_KEY + r"\[\]"
_HEADERS_PAT = re.compile(r'''
    \s*                             # Optional space
    (?P<key>                        # Start group of key
    [''' + _HEADER_KEY + r''']+?    # Match least one letter
    )                               # End group of key
    \s*:\s*                         # Optional sapce and : sign
    (?P<value>                      # Start of value group
    [''' + _HEADER_VALUE + r''']    # Match least one letter
    )                               # End of value group
    \s*''', re.ASCII | re.VERBOSE)  # Optional space (which includes
                                    # [ \t\n\r\f\v])
# e.g. HTTP/1.1 200 OK\r\n
_HTTP_VERSION = r"\d\."
_HTTP_STATUS_CODE = r"\d"
_HTTP_REASON = r"[^\r\n]"
_HTTP_RESPONSE_PAT = re.compile(r'''
    \s*                                 # Optional space
    HTTP\s*?/\s*?                       # HTTP keyword and slash
    (?P<version>                        # Start of version group
    [''' + _HTTP_VERSION + r''']+?      # Match HTTP version
    )                                   # End of version group
    \s+                                 # Match least one space
    (?P<status_code>                    # Start of status code group
    [''' + _HTTP_STATUS_CODE + r''']+?  # Match HTTP status code
    )                                   # End of status code group
    \s+                                 # Match least one space
    (?P<reason>                         # Start of reason group
    [''' + _HTTP_REASON + r''']+?       # Match HTTP Rsponse status
    )                                   # End of reason group
    \s*''', re.ASCII | re.VERBOSE)      # Optional space

# e.g.
# Set-Cookie: auth_key=827525; expires=Thu, 07-Jun-2018 22:19:06 GMT;\
# Max-Age=2592000; path=/; domain=.aixifan.com\r\n
_HTTP_COOKIE_PAT = re.compile(r'''
    \s*                                 # Optional space
    Set-Cookie                          # Set-Cookie keyword
    \s*:\s*                             # Optional space and ':' sign
    (?P<cookie>                         # Start of cookie group
    [^\r\n]+?                           # Match any letter excepct '\r\n'
    )                                   # End of cookie group
    \s*''', re.ASCII | re.VERBOSE)      # Optional space


class HTTPResponse:
    def __init__(self, conn, method, url):
        # sock.makefile not support not blocking socket
        # The socket must be in blocking mode; it can have a timeout,
        # but the file object’s internal buffer may end up in an
        # inconsistent state if a timeout occurs.
        # https://docs.python.org/3/library/socket.html#socket.socket.makefile
        self.conn = conn
        self.method = method
        self.url = url

    def _read(self):
        pass

    def _read_response_header(self):
        pass

    def _read_body(self):
        pass

    @property
    def status_code(self):
        pass

    @property
    def reason(self):
        pass

    @property
    def ok(self):
        pass

    @property
    def cookies(self):
        pass

    @property
    def body(self):
        pass

    @property
    def headers(self):
        # Delete set_cookie fields.
        pass

    @property
    def charset(self):
        pass

    @property
    def content_type(self):
        pass
