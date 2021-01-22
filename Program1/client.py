#!/usr/bin/env python3

'''
Author: Blake Rusteberg
Assignment: #01
'''
import sys
import socket
import argparse

parser = argparse.ArgumentParser(description='Requires a Hostname and Port')
parser.add_argument('<server-hostname>', type=str)
parser.add_argument('<server-port>', type=int)
args = parser.parse_args()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

if PORT > 0 and PORT < 65536:
	print(f"Port Number {PORT} is valid.")
else:
	print(f"That is not a valid port number. Try Again!!")
	sys.exit(1)

if HOST[0].isdigit():
   print(f"That is not a valid Hostname. Try Again!!")
   sys.exit(1)
else:
   print(f"Hostname {HOST} is valid.")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Retrieve IP address
try: 
    IP = socket.gethostbyname(HOST) # Find Host name IP address
except socket.gaierror: 
  
    print(f"There was an error resolving the Hostname", end='\n\n')
    sys.exit(1) 

# Connect to Server
try: 
    s.connect((IP, PORT))
except ConnectionRefusedError: 

    print(f"There was an error connecting to the ip {IP} on port {PORT}.")
    sys.exit(1) 

print(f"Success!!", end= '\n\n')
print(f"Say HELO to the SERVER!")
bye_reply = "BYE " + HOST
while True:
	print(end='\n')
	cmd = input()
	if cmd == "":
		print(f"SERVER REPLY -> 500 Syntax Error, Command '' Unrecognized!")
	else:
		s.send(bytes(cmd, "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"SERVER REPLY -> {server_response}")
	if cmd == bye_reply:
		s.close()
		sys.exit()
	