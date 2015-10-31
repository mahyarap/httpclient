#!/usr/bin/env python3

import sys
import argparse
import requests

class HttpRequest(object):
    def __init__(self, url, method='GET', header=None, body=None):
        self.url = url
        self.method = method
        self.header = header
        self.body = body

    def send(self):
        response = requests.get(self.url)
        return response


def parse_cmd_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to send the request to')

    return parser.parse_args(args)

def main():
    args = parse_cmd_options(sys.argv[1:])
    # print('Hello')


if __name__ == '__main__':
    main()
