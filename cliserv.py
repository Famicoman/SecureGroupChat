#!/usr/bin/env python
# Hybrid Client/Server
#
# - YOU MUST RUN THESE FOR CERT/KEY CREATION -
#
# openssl genrsa 4096 > key
# openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert
#

import sys               
import socket
import string
import threading
import time
import ssl
import os
from OpenSSL import SSL
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import *
from base64 import b64decode

def decrypt(private_key, package):
        rsakey = RSA.importKey(private_key)
        #rsakey = PKCS1_OAEP.new(rsakey)
        decrypted = rsakey.decrypt(b64decode(package))
        return decrypted

def encrypt(public_key, message):
        rsakey = RSA.importKey(public_key)
        #rsakey = PKCS1_OAEP(rsakey)
        encrypted = rsakey.encrypt(message,32)
        return encrypted[0].encode('base64')

exit = 0
client_list= dict()
users = dict()
privkey = ""
serverkey = ""

def openUsers():
	numusers = int(sys.argv[4])
	print "[NUMBER OF USERS: "+str(numusers)+"]"
	num = 5+numusers
	for x in range(5,num):
		if len(sys.argv[x])>0:
			if os.path.isfile('keys/'+sys.argv[x]+'.pub'):
				print "[LOADED USER "+sys.argv[x]+"]"
				data = open('keys/'+sys.argv[x]+'.pub').read()
				data = data.strip()
				users[sys.argv[x]] = data
			else:
				print "[FAILED TO LOAD USER "+sys.argv[x]+"]"
				return 0
		else:
			return 0
	return 1

class sending(threading.Thread):
	def run(self):
		global exit
		global client_list
		global users
		global serverkey
		print "[TYPE TO SEND MESSAGE (/q TO QUIT)]"
        	data = ""
        	while data.startswith("/q")==False:
            		data = sys.stdin.readline()
			olddata = data
			if (sys.argv[1] == "s"):
				for key in client_list:
					thisdata = encrypt(users[key],"<"+sys.argv[2]+"> "+data)
					client_list[key].write(thisdata)
			else:
				data = encrypt(serverkey,data)
				clisock.write(data) # Send command
			data = olddata
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
		global privkey
		while exit==0:
            		data = clisock.read()
                        data = data.replace("\\n",'')
			data = decrypt(privkey,data)
			data = data.strip()
			if data.find("/q")!=-1:#startswith("/q"):
				exit = 1;
			else:
				print data

class servreceiving(threading.Thread):

	def __init__(self, user, connection):
		self.user = user
		self.connection = connection
		threading.Thread.__init__(self)
	
	def run(self):
		global exit
		global client_list
		global users
		global privkey
		while 1:
			data = repr(self.connection.recv(65535))
			data = data[1:-3]
                        data = data.replace("\\n",'')
			data = decrypt(privkey, data)
			#data = data[1:-2]
			if data.find("/q")!=-1:#startswith("/q"):
				self.connection.write(encrypt(users[self.user],"/q"))
				del client_list[self.user]
				print "[A CLIENT HAS EXITED]"
				for key in client_list:
                                        if key!=self.user:
						data = encrypt(users[key],"[A CLIENT HAS EXITED]")
                                                client_list[key].write(data)
				break
			else:
				output = data[0:-1]
				print "<"+self.user+"> "+output # Print message from server
				for key in client_list:
					if key!=self.user:
						thisdata = encrypt(users[key], "<"+self.user+"> "+data)
						client_list[key].write(thisdata)
				
class newconnection(threading.Thread):
	 def run(self):
		global exit
		global client_list
		print "[SERVER LISTENING FOR CONNECTIONS]"
		while exit==0:
			connection, address = srvsock.accept()
			print "[USER ATTEMPTING TO CONNECT]"
			#timestamp = time.time()
			data = repr(connection.recv(65535))
			data = data[1:-3]
			data = data.replace("\\n",'')
			data = decrypt(privkey,data)
			if data in users:
				print "[USER "+data+" IDENTIFIED & CONNECTED]"
				#print "[NEW CLIENT CONNECTED]"
				#client_list[str(address)+"-"+str(timestamp)] = connection
				client_list[data] = connection
				#servrec = servreceiving(str(address)+"-"+str(timestamp),connection)
				servrec = servreceiving(data,connection)
				servrec.start()

privkey = open('keys/'+sys.argv[2]+'.priv').read()		

# ./cliserv.py s $name $port $numusers $user1 $user2 ...
if (sys.argv[1] == "s"):
	# Make socket
	srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	
	### SERVER SSL ###
	context = SSL.Context(SSL.SSLv3_METHOD)
	context.use_privatekey_file('key')
	context.use_certificate_file('cert')
	srvsock = SSL.Connection(context, srvsock)
	##################

	openUsers()

	srvsock.bind( ('', int(sys.argv[3]))) 
	srvsock.listen( 5 )
	
	n = newconnection()
	n.start()
	s = sending()
	s.start()

	s.join()
	srvsock.close()
	
#./cliserv.py c $name $address:port $serveruser
if (sys.argv[1] == "c"):
	clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	if sys.argv[3].find(":") == -1:
		clisock.connect( (sys.argv[3], 31337) )
	else:
		addressport = sys.argv[3].split(":")
		clisock.connect( (addressport[0], int(addressport[1])) )

	### CLIENT SSL ###
	#clisock = socket.ssl(clisock)
	clisock = ssl.wrap_socket(clisock, ca_certs="cert", cert_reqs=ssl.CERT_REQUIRED)
	##################

	serverkey = open('keys/'+sys.argv[4]+'.pub').read()

	data = encrypt(serverkey,sys.argv[2])
	clisock.write(data)

	print "[CONNECTED TO SERVER]"	
	r = receiving()
	r.start()
	s = sending()
	s.start()
	
	s.join()
	r.join()



