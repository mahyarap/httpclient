import socket

class Connection(object):
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.socket = None

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        # Assert
        self.__host = host 

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        assert 0 < port < 2**16, "Invalid port range"
        self.__port = port

    def establish(self):
        family, type, proto, canonname, sockaddr = \
            socket.getaddrinfo(self.host, self.port, socket.AF_INET, 
                socket.SOCK_STREAM)[0]
        self.socket = socket.socket(family, type, proto)
        self.socket.connect(sockaddr)

    def write(self, request):
        self.socket.send(request)

    def read(self, bufsize=4096):
        return self.socket.recv(bufsize)

    def close(self):
        self.socket.close()
