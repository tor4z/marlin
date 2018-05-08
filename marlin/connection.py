import socket
import asyncio
import logging
import collections

from .response import HTTPResponse

log = logging.getLogger(__name__)
schemas = {"http": 80,
           "https": 443}

def schema_to_port(schema):
    port = schemas.get(schema, None)
    if port is None:
        raise Error("not suport schema")
    return port

class HTTPConnection:

    @classmethod
    def get_host_port(self, host, port=None):
        # http://www.python.org:80
        # Default port equal to 80
        i = host.rfind("/")
        j = host.find(":")
        if j != -1 and i > j:
            schema = host[:j]
        else:
            schema = None
        host = host[i + 1:]
        i = host.rfind(":")

        if i == -1:
            if port is None:
                if schema is None:
                    port = 80
                else:
                    port = schema_to_port(schema)
        else:
            port = host[i + 1:]
            host = host[:i]
        return (host, port)

    def __init__(self, host, port=None, timeout=None, source_address=None):
        self.timeout = timeout
        self.sock= None
        self.source_address = source_address
        (self.host, self.port) = self.get_host_port(host, port)
        self.method = None
        self.url = None

    def _create_connection(self, host, port, timeout=None,
                           source_address=None, family=None,
                           type=None, proto=None, flags=0):
        family = family or socket.AF_INET
        type = type or socket.SOCK_STREAM
        proto = proto or socket.IPPROTO_IP
        err = None
        log.debug("connect to {host}")

        for res in socket.getaddrinfo(host, port, family, type,
                                      proto, flags):
            af, socktype, proto, _, sa = res

            try:
                sock = socket.socket(af, socktype, proto)
                if timeout is not None:
                    sock.settimeout(timeout)
                if source_address is not None:
                    sock.bind(source_address)
                sock.connect(sa)
                return sock
            except Exception as e:
                if sock is not None:
                    sock.close()
                err = e

        if err is None:
            raise SocketError("getaddrinfo return empty list.")
        else:
            raise SocketError(err)

    def connect(self):
        self.sock = self._create_connection(self.host, self.port, 
                                            self.timeout, self.source_address)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.setblocking(True)

    def close(self):
        self.sock.close()

    def send(self, data):
        # auto connect
        if not self.sock:
            self.connect()

        if isinstance(data, bytes):
            self.sock.sendall(data)
        else:
            for d in data:
                self.sock.sendall(d)

    def get_reponse(self):
        if self.sock is not None:
            return HTTPResponse(self.sock, self.method, self.url)
        else:
            raise Error("not connected")

    def putrequest(self):
        pass

    def putheader(self):
        pass

    def endheader(self):
        pass

    def request(self, method, url, body, headers={}):
        self.method = method
        self.url = url


class SocketError(Exception):
    pass


class Error(Exception):
    pass
