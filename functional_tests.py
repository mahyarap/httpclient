#!/usr/bin/env python3

import sys
import io
import unittest
import argparse
from httpclient.httpclient import main

class HttpClientTest(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.out

    def tearDown(self):
        self.out.close()
        sys.stdout = self.saved_stdout

    def test_http_options(self):
        args = ['httpclient.py', 'localhost']
        main(args)
        self.assertEqual(self.out.getvalue().strip(), '200')


if __name__ == '__main__':
    unittest.main()
