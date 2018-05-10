## This section encrypts text using a stored public key. Will likely move
## from fernet encryption to more web3 compatible

import os
from cryptography.fernet import Fernet

class beacon_fernet_encrypt():
    def __init__(self):
        f=open(os.path.expanduser('~/.beacon_creds/creds'),'r')
        temp=f.read()
        f.close()
        self.beacon_public_key=temp.split('beacon_public_key=')[1].split('\n')[0]
        self.cipher_suite = Fernet(self.beacon_public_key)
    def encrypt_text(self,stringer):
        return self.cipher_suite.encrypt(stringer.encode())

    def decrypt_text(self,stringer):
        return self.cipher_suite.decrypt(stringer.encode())
