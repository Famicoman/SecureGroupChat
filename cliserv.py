#!/usr/bin/env python
# Hybrid Client/Server
# - YOU MUST RUN THESE FOR CERT CREATION -
#
# openssl genrsa 1024 > key
# openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert
#

import random, math
import fractions
import sys               
import socket
import string
import time
import threading
from OpenSSL import SSL

exit=0
client_list={}

class sending(threading.Thread):
	def run(self):
		print "Type to send an excrypted message."
        	data = ""
        	while data.startswith("/q")==False:
            		data = sys.stdin.readline()
			if (sys.argv[1] == "s"):
				for key in client_list:
					client_list[key].write(data)#send(data)
			else:
				clisock.write(data)#send(data) #Send command
		exit = 1
		#clisock.close()
		#self.join()
		
class receiving(threading.Thread):
	def run(self):
		while exit==0:
            		data = clisock.read()#repr(clisock.recv(65535)) #clisock.recv(1024)
			print data#.replace('\r','').replace('\n','') #Print message from server
		clisock.close()
		#self.join()

class servreceiving(threading.Thread):

	def __init__(self, address, connection):
		self.address = address
		self.connection = connection
		threading.Thread.__init__(self)
	
	def run(self):
		while exit==0:
			data = repr(self.connection.recv(65535))#(1024)
			print data #Print message from server
			for key in client_list:
				client_list[key].write(data)#send(data)
		self.join()
				
class newconnection(threading.Thread):
	 def run(self):
		print "Server listening for connections"
		while 1:
			connection, address = srvsock.accept()
			print "[NEW CLIENT CONNECTED]"
			client_list[address] = connection
			servrec = servreceiving(address,connection)
			servrec.start()

		
# ./securegroupchat s
if (sys.argv[1] == "s"):
	#Make socket
	srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	
	### SERVER SSL ###
	context = SSL.Context(SSL.SSLv3_METHOD)
	context.use_privatekey_file('key')
	context.use_certificate_file('cert')
	srvsock = SSL.Connection(context, srvsock)
	##################

	srvsock.bind( ('', 31337)) 
	srvsock.listen( 5 )
	
	n = newconnection()
	n.start()
	s = sending()
	s.start()
	
#./securegroupchat c $serveraddress
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



