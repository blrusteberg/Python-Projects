=====================================================================
FILE: README.txt

Author: Blake Rusteberg

Programming Assignment #2
=====================================================================

FILES: Project2_Server
		-> makefile
		-> server.py
		-> serverBackup.py
       Project2_Client
      		-> makefile
		-> controller.py
		-> receiver.py 

Python3 and above must be downloaded to run these 3 files!!

1) In terminal type 'make' in the same folder the server.py
   In terminal type 'make' in the same folder the controller.py and receiver.py

2) In the server terminal and locate the server.py 
   To run Type "./server.py  (1-65535)" and this gives you your IP address

3) Open another terminal and locate the receiver.py 
   To run Type "./receiver.py  (1-65535)" something different than the server port

4) Open another terminal and locate the controller.py
   To run Type "./controller.py <server-ip> <server-port> <receiver-port>" 

NOTE - 

SERVER - to close CTRL-Z

Controller - only uses 4 commands SETUP, PLAY, PAUSE, TEARDOWN

Receiver - only receives data

MORE NOTES - I added another server backup folder because the server won't run on a local machine with the clients on local machines it will only run if (controller and client) and (server) are on seperate machines. Some IP error I could not fix. Also the audio file will stream all the way through but will have static if paused. 

The Pause and Play will work eventually if typed in the Controller.


