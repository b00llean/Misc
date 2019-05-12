#!/usr/bin/env python3
#

import sys
import socket


def reverse_lookup(ip=None):
    if ip:
        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
            return hostname
        except:
            pass
    return []


def main():
    ipaddr='192.168.10.170'
    print(f'{ipaddr},{reverse_lookup(ipaddr)}')
    sys.exit(0)

main()