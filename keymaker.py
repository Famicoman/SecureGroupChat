#!/usr/bin/env python

import sys
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import *
from base64 import b64decode


def generate_RSA( bits):
	random_generator = Random.new().read
	key = RSA.generate(bits, random_generator)
	public_key = key.publickey().exportKey("PEM") 
	private_key = key.exportKey("PEM") 
	return public_key, private_key

def decrypt(private_key, package):
   	rsakey = RSA.importKey(private_key) 
	#rsakey = PKCS1_OAEP.new(rsakey) 
	decrypted = rsakey.decrypt(b64decode(package)) 
	return decrypted

def encrypt(public_key, message):
	rsakey = RSA.importKey(public_key)
	#rsakey = PKCS1_OAEP(rsakey)
	encrypted = rsakey.encrypt(message,32)
	print encrypted
	return encrypted[0].encode('base64')

if (len(sys.argv[1])>0):
	pub,priv = generate_RSA(4096)
	f = open('keys/'+sys.argv[1]+'.pub','w+')
	f.write(pub)
	f.close()

	f = open('keys/'+sys.argv[1]+'.priv','w+')
        f.write(priv)
        f.close()

	print "Testing keypair..."
	print "Encrypting: \'hello world\'"
	encrypted = encrypt(pub, "hello world")
	decrypted = decrypt(priv, encrypted)
	print "Decrypted text: \'"+decrypted+"\'"

