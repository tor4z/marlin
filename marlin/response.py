class HTTPResponse:
    def __init__(self, sock, method, url):
        self.fp = sock.makefile("rb")
        self.method = method
        self.url = url

    def read(self):
        return self.fp.read()

    def close(self):
        fp = self.fp
        fp.close()
        self.fp = None
