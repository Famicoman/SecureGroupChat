ready:
    chmod +x cliserv.py
    chmod +x keymaker.py
    mkdir keys
    openssl genrsa 4096 > keys/mike.priv
    openssl req -new -x509 -nodes -sha1 -days 365 -key keys/mike.priv > keys/mike.cert
    openssl genrsa 4096 > keys/luke.priv
    openssl req -new -x509 -nodes -sha1 -days 365 -key keys/luke.priv > keys/luke.cert
    openssl genrsa 4096 > keys/bob.priv
    openssl req -new -x509 -nodes -sha1 -days 365 -key keys/bob.priv > keys/bob.cert
    cat keys/mike.cert > ca_certs
    cat keys/luke.cert >> ca_certs
    cat keys/bob.cert >> ca_certs
    touch ready
    
server: ready
    ./cliserv.py s mike 31337 2 luke bob

clientluke: ready
    ./cliserv.py c luke 127.0.0.1:31337 mike

clientbob: ready
    ./cliserv.py c bob 127.0.0.1:31337 mike

clean:
    rm -rf keys
    rm ca_certs
    rm ready
