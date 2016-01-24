#!/usr/bin/env python3

import sys
import io
import unittest
from httpclient.httpclient import main


def fake_main(args):
    args.insert(0, 'httpclient')
    sys.argv = args
    main()


class HttpClientTest(unittest.TestCase):
    def setUp(self):
        self.out = io.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.out

    def tearDown(self):
        self.out.close()
        sys.stdout = self.saved_stdout

    def test_verbose_http_options(self):
        args = ['-vm', 'OPTIONS', 'localhost']
        fake_main(args)
        self.assertIn('OPTIONS /', self.out.getvalue())
        self.assertIn('200 OK', self.out.getvalue())


if __name__ == '__main__':
    unittest.main()
