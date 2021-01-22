#!/usr/bin/env python3

'''
Author: Blake Rusteberg
Assignment: #02
'''
import sys, socket, ipaddress, time

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
RECEIVER_PORT = int(sys.argv[3])

setupRdy = True
playRdy = False
pauseRdy = False
teardownRdy = False

SETUP = 'SETUP'
PLAY = 'PLAY'
PAUSE = 'PAUSE'
TEARDOWN = 'TEARDOWN'
RTSP = 'RTSP/2.0'

fileName = 'default.wav'
cseq_num = 0

request = ' '

if RECEIVER_PORT == SERVER_PORT:
	print(f"Port Numbers cannot be on the same port!!")
elif SERVER_PORT < 0 or SERVER_PORT > 65535:
	print(f"That is not a valid port number. Try Again!!")
elif RECEIVER_PORT < 0 or RECEIVER_PORT > 65535:
	print(f"That is not a valid port number. Try Again!!")
else:
	print(f"Port numbers are valid.")

try:
	socket.inet_aton(SERVER_IP)
except ValueError:
	print(f"address/netmask is invalid: {SERVER_IP}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to Server
try: 
    s.connect((SERVER_IP, SERVER_PORT))
    print("Success!!")
except ConnectionRefusedError: 

    print(f"There was an error connecting to the ip {SERVER_IP} on port {SERVER_PORT}.")
    sys.exit(1) 

s.send(bytes(str(RECEIVER_PORT), "utf-8"))

while True:

	print(end='\n')
	reqCmd = input()


	if reqCmd == "":
		print(f"S --> C: Invalid Command!!")

	elif reqCmd == SETUP and setupRdy == True:
		setupRdy = False
		teardownRdy = True
		playRdy = True

		cseq_num = 1
		reqCmd = "SETUP " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + "/" + fileName + " "\
		+ RTSP + "\n\t" + " CSeq: " + str(cseq_num) + " \n\t"\
		+ " Transport: UDP;unicast;dest_addr\":" + str(RECEIVER_PORT) + "\""
		s.send(bytes(reqCmd, "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"S --> C: {server_response}")

	elif reqCmd == PLAY and playRdy == True:
		playRdy = False
		pauseRdy = True
		teardownRdy = True

		cseq_num += 1
		reqCmd = "PLAY " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + " " + RTSP + "\n\t" + " CSeq: " + str(cseq_num)
		s.send(bytes(reqCmd, "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"S --> C: {server_response}")


	elif reqCmd == PAUSE and pauseRdy == True:
		playRdy = True
		pauseRdy = False
		cseq_num += 1
		reqCmd = "PAUSE " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + " " + RTSP + "\n\t" + " CSeq: " + str(cseq_num)

		s.send(bytes(reqCmd, "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"S --> C: {server_response}")

	elif reqCmd == TEARDOWN and teardownRdy == True:

		cseq_num += 1
		reqCmd = "TEARDOWN " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + " " + RTSP + "\n\t" + " CSeq: " + str(cseq_num)

		s.send(bytes(reqCmd, "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"S --> C: {server_response}")
		time.sleep(2)
		sys.exit()

	else:

		s.send(bytes(reqCmd , "utf-8"))
		server_response = str(s.recv(1024), "utf-8")
		print(f"S --> C: {server_response}")


s.close()