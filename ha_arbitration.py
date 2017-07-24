#!/usr/bin/env python

"""
Simple script to query the two namenode ha_servers. Returns True if the current
namenode wins arbitration by having the oldest timestamp.

$ ha_arbitration.py [SERVICE] [NAMESPACE] [NUM_RETRIES]
"""

import requests
import socket
import sys
import time

def main(args):
    if len(args) != 5:
        raise TypeError("ha_arbitration.py, Invalid arguments, " + str(args))

    service, namespace, num_retries, port = args[1], args[2], int(args[3]), args[4]
    localhost_url = "http://localhost:" + port
    min_timestamp = local_timestamp = get_timestamp(localhost_url, num_retries)
    for ipaddr in get_ipaddrs(service, namespace):
        url = "http://" + ipaddr + ":" + port
        timestamp = get_timestamp(url, num_retries)
        min_timestamp = min(timestamp, min_timestamp)

    sys.exit(min_timestamp == local_timestamp)

def get_ipaddrs(service, namespace):
    dns = service.lower() + '.' + namespace.lower()
    ip_list = set()
    ais = socket.getaddrinfo(dns, 0, 0, 0, 0)
    for result in ais:
        ip_list.add(result[-1][0])
    return set(ip_list)

def get_timestamp(url, num_retries):
    while num_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200 and isfloat(response.text):
                return float(response.text)
        except requests.ConnectionError as e:
            print url, e
            time.sleep(1)
        num_retries -= 1
    return sys.maxint

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main(sys.argv)

