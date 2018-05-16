import asyncio
import collections
import re

class Buffer:
    _BIG_DATA = 2048
    def __init__(self):
        self._data = collections.deque()
        self._size = 0

    def size(self):
        return self._size

    def append(self, data):
        size = len(data)
        if size < self._BIG_DATA:
            self._data.append(data)
        else:
            self._data.append(data[:self._BIG_DATA])
            remaining = data[self._BIG_DATA:]
            self.append(remaining)
            size = self._BIG_DATA
        self._size += size

    def appendleft(self, data):
        size = len(data)
        if size < self._BIG_DATA:
            self._data.appendleft(data)
        else:
            self._data.appendleft(data[-self._BIG_DATA:])
            remaining = data[:-self._BIG_DATA]
            self.appendleft(remaining)
            size = self._BIG_DATA
        self._size += size

    def pop(self, size=None):
        if size is None or size >= self.size():
            size = self.size()
        if size <= 0:
            raise ValueError("size should be greater than 0.")

        out = b''
        data = self._data.popleft()
        data_size = len(data)
        if data_size < size:
            out += data
            self._size -= data_size
            out += self.pop(size - data_size)
        elif data_size > size:
            out = data[:size]
            remaining = data[size:]
            self._size -= data_size
            self.appendleft(remaining)
        else:
            out = data
            self._size -= size

        return out

    def clear(self):
        self._data.clear()
        self._size = 0

    peek = pop

    __len__ = size


class IOStream:
    size = 65536

    def __init__(self, sock, loop=None):
        self._sock = sock
        self.fd = sock.fileno()
        self._loop = loop or asyncio.get_event_loop()
        self._write_buffer = bytearray()
        self._read_buffer = Buffer()
        self._conn_aborted = False
        self._loop.add_reader(self.fd, self.read_from_fd)
        self._loop.add_writer(self.fd, self.write_to_fd)

    def write(self, data):
        if not isinstance(data, bytes):
            raise TypeError("bytes required.")
        self._write_buffer += data

    def read(self, size):
        return self._read_buffer.peek(size)

    def read_chunk(self):
        return self.read_until_regex(b'\r\n')

    def read_until_close(self):
        data = self._read_buffer.peek()
        while not self._conn_aborted:
            data += self._read_buffer.peek()
        return data
    
    def read_until(self, delimiter):
        self.read_until_regex(delimiter)
    
    def read_until_regex(self, regex):
        if not isinstance(regex, bytes):
            raise TypeError("bytes required.")
        pat = re.compile(regex, re.IGNORECASE)
        data = b''
        while self._read_buffer.size() > 0:
            d = self._read_buffer.peek(1024)
            result =  pat.search(d)
            if not result:
                data += d
                continue
            else:
                _, end = result.span()
                data += d[:end]
                self._read_buffer.appendleft(d[end:])
                break
        return data

    def write_to_fd(self):
        if self._write_buffer:
            try:
                self._sock.sendall(self._write_buffer)
                self._write_buffer = b''
            except BlockingIOError:
                pass
    
    def read_from_fd(self):
        try:
            data = self._sock.recv(self.size)
            self._read_buffer.append(data)
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            self._conn_aborted = True

    def close(self):
        self._loop.remove_reader(self.fd)
        self._loop.remove_writer(self.fd)

    def __del__(self):
        self.close()
