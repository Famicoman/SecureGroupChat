#!/usr/bin/env python

import sys
from Crypto.PublicKey import RSA
from Crypto import Random

def generate_RSA( bits):
	random_generator = Random.new().read
	key = RSA.generate(bits, random_generator)
	public_key = key.publickey().exportKey("PEM") 
	private_key = key.exportKey("PEM") 
	return public_key, private_key

if (len(sys.argv[1])>0):
	pub,priv = generate_RSA(2048)
	f = open('keys/'+sys.argv[1]+'.pub','w+')
	f.write(pub)
	f.close()

	f = open('keys/'+sys.argv[1]+'.priv','w+')
        f.write(priv)
        f.close()

