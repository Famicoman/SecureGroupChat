all:
	chmod +x cliserv.py
	openssl genrsa 1024 > key
	openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert
	
server:
	./cliserv.py s

client:
	./cliserv.py c

generate:
	./keymaker.py $1

clean:
	rm key
	rm cert
