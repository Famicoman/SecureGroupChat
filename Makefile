all:
	chmod +x cliserv.py
	chmod +x keymaker.py
	openssl genrsa 4096 > key
	openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert
	
server:
	./cliserv.py s mike 2 luke bob

clientluke:
	./cliserv.py c luke mike

clientbob:
	./cliserv.py c bob mike

generate:
	./keymaker.py mike
	./keymaker.py luke
	./keymaker.py bob

clean:
	rm key
	rm cert
