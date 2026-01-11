#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
        print("Usage: vrfy.py <username> <target_ip>")
        sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = sys.argv[2]
connect = s.connect((ip,25))

banner = s.recv(1024)

print(banner)

user = (sys.argv[1]).encode()
s.send(b'VRFY ' + user + b'\r\n')
result = s.recv(1024)

print(result)

s.close()
