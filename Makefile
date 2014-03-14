all:
	openssl genrsa 1024 > key
	openssl req -new -x509 -nodes -sha1 -days 365 -key key > cert

clean:
	rm key
	rm cert