import sys
import socket


class Connection(object):
    """
    A representation of a socket.

    :param host: A domain name or an IP address
    :param port: A port number
    """
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self._socket = None

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        if not 0 < port < 2**16:
            raise ValueError('Invalid port range')
        self.__port = port

    def establish(self):
        (family, type, proto, canonname,
            sockaddr) = socket.getaddrinfo(self.host, self.port,
                                           socket.AF_INET,
                                           socket.SOCK_STREAM)[0]
        self._socket = socket.socket(family, type, proto)
        self._socket.connect(sockaddr)

    def write(self, request):
        self._socket.send(request)

    def read(self, bufsize=4096):
        return self._socket.recv(bufsize)

    def close(self):
        self._socket.close()
