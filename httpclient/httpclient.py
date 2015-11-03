#!/usr/bin/env python3

import sys
import argparse
from httpclient.http import HttpRequest

def parse_cmd_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to send the request to')
    parser.add_argument('-m', '--method',
        default='GET',
        help='HTTP request method')
    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='be verbose')
    return parser.parse_args(args)


def main(argv):
    args = parse_cmd_options(argv[1:])
    if args.url:
        request = HttpRequest(args.url, args.method)
        if args.verbose:
            print(str(request))
        response = request.send()
        print(str(response))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
