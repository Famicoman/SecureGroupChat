#!/usr/bin/env python
# Hybrid Client/Server
#
# - YOU MUST RUN THESE FOR CERT/KEY CREATION -
#
# openssl genrsa 1024 > key
# openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert
#

import sys               
import socket
import string
import threading
import time
from OpenSSL import SSL

exit = 0
client_list= dict()

class sending(threading.Thread):
	def run(self):
		global exit
		global client_list
		print "[TYPE TO SEND MESSAGE (/q TO QUIT)]"
        	data = ""
        	while data.startswith("/q")==False:
            		data = sys.stdin.readline()
			if (sys.argv[1] == "s"):
				for key in client_list:
					client_list[key].write(data)
			else:
				clisock.write(data) # Send command
		exit = 1
		print "[YOU HAVE EXITED]"
		if (sys.argv[1] == "s"):
			for key in client_list:
                        	client_list[key].close()
			srvsock.close() # This causes a crash on the server 
		
		
class receiving(threading.Thread):
	def run(self):
		global exit
		global client_list
		while exit==0:
            		data = clisock.read()
			data = data[0:-1]
			if data.startswith("/q"):
				exit = 1;
			else:
				print data

class servreceiving(threading.Thread):

	def __init__(self, address, connection):
		self.address = address
		self.connection = connection
		threading.Thread.__init__(self)
	
	def run(self):
		global exit
		global client_list
		while 1:
			data = repr(self.connection.recv(65535))
			data = data[1:-2]
			if data.startswith("/q"):
				self.connection.write("/q/")
				del client_list[self.address]
				print "[A CLIENT HAS EXITED]"
				for key in client_list:
                                        if key!=self.address:
                                                client_list[key].write("[A CLIENT HAS EXITED]/")
				break
			else:
				output = data[0:-1]
				print output # Print message from server
				for key in client_list:
					if key!=self.address:
						client_list[key].write(data)
				
class newconnection(threading.Thread):
	 def run(self):
		global exit
		global client_list
		print "[SERVER LISTENING FOR CONNECTIONS]"
		while exit==0:
			connection, address = srvsock.accept()
			timestamp = time.time()
			print "[NEW CLIENT CONNECTED]"
			client_list[str(address)+"-"+str(timestamp)] = connection
			servrec = servreceiving(str(address)+"-"+str(timestamp),connection)
			servrec.start()
		
# ./cliserv.py s
if (sys.argv[1] == "s"):
	# Make socket
	srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	
	### SERVER SSL ###
	context = SSL.Context(SSL.SSLv3_METHOD)
	context.use_privatekey_file('key')
	context.use_certificate_file('cert')
	srvsock = SSL.Connection(context, srvsock)
	##################

	srvsock.bind( ('127.0.0.1', 31337)) 
	srvsock.listen( 5 )
	
	n = newconnection()
	n.start()
	s = sending()
	s.start()

	s.join()
	srvsock.close()
	
#./cliserv.py c $serveraddress
if (sys.argv[1] == "c"):
	clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	clisock.connect( ("127.0.0.1", 31337) )

	### CLIENT SSL ###
	clisock = socket.ssl(clisock)
	##################

	print "[CONNECTED TO SERVER]"	
	r = receiving()
	r.start()
	s = sending()
	s.start()
	
	s.join()
	r.join()



