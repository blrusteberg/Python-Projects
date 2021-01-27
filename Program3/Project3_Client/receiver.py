#!/usr/bin/env python3

'''
Author: Blake Rusteberg
Assignment: #02
'''
import sys, socket, subprocess, time
from threading import Thread
import threading

RECEIVER_IP = socket.gethostbyname(socket.gethostname())
RECEIVER_PORT = int(sys.argv[1])
print(RECEIVER_IP)

newFile = "new.wav"
buffer_size = 100000
packet_size = 0
first_payload_recv = 1
first_pause = False
single_payload = bytes()
final_payload = bytes()
setThread_1 = threading.Event()
setThread_2 = threading.Event()
setThread_1.clear()
setThread_2.clear()

seqNum = 0

def aplay_command(newFile, setThread_1): 
	time.sleep(4)
	cmd = 'aplay -f cd ' + newFile
	return_value = subprocess.call(cmd, shell=True)
	print("return_value:", return_value)

	setThread_1.set()
	setThread_2.clear()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to Port
try: 
    s.bind((RECEIVER_IP, RECEIVER_PORT))
    print("The Receiver is Ready to Receive!!")
except ConnectionRefusedError: 

    print(f"There was an error binding to the port {RECEIVER_PORT}.")
    sys.exit(1) 
	
try:
    newfile = open(newFile, "wb")
except:
    print("file open error")

while True:
	#print(end='\n')
	header_num = ""
	data, serverAddresss = s.recvfrom(60)

	if setThread_1.isSet() == True:
		# delete all contents in the file
		setThread_1.clear()
		setThread_2.set()
		newfile.truncate(0)
		newfile.close()
		
		newfile = open(newFile, "wb")
		
	if data[:].decode("utf-8", errors="ignore") == "TEARDOWN":
		cmd = 'rm ' + newFile
		return_value = subprocess.call(cmd, shell=True)
		print(f"Receiver is exiting gracefully!")
		time.sleep(2)
		sys.exit()

	if data[:].decode("utf-8", errors="ignore") == "END":
		break

	num = data[:].decode("utf-8", errors="ignore")
	for char in num:
		if char == ".":
			break
		header_num += char
 

	seqNum += 1
	
	new_header_length = len(header_num)
	decoded_packet = data[new_header_length+4:]	

	single_payload = decoded_packet

	packet_size += 80

	if seqNum % 1000 == 0:
		print(end='\n')
		print(f"Message Received from Server: {data} ")
	
	newfile.write(single_payload)

	if packet_size == buffer_size:
		
		packet_size = 0

		if first_payload_recv == 1:
			first_payload_recv = 0
			Thread(target=aplay_command, args=(newFile, setThread_1)).start()

		if setThread_2.isSet() == True:
			print("----------------------------------------------")
			setThread_2.clear()
			Thread(target=aplay_command, args=(newFile, setThread_1)).start()

print(f"Message Received from Server: End of file...")
cmd = 'rm ' + newFile
return_value = subprocess.call(cmd, shell=True)
                                                                                                         
s.close()

newfile.close()