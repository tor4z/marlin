from http.cookiejar import CookieJar
from datetime import datetime


class HTTPRequest:

    def __init__(self, method, url, headers=None):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.cookies = None
        self.http_version = 1.1

    def set_header(self, key, value):
        self.headers[key] = value

    def update_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("dict required.")
        self.headers.update(headers)

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("dict required.")
        self.headers = headers

    def set_cookies(self, cookies):
        if not isinstance(cookies, CookieJar):
            raise TypeError("CookieJar required.")
        self.cookies = cookies

    def set_http_version(self, version):
        self.http_version = version

    def request_line(self):
        request = f"{self.method} {self.url.path} HTTP/{self.http_version}\r\n"
        return request.encode()
    
    def headers_data(self):
        headers = ""
        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"
        return headers.encode()

    def cookies_data(self):
        if self.cookies:
            cookies =  self.cookies.output(header = "Cookie:")
            if not isinstance(cookies, bytes):
                cookies = cookies.encode()
            return cookies
        else:
            return b''

    def request_date(self):
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        return date.encode()

    def request_data(self):
        data = self.request_line() +\
               self.headers_data() +\
               self.request_date() +\
               self.cookies_data()
        return data
