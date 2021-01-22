#!/usr/bin/env python3

'''
Author: Blake Rusteberg
Assignment: #01
'''
import sys
import socket
import argparse
import math
import threading

parser = argparse.ArgumentParser(description='Requires a Hostname and Port')
parser.add_argument('<server-port>', type=int)
args = parser.parse_args()


HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
PORT = int(sys.argv[1])

if PORT > 0 and PORT < 65536:
	print(f"Port Number {PORT} is valid.")
else:
	print(f"That is not a valid port number. Try Again!!")
	sys.exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((HOST_IP, PORT))
	print(f"Listening for networks.", end='\n\n')
except Exception as e:
	raise SystemExit(f"The server could not bind the server on the host {HOST_NAME} to port: {PORT} because {e}", end='\n')



def CALC_CUBE_VOL(conn, data, cube_RDY):
	dec = data[4:].decode("utf-8")			# take away the area part so the format is "x x x"
	vol_arr = dec.split(' ')				# put in array [x, x, x]
	

	if len(vol_arr) == 3 and vol_arr[0].isdigit() and vol_arr[1].isdigit() and vol_arr[2].isdigit():
		l = int(vol_arr[0])
		w = int(vol_arr[1])
		h = int(vol_arr[2])
		volume = l*w*h
		conn.send(bytes(f"250 {volume}", "utf-8"))

		cube_RDY = False
		return cube_RDY

	elif len(vol_arr) < 3 or len(vol_arr) > 3:
		conn.send(bytes(f"501 Syntax Error in Parameters: VOL <l><w><h>", "utf-8"))
		cube_RDY = True
		return cube_RDY 

	elif vol_arr[0].isdigit() is False or vol_arr[1].isdigit() is False or vol_arr[2].isdigit() is False:
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))
		cube_RDY = True
		return cube_RDY 



def CALC_CUBE_AREA(conn, data, cube_RDY):
	dec = data[5:].decode("utf-8")			# take away the area part so the format is "x x x"
	area_arr = dec.split(' ')				# put in array [x, x, x]
	
					
	if len(area_arr) == 3 and area_arr[0].isdigit() and area_arr[1].isdigit() and area_arr[2].isdigit():
		l = int(area_arr[0])
		w = int(area_arr[1])
		h = int(area_arr[2])
		area = 2*((l*w) + (h*w) + (h*l))
		conn.send(bytes(f"250 {area}", "utf-8"))

		cube_RDY = False
		return cube_RDY

	elif len(area_arr) < 3 or len(area_arr) > 3:
		conn.send(bytes(f"501 Syntax Error in Parameters: AREA <l><w><h>", "utf-8"))
		cube_RDY = True
		return cube_RDY 

	elif area_arr[0].isdigit() is False or area_arr[1].isdigit() is False or area_arr[2].isdigit() is False:
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))
		cube_RDY = True
		return cube_RDY 



def CALC_SPHERE_VOL(conn, data, sphere_RDY):
	dec = data[4:].decode("utf-8")			# take away the area part so the format is "x x x"
	vol_arr = dec.split(' ')				# put in array [x, x, x]
	

	if len(vol_arr) == 1 and vol_arr[0].isdigit():
		r = float(vol_arr[0])
		volume = (4.0/3.0)*math.pi*r**3.0
		conn.send(bytes(f"250 {volume}", "utf-8"))

		sphere_RDY = False
		return sphere_RDY 

	elif len(vol_arr) != 1:
		conn.send(bytes(f"501 Syntax Error in Parameters: VOL <r>", "utf-8"))
		sphere_RDY = True
		return sphere_RDY 

	elif vol_arr[0].isdigit() is False or vol_arr[0] == " ":
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))
		sphere_RDY = True
		return sphere_RDY 


def CALC_SPHERE_RAD(conn, data, sphere_RDY):
	dec = data[4:].decode("utf-8")			# take away the area part so the format is "x x x"
	rad_arr = dec.split(' ')				# put in array [x, x, x]
	

	if len(rad_arr) == 1 and rad_arr[0].isdigit():
		A = float(rad_arr[0])
		radius = (1.0/2.0)*math.sqrt(A/math.pi)
		conn.send(bytes(f"250 {radius}", "utf-8"))

		sphere_RDY = False
		return sphere_RDY 
			
	elif len(rad_arr) != 1:
		conn.send(bytes(f"501 Syntax Error in Parameters: RAD <A>", "utf-8"))
		sphere_RDY = True
		return sphere_RDY 
	elif rad_arr[0].isdigit() is False or rad_arr[0] == " ":
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))	
		sphere_RDY = True
		return sphere_RDY 



def CALC_CONE_VOL(conn, data, cone_RDY):
	dec = data[4:].decode("utf-8")			# take away the area part so the format is "x x x"
	vol_arr = dec.split(' ')				# put in array [x, x, x]
	

	if len(vol_arr) == 2 and vol_arr[0].isdigit() and vol_arr[1].isdigit():
		r = float(vol_arr[0])
		h = float(vol_arr[1])
		volume = math.pi*r*math.sqrt((r**2) + (h**2))
		conn.send(bytes(f"250 {volume}", "utf-8"))

		cone_RDY = False
		return cone_RDY
			
	elif len(vol_arr) < 2 or len(vol_arr) > 2:
		conn.send(bytes(f"501 Syntax Error in Parameters: VOL <r><h>", "utf-8"))
		cone_RDY = True
		return cone_RDY
			
	elif vol_arr[0].isdigit() is False or vol_arr[1].isdigit() is False:
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))	
		cone_RDY = True
		return cone_RDY
			



def CALC_CONE_HGH(conn, data, cone_RDY):
	dec = data[4:].decode("utf-8")			# take away the area part so the format is "x x x"
	hgh_arr = dec.split(' ')				# put in array [x, x, x]
	print(hgh_arr)

	if len(hgh_arr) == 2 and hgh_arr[0].isdigit() and hgh_arr[1].isdigit():
		A = float(hgh_arr[0])
		r = float(hgh_arr[1])
		height = (3.0/A)*math.pi*r**2.0
		conn.send(bytes(f"250 {height}", "utf-8"))
		
		cone_RDY = False
		return cone_RDY
			
	elif len(hgh_arr) < 2 or len(hgh_arr) > 2:
		conn.send(bytes(f"501 Syntax Error in Parameters: HGH <A><r>", "utf-8"))
		cone_RDY = True
		return cone_RDY
			
	elif hgh_arr[0].isdigit() is False or hgh_arr[1].isdigit() is False:
		conn.send(bytes(f"501 Syntax Error in Parameters: All arguments must be digits.", "utf-8"))
		cone_RDY = True
		return cone_RDY
			


def HELP_COMMAND(conn):
	conn.send(bytes(f"200 These are the list of commands used on this server.", "utf-8"))
	conn.send(bytes(f'\n', "utf-8"))
	conn.send(bytes(f"HELO   - The first command that is used to greet the server. Unrecognized after the first greeting. <\n", "utf-8"))
	conn.send(bytes(f"HELP   - A list of commands the server interacts with.\n", "utf-8"))
	conn.send(bytes(f"CUBE   - Used to calculate the area calulation AREA <l><w><h> and the volume calulation VOL <l><w><h>.\n", "utf-8"))
	conn.send(bytes(f"SPHERE - Used to calculate the volume calulation VOL <r> and the radius calulation RAD <A>.\n", "utf-8"))
	conn.send(bytes(f"CONE   - Used to calulate the height calulation HGH <A><r> and volume calulation VOL <r><h>.\n", "utf-8"))
	conn.send(bytes(f"AREA   - Can only be used after the CUBE command. Formula: 2(lw + hw + hl).\n", "utf-8"))
	conn.send(bytes(f"VOL    - Can only be used after the CUBE, SPHERE, or CONE command, CUBE: lwh, SPHERE: (4/3)πr^3, CONE: πr√(r^2 + h^2).\n", "utf-8"))
	conn.send(bytes(f"RAD    - Can only be used after the SPHERE command, Formula: (1/2)√(A)/(π). \n", "utf-8"))
	conn.send(bytes(f"HGH    - Can only be used after the CONE command. Formula: (3/A)/(πr^2).\n", "utf-8"))
	conn.send(bytes(f"BYE    - Exit the server gracefully... BYE <hostname>\n", "utf-8"))
	conn.send(bytes(f"Note - Client must enter a valid calulation command to get another shape ready. EX: CONE then HGH. <r>\n", "utf-8"))



def BYE_COMMAND(conn, client_ip):
	conn.send(bytes(f"200 BYE {client_ip}", "utf-8"))
	print(f"Server Closing for client {client_ip}.")
	sys.exit()



def UNREC_COMMAND(conn, data):
	decode_com = data[:].decode("utf-8") 
	conn.send(bytes(f"500 Syntax Error, Command '{decode_com}' Unrecognized! \n", "utf-8"))
	conn.send(bytes(f"Use the 'HELP' Command for the list of Commands.", "utf-8"))



def new_client(conn, addr):
	client_ip = addr[0]
	client_port = addr[1]

	cube_RDY = False
	sphere_RDY = False
	cone_RDY = False

	command_arr = ['HELO', 'HELP', 'CUBE', 'SPHERE', 'CONE', 'BYE', 'AREA', 'RAD', 'HGH', 'VOL']

	print(f"\nA new Client has connected!!") 
	print(f"Success!!") 
	print(f"IP: {client_ip}") 
	print(f"Port: {client_port}", end='\n\n')

	# HELO command
	while True:
		
		data = conn.recv(1024)
	  
		if data[:4].decode("utf-8") == "HELO" and data[5:].decode("utf-8") == HOST_NAME:
			conn.send(bytes(f"200 HELO {addr[0]}", "utf-8"))
			print(f"The client {addr[0]} said: HELO", end='\n')
			command_arr.pop(0)
			break
		elif data[:4].decode("utf-8") == "HELO":
			conn.send(bytes(f"Try using the server's host name {HOST_NAME} after HELO.", "utf-8"))
		else:
			decode_com = data[:].decode("utf-8")
			conn.send(bytes(f"500 Syntax Error, Command '{decode_com}' Unrecognized!", "utf-8"))

	while True:
		data = conn.recv(1024)

		check_command = data[:6].decode("utf-8")		
		check_command_arr = check_command.split()		#puts the first command before the space in an array
		
		if check_command_arr[0] in command_arr:			#if that command is in the array allow it to go through

			# HELP command
			if data[:4].decode("utf-8") == "HELP" and cube_RDY is False and sphere_RDY is False and cone_RDY is False:
				HELP_COMMAND(conn)
			# CUBE 
			elif data[:4].decode("utf-8") == "CUBE" and sphere_RDY is False and cone_RDY is False:
				conn.send(bytes(f"210 CUBE ready!", "utf-8"))
				cube_RDY = True
			elif cube_RDY is True:
				# VOLUME for CUBE
				if data[:3].decode("utf-8") == "VOL":
					cube_RDY = CALC_CUBE_VOL(conn, data, cube_RDY)

				# AREA for CUBE
				elif data[:4].decode("utf-8") == "AREA":
					cube_RDY = CALC_CUBE_AREA(conn, data, cube_RDY)

				#HELP for CUBE
				elif data[:4].decode("utf-8") == "HELP":
					HELP_COMMAND(conn)

				#BYE for CUBE
				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") == HOST_NAME:
					BYE_COMMAND(conn, client_ip)

				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") != HOST_NAME:
					conn.send(bytes(f"Try using the server's host name {HOST_NAME} after the command BYE.", "utf-8"))

				#RAD error for CUBE
				elif data[:3].decode("utf-8") == "RAD":
					conn.send(bytes(f"503 Bad Sequence of Commands: SPHERE before RAD", "utf-8"))

				#HGH error for CUBE
				elif data[:3].decode("utf-8") == "HGH":
					conn.send(bytes(f"503 Bad Sequence of Commands: CONE before HGH", "utf-8"))

				#command Unrecognized
				else:
					decode_com = data[:].decode("utf-8")
					conn.send(bytes(f"500 Syntax Error, Command '{decode_com}' Unrecognized! \n", "utf-8"))
					conn.send(bytes(f"Use the 'HELP' Command for the list of Commands.", "utf-8"))

			#SPHERE
			elif data[:6].decode("utf-8") == "SPHERE" and sphere_RDY is False and cone_RDY is False:
				conn.send(bytes(f"220 SPHERE ready!", "utf-8"))
				sphere_RDY = True
			elif sphere_RDY is True:
				#VOLUME for SPHERE
				if data[:3].decode("utf-8") == "VOL":
					sphere_RDY = CALC_SPHERE_VOL(conn, data, sphere_RDY)

				#RADIUS for SPHERE
				elif data[:3].decode("utf-8") == "RAD":
					sphere_RDY = CALC_SPHERE_RAD(conn, data, sphere_RDY)

				#HELP for SPHERE
				elif data[:4].decode("utf-8") == "HELP":
					HELP_COMMAND(conn)

				#BYE for SPHERE
				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") == HOST_NAME:
					BYE_COMMAND(conn, client_ip)

				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") != HOST_NAME:
					conn.send(bytes(f"Try using the server's host name {HOST_NAME} after the command BYE.", "utf-8"))

				#AREA error for CUBE
				elif data[:4].decode("utf-8") == "AREA":
					conn.send(bytes(f"503 Bad Sequence of Commands: CUBE before AREA", "utf-8"))

				#HGH error for CONE
				elif data[:3].decode("utf-8") == "HGH":
					conn.send(bytes(f"503 Bad Sequence of Commands: CONE before HGH", "utf-8"))

				#Command Unrecognized
				else:
					UNREC_COMMAND(conn, data)

			#CONE
			elif data[:4].decode("utf-8") == "CONE" and sphere_RDY is False and cube_RDY is False:
				conn.send(bytes(f"230 CONE ready!", "utf-8"))
				cone_RDY = True
			elif cone_RDY is True:
				#VOLUME for CONE
				if data[:3].decode("utf-8") == "VOL":
					cone_RDY = CALC_CONE_VOL(conn, data, cone_RDY)

				#HEIGHT for CONE
				elif data[:3].decode("utf-8") == "HGH":
					cone_RDY = CALC_CONE_HGH(conn, data, cone_RDY)

				#HELP for CONE
				elif data[:4].decode("utf-8") == "HELP":
					HELP_COMMAND(conn)

				#BYE for CONE
				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") == HOST_NAME:
					BYE_COMMAND(conn, client_ip)

				elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") != HOST_NAME:
					conn.send(bytes(f"Try using the server's host name {HOST_NAME} after the command BYE.", "utf-8"))

				#AREA error for CUBE
				elif data[:4].decode("utf-8") == "AREA":
					conn.send(bytes(f"503 Bad Sequence of Commands: CUBE before AREA", "utf-8"))

				#RAD error for SPHERE
				elif data[:3].decode("utf-8") == "RAD":
					conn.send(bytes(f"503 Bad Sequence of Commands: SPHERE before RAD", "utf-8"))

				#Command Unrecognized
				else:
					UNREC_COMMAND(conn, data)

			elif data[:4].decode("utf-8") == "AREA" and cube_RDY is False:
				conn.send(bytes(f"503 Bad Sequence of Commands: CUBE before AREA", "utf-8"))

			elif data[:3].decode("utf-8") == "RAD" and sphere_RDY is False:
				conn.send(bytes(f"503 Bad Sequence of Commands: SPHERE before RAD", "utf-8"))

			elif data[:3].decode("utf-8") == "HGH" and cone_RDY is False:
				conn.send(bytes(f"503 Bad Sequence of Commands: CONE before HGH", "utf-8"))

			elif data[:3].decode("utf-8") == "VOL" and cone_RDY is False and sphere_RDY is False and sphere_RDY is False:
				conn.send(bytes(f"\n503 Bad Sequence of Commands: CUBE before VOL\n", "utf-8"))
				conn.send(bytes(f"503 Bad Sequence of Commands: SPHERE before VOL\n", "utf-8"))
				conn.send(bytes(f"503 Bad Sequence of Commands: CONE before VOL", "utf-8"))


			elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") == HOST_NAME:
				BYE_COMMAND(conn, client_ip)
			
			elif data[:3].decode("utf-8") == "BYE" and data[4:].decode("utf-8") != HOST_NAME:
				conn.send(bytes(f"Try using the server's host name {HOST_NAME} after the command BYE.", "utf-8"))
			else:
				UNREC_COMMAND(conn, data)
		else:
			UNREC_COMMAND(conn, data)

		data_to_server = data[:].decode("utf-8")
		print(f"The client {addr[0]} said: {data_to_server}")

	client.close()

while True:
	try:
		s.listen(5)
		conn, addr = s.accept()
		threading._start_new_thread(new_client, (conn, addr))
	except KeyboardInterrupt:
		print(f"The server is shutting down gracefully!")
		sys.exit()

s.close()
