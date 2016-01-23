#!/usr/bin/env python3

import sys
import argparse

from httpclient.http import HttpRequest


__version__ = '0.1.0'


def parse_cmd_options(args):
    """Parse the command line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to send the request to')
    parser.add_argument('-m', '--method',
                        default='GET',
                        help='HTTP request method')
    parser.add_argument('-H', '--header',
                        action='append',
                        default=[],
                        help='HTTP headers')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='be verbose')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__),
                        help='show version and exit')
    return parser.parse_args(args)


def main():
    args = parse_cmd_options(sys.argv[1:])
    if args.url:
        headers = {}
        for header in args.header:
            key, val = header.split(':', maxsplit=1)
            headers[key.strip()] = val.strip()

        request = HttpRequest(args.url, method=args.method,
                              headers=headers)
        if args.verbose:
            print(str(request))
        response = request.send()
        print(response.body, end='')

    return 0


if __name__ == '__main__':
    sys.exit(main())
