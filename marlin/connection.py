import socket
import logging

from .response import HTTPResponse
from .util.url import scheme_to_port

log = logging.getLogger(__name__)


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
                    port = scheme_to_port(schema)
        else:
            port = host[i + 1:]
            host = host[:i]
        return (host, port)

    def __init__(self, host, port=None, timeout=None, source_address=None):
        self.timeout = timeout
        self.sock = None
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
        # Auto connect
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
            raise ConnectionError("not connected")

    def putrequest(self):
        pass

    def putheader(self):
        pass

    def endheader(self):
        pass

    def request(self, method, url, body, headers={}):
        self.method = method
        self.url = url


try:
    import ssl
except ImportError:
    pass
else:
    class HTTPSConnection(HTTPConnection):

        def __init__(self, host, port=None, key_file=None, cert_file=None,
                     timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                     source_address=None, *, context=None,
                     check_hostname=None):
            super().__init__(host, port, timeout, source_address)
            self.key_file = key_file
            self.cert_file = cert_file
            if context is None:
                context = ssl._create_default_https_context()
            will_verify = context.verify_mode != ssl.CERT_NONE
            if check_hostname is None:
                check_hostname = context.check_hostname
            if check_hostname and not will_verify:
                raise ValueError("check_hostname needs a SSL context with "
                                 "either CERT_OPTIONAL or CERT_REQUIRED")
            if key_file or cert_file:
                context.load_cert_chain(cert_file, key_file)
            self._context = context
            self._check_hostname = check_hostname

        def connect(self):
            super().connect()

            server_hostname = self.host
            self.sock = self._context.wrap_socket(
                                    self.sock,
                                    server_hostname=server_hostname)
            # Check hostname outside the context, if not check
            # the hostname in the context
            if not self._context.check_hostname and self._check_hostname:
                try:
                    ssl.match_hostname(self.sock.getpeercert(),
                                       server_hostname)
                except Exception:
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    raise


class SocketError(Exception):
    pass


class ConnectionError(Exception):
    pass
