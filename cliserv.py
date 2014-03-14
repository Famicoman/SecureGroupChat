#!/usr/bin/env python
#Hybrid Client/Server
import random, math
import fractions
import sys               
import socket
import string
import time
import threading


#Make socket
srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
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
					client_list[key].send(data)
			else:
				clisock.send(data) #Send command
		exit = 1
		#clisock.close()
		#self.join()
		
class receiving(threading.Thread):
	def run(self):
		while exit==0:
            		data = clisock.recv(1024)
			print data #Print message from server
		clisock.close()
		#self.join()

class servreceiving(threading.Thread):

	def __init__(self, address, connection):
		self.address = address
		self.connection = connection
		threading.Thread.__init__(self)
	
	def run(self):
		while exit==0:
			data = self.connection.recv(1024)
			print data #Print message from server
			for key in client_list:
				client_list[key].send(data)
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
	#srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	srvsock.bind( ("127.0.0.1", 31337)) 
	srvsock.listen( 5 )
	
	n = newconnection()
	n.start()
	s = sending()
	s.start()
	
#./securegroupchat c $serveraddress
if (sys.argv[1] == "c"):
	#clisock, (remhost, remport) = srvsock.accept()
	clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	clisock.connect( ("127.0.0.1", 31337) )
	print "[CONNECTED TO SERVER]"	
	r = receiving()
	r.start()
	s = sending()
	s.start()




