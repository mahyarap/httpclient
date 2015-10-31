#!/usr/bin/env python3

import unittest
import argparse
import httpclient.httpclient as httpc

class CommandLineOptionsTest(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()

    def tearDown(self):
        pass

    def test_can_parse_commandline_options(self):
        args = httpc.parse_cmd_options(['http://localhost'])
        self.parser.add_argument('url')
        self.assertEqual(args, 
            self.parser.parse_args(['http://localhost']))


class HttpRequstTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost/hi.txt'
        self.request = httpc.HttpRequest(self.url)

    def tearDown(self):
        pass

    def test_can_create_http_request(self):
        self.request.method = 'GET'
        self.request.header = ''
        self.request.body = ''
        response = self.request.send()
        self.assertEqual(response.text.strip(), 'Hi there!')


if __name__ == '__main__':
    unittest.main()
