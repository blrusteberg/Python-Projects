#!/usr/bin/env python3

'''
Author: Blake Rusteberg
Assignment: #03
'''
import sys, socket, ipaddress, time, ssl, base64, hashlib

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
RECEIVER_PORT = int(sys.argv[3])

setupRdy = True
playRdy = False
pauseRdy = False
teardownRdy = False
authorizeRdy = False
logInSuccessRdy = False

SETUP = 'SETUP'
PLAY = 'PLAY'
PAUSE = 'PAUSE'
TEARDOWN = 'TEARDOWN'
RTSP = 'RTSP/2.0'

fileName = 'default.wav'
server_cert = 'CS447.cert'
server_sni_hostname = 'blake.com'

cseq_num = 0

request = ' '

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(server_cert)

if RECEIVER_PORT == SERVER_PORT :
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

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = context.wrap_socket(conn, server_side=False, server_hostname=server_sni_hostname)
# Connect to Server
try: 
    s.connect((SERVER_IP, SERVER_PORT))
    print("SSL established. Peer: {}".format(s.getpeercert()))
except ConnectionRefusedError: 

    print(f"There was an error connecting to the ip {SERVER_IP} on port {SERVER_PORT}.")
    sys.exit(1) 


s.send(bytes(str(RECEIVER_PORT), "utf-8"))

while True:

	if authorizeRdy == False and setupRdy == True:
		print("\nEnter the 'SETUP' to continue:")

	if authorizeRdy == True:
		while True:
			user = ""
			password = ""
			print("\n\nPlease enter a username and password to login into the secure server.")
			print("Usernames or Passwords with spaces will be concatenated!!\n")

			while user == "":
				user = input("Username: ")
				user = user.replace(" ", "")

			while password == "":
				password = input("Password: ")
				password = password.replace(" ", "")

			credStr = user + ":" + password

			pass64 = base64.b64encode(credStr.encode('ascii'))

			cseq_num += 1
			reqCmd = "SETUP " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + "/" + fileName + " "\
			+ RTSP + "\n\t" + " CSeq: " + str(cseq_num) + " \n\t"\
			+ " Transport: UDP;unicast;dest_addr\":" + str(RECEIVER_PORT) + "\"\n\t"\
			+ " Authorization: Basic " + str(pass64.decode("utf-8"))
		
			s.send(bytes(reqCmd, "utf-8"))
			server_response = str(s.recv(1024), "utf-8")
			split = server_response.split(" ")
		
			print(f"S --> C: {server_response}")

			if split[1] == "403":
				continue

			elif split[1] == "410":
				time.sleep(2)
				s.send(bytes("Client disconnected...\n\n", "utf-8"))
				sys.exit()

			elif split[1] == "200":
				logInSuccessRdy = True
				break

	if logInSuccessRdy == True:
		break

	print(end='\n')
	reqCmd = input()

	if reqCmd == "":
		print(f"S --> C: Invalid Command!!")

	elif reqCmd == SETUP and authorizeRdy == False and setupRdy == True:
		setupRdy = False
		authorizeRdy = True
		teardownRdy = True

		cseq_num = 1
		reqCmd = "SETUP " + "rtsp://" + socket.gethostbyaddr(SERVER_IP)[0] + "/" + fileName + " "\
		+ RTSP + "\n\t" + " CSeq: " + str(cseq_num) + " \n\t"\
		+ " Transport: UDP;unicast;dest_addr\":" + str(RECEIVER_PORT) + "\""

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

print("-" * 60)
playRdy = True
while True:

	print(end='\n')
	reqCmd = input()

	if reqCmd == "":

		reqCmd = " "
		s.send(bytes(reqCmd , "utf-8"))
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