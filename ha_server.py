#!/usr/bin/env python

"""
Sets up a SimpleHTTPServer to return the timestamp of creation.
"""

from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys
import time
from random import uniform
import warnings

class HaRequestHandler(SimpleHTTPRequestHandler):
    """
    Sleeps a random amount of time between 0 and 1 second, then saves the
    current timestamp.
    """
    def __init__(self, *args, **kwargs):
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        global timestamp

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(timestamp))
        self.end_headers()
        self.wfile.write(timestamp)


def main(args):
    global timestamp

    if len(args) != 2:
        raise TypeError("ha_server.py, Invalid arguments, " + str(args))

    port = int(args[1])
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    time.sleep(uniform(0, 1))
    timestamp = str(time.time())
    server = SocketServer.TCPServer(('0.0.0.0', port), HaRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main(sys.argv)

