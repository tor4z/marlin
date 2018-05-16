from urllib.parse import urlparse, urljoin


def relative_to_absolute(self, host, path):
    return urljoin(host, path)


schemes = {"http": 80,
           "https": 443}


def scheme_to_port(scheme):
    port = schemes.get(scheme, None)
    if port is None:
        raise URLError("not suport scheme")
    return port


class Url:
    '''
    General structure of URL: scheme://netloc/path;parameters?query#fragment
    https://docs.python.org/3/library/urllib.parse.html
    URL structure defined by this class:
    scheme://host:port/path;parameters?query#fragment
    '''

    def __init__(self, url):
        self.url = url
        self._parse_result = urlparse(url)
        self._path = None
        self._scheme = None
        self._host = None
        self._port = None
        self._params = None
        self._query = None
        self._fragment = None

    @property
    def path(self):
        if self._path is None:
            self._path = self._parse_result.path or "/"
        return self._path

    @property
    def scheme(self):
        if self._scheme is None:
            self._scheme = self._parse_result.scheme
        return self._scheme

    @property
    def host(self):
        # eg.
        # if the url is https://docs.python.org/3.8/library/socket.html
        # it will return docs.python.org
        if self._host is None:
            netloc = self._parse_result.netloc
            i = netloc.rfind(":")
            if i > 0:
                self._path = netloc[:i]
        return self._path

    @property
    def port(self):
        if self._port is None:
            netloc = self._parse_result.netloc
            i = netloc.find(":")
            self._port = netloc[i + 1:]
            if not self._port:
                self._port = scheme_to_port(self.scheme)
        return self._port

    @property
    def query(self):
        if self._query is None:
            self._query = self._parse_result.query
        return self._query

    @property
    def params(self):
        if self._params is None:
            self._params = self._parse_result.params
        return self._params

    @property
    def fragment(self):
        if self._fragment is None:
            self._fragment = self._parse_result.fragment
        return self._fragment


class URLError(Exception):
    pass
