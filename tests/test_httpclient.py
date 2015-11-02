#!/usr/bin/env python3

import unittest
import argparse
from httpclient.httpclient import HttpRequest

class HttpRequstTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_url(self):
        host, resource = HttpRequest.parse_url('127.0.0.1')
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(resource, '/')
        host, resource = HttpRequest.parse_url('http://localhost')
        self.assertEqual(host, 'localhost')
        self.assertEqual(resource, '/')
        host, resource = HttpRequest.parse_url('http://localhost/foo/bar')
        self.assertEqual(host, 'localhost')
        self.assertEqual(resource, '/foo/bar')

    def test_send_http_request_options(self):
        request = HttpRequest('http://localhost')
        request.method = 'OPTIONS'
        response = request.send()
        self.assertEqual(response.status, '200')

    def test_send_http_request_get(self):
        request = HttpRequest('http://localhost')
        request.method = 'GET'
        response = request.send()
        self.assertEqual(response.status, '200')
        self.assertTrue(response.body)


if __name__ == '__main__':
    unittest.main()
