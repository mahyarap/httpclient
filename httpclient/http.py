from httpclient.connection import Connection

class HttpRequest(object):
    def __init__(self, url, method='GET', headers={}, body=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    @staticmethod
    def parse_url(url):
        if url.startswith('http://'):
            url = url[7:].split('/', maxsplit=1)
        else:
            url = url.split('/', maxsplit=1)
        host = url[0]
        resource = '/'
        if len(url) == 2:
            resource = '/' + url[1]
        return host, resource

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        assert method.upper() in ['GET', 'POST', 'PUT', 'DELELTE', 
            'HEAD', 'TRACE', 'OPTIONS'], 'Invalid request method'
        self.__method = method

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = {}
        host, resource = HttpRequest.parse_url(self.url)
        if not ('HOST' in headers or 'host' in headers):
            self.__headers['HOST'] = host

    def build(self):
        host, resource = HttpRequest.parse_url(self.url)
        request_line = (self.method + 
            ' ' + resource + 
            ' ' + 'HTTP/1.1' + 
            '\r\n')

        host = 'HOST: {0}\r\n'.format(host)

        headers = ''
        for k, v in self.headers.items():
            headers += '{0}: {1}\r\n'.format(k, v)
        headers += '\r\n'

        header_section = request_line + host + headers

        # body = bytes(body, 'UTF-8')

        request = bytes(header_section, 'UTF-8')
        return request

    def send(self):
        host, resource = HttpRequest.parse_url(self.url)
        conn = Connection(host)
        conn.establish()
        request = self.build()
        conn.write(request)
        response = conn.read()
        conn.close()
        http_resp = HttpResponse(response)
        return http_resp


class HttpResponse(object):
    def __init__(self, response):
        self.start_line, self.headers, self.body = \
            HttpResponse.parse_response(response)

    @staticmethod
    def parse_response(response):
        CR = 13
        LF = 10
        for i, _ in enumerate(response):
            if response[i] == CR and response[i+1] == LF:
                break
        # Without newline at the end
        start_line = response[:i]

        for j, _ in enumerate(response[i+1:], start=i):
            if response[j] == CR and response[j+1] == LF:
                if response[j+2] == CR and response[j+3] == LF:
                    break
        headers = response[i+2:j]

        body = response[j+4:]
        return start_line, headers, body

    @property
    def start_line(self):
        return self.__start_line

    @start_line.setter
    def start_line(self, start_line):
        self.__start_line = start_line.decode()

    @property
    def status(self):
        return self.start_line.split(' ')[1]

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = {}
        headers = headers.decode()
        for line in headers.split('\r\n'):
            k, v = line.split(':', maxsplit=1)
            self.__headers[k] = v

    def __str__(self):
        headers = ''
        for k, v in self.headers.items():
            headers += '{0}: {1}\n'.format(k, v)

        response = self.start_line + '\n\n' + headers
        return response
