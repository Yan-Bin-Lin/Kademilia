# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

#Authenticated encryption with associated data (AEAD)
class AEAD():
    def __init__(self, key, nonce = os.urandom(12)):
        self.key = key
        self.nonce = nonce
        self.chacha = ChaCha20Poly1305(self.key)
        self.hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        
    
    # encrypt data    
    def encrypt(self, msg, nonce=None):
        if nonce == None:
            return self.chacha.encrypt(self.nonce, msg.encode(encoding='utf-8'))
        else:
            return self.chacha.encrypt(nonce, msg.encode(encoding='utf-8'))            
        
    
    # decrypt chiper text
    def decrypt(self, ct, nonce=None):
        if nonce == None:
            return self.chacha.encrypt(self.nonce, ct).decode(encoding='utf-8')
        else:
            return self.chacha.encrypt(nonce, ct).decode(encoding='utf-8')            
    
    
    # don't reuse nonce
    def NewNonce(self):
        self.nonce = hash.update(self.nonce).finalize()

        
    def GetKey(self):
        return self.key

    
    def GetNonce(self):
        return self.nonce
