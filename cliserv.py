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
srvsock.bind( ("127.0.0.1", 31337)) 
srvsock.listen( 5 )
clisock, (remhost, remport) = srvsock.accept()

exit=0

class sending(threading.Thread):
    def run(self):
		print "type to send an excrypted message."
        send = ""
        while send.startswith("/q")==False:
            send= sys.stdin.readline()
            clisock.send(send) #Send command
        exit = 1
		self.join()

class receiving(threading.Thread):

	def __init__(self, address, connection):
		self.address = address
		self.connection = connection
		threading.Thread.__init__(self)
		
    def run(self):
		global address = self.address
		global connection = self.connection
	
        rec = ['0','0']
        while exit==0:
            data = eval(clisock.recv(1024))
            print data #Print message from server
		self.join()
				
class newconnection(threading.Thread):
	global client_list = dict()
	while 1:
		connection, address = srvsock.accept()
		client_list[connection] = address
		thread = receiving(address,connection)
		thread.start()

n = newconnection()
n.start()
s = sending()
s.start()


