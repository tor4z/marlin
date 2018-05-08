import pytest
from marlin.connection import HTTPConnection, schema_to_port

host = "www.python.org"
port = 443


def test_schema_to_port():
    schemas = {"http": 80, "https": 443}
    for schema in schemas:
        port = schema_to_port(schema)
        assert port == schemas[schema]


def test_parse_host_port():
    h, p = HTTPConnection.get_host_port(host, port)
    assert host == h
    assert port == p

    h, p = HTTPConnection.get_host_port("http://www.google.com")
    assert h == "www.google.com"
    assert p == 80

    h, p = HTTPConnection.get_host_port("https://www.google.com")
    assert h == "www.google.com"
    assert p == 443

    h, p = HTTPConnection.get_host_port("www.google.com")
    assert h == "www.google.com"
    assert p == 80


def test_connect():
    conn = HTTPConnection(host, port)
    conn.connect()
    assert conn.sock is not None
    conn.close()


def test_send_data():
    host = "socket.io"
    port = 80
    conn = HTTPConnection(host, port)
    conn.connect()
    conn.send(b'data')
    resp = conn.get_reponse()
    data = resp.read()
    conn.close()

    assert "HTTP" in str(data)
