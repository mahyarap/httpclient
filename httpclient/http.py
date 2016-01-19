from httpclient.connection import Connection


class HttpMsg(object):
    """
    A base class for an HTTP message.

    :param startln: An HTTP start line. Must be ASCII.
    :param headers: A dictionary of HTTP headers. Must be ASCII.
    :param body: An HTTP body. Can be of any format.
    """
    def __init__(self, startln='', headers={}, body=None):
        self.startln = startln
        self.headers = headers
        self.body = body

    @property
    def body(self):
        return str(self.__body, encoding='UTF-8')

    @body.setter
    def body(self, body):
        self.__body = body

    def __str__(self):
        headers = ''
        for k, v in self.headers.items():
            headers += '{0}: {1}\n'.format(k, v)

        msg = self.startln + '\n' + headers
        return msg


class HttpRequest(HttpMsg):
    """
    A representation of an HTTP request.

    :param url: A URL.
    :param method: An HTTP verb. Must be ASCII.
    :param headers: A dictionary of HTTP headers. Must be ASCII.
    :param body: An HTTP body. Can be of any format.
    """
    def __init__(self, url, method='GET', headers={}, body=None):
        self.method = method
        host, resource = HttpRequest._parse_url(url)
        self.host = host
        self.resource = resource
        startln = method + ' ' + resource + ' ' + 'HTTP/1.1'
        for key in headers:
            if key.lower() == 'host':
                break
        else:
            headers['HOST'] = host
        super().__init__(startln, headers, body)

    @staticmethod
    def _parse_url(url):
        parsed_url = []
        if url.startswith('http://'):
            parsed_url = url[7:].split('/', maxsplit=1)
        else:
            parsed_url = url.split('/', maxsplit=1)

        host = parsed_url[0]
        resource = '/'
        if len(parsed_url) == 2:
            resource = '/' + parsed_url[1]

        return host, resource

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        assert method.upper() in ('GET', 'POST', 'PUT', 'DELETE',
            'HEAD', 'TRACE', 'OPTIONS'), 'Invalid request method'
        self.__method = method

    def build(self):
        request_line = ' '.join([self.method,
                                self.resource,
                                'HTTP/1.1',
                                '\r\n'])

        headers = ''
        for k, v in self.headers.items():
            headers += '{0}: {1}\r\n'.format(k, v)
        headers += '\r\n'

        request = request_line + headers
        return bytes(request, 'UTF-8')

    def send(self):
        conn = Connection(self.host)
        conn.establish()
        request = self.build()
        conn.write(request)
        response = conn.read()
        conn.close()
        return HttpResponse(response)


class HttpResponse(HttpMsg):
    """
    A representation of an HTTP response.

    :param: An HTTP response.
    """
    def __init__(self, response):
        startln, headers, body = HttpResponse.parse_response(response)
        self.version, self.status, self.status_msg = startln.split()
        super().__init__(startln, headers, body)

    @staticmethod
    def parse_response(response):
        CR = 13
        LF = 10
        for i, _ in enumerate(response):
            if response[i] == CR and response[i+1] == LF:
                break
        # Without newline at the end
        startln = response[:i].decode()

        for j, _ in enumerate(response[i+1:], start=i):
            if response[j] == CR and response[j+1] == LF:
                if response[j+2] == CR and response[j+3] == LF:
                    break
        raw_headers = response[i+2:j].decode()
        headers = {}
        for line in raw_headers.split('\r\n'):
            k, v = line.split(':', maxsplit=1)
            headers[k] = v.strip()

        body = response[j+4:]
        return startln, headers, body
