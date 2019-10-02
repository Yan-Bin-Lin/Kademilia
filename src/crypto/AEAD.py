# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class AEAD():
    '''Authenticated encryption with associated data (AEAD)'''
    def __init__(self, key = None, nonce = os.urandom(12)):
        self.key = key
        self.nonce = nonce
        self.aead = ChaCha20Poly1305(self.key) if key != None else None
        self.hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        
    
    def _methodinit(self, key = None):
        '''initial for encrypt and decrypt'''
        if key != None:
            self.key = key
        if self.aead == None:
            self.aead = ChaCha20Poly1305(self.key)
    
    
    # encrypt data    
    def encrypt(self, msg, nonce=None, *, key = None):
        self._methodinit(key = key)
        if nonce == None:
            self.NewNonce()
            return self.aead.encrypt(self.nonce, msg.encode(encoding='utf-8')), self.nonce
        else:
            return self.aead.encrypt(nonce, msg.encode(encoding='utf-8')), self.nonce
        
    
    # decrypt chiper text
    def decrypt(self, ct, nonce=None, *, key = None):
        self._methodinit(key = key)
        if nonce == None:
            self.NewNonce()
            return self.aead.encrypt(self.nonce, ct).decode(encoding='utf-8')
        else:
            return self.aead.encrypt(nonce, ct).decode(encoding='utf-8')
    
    
    # don't reuse nonce
    def NewNonce(self):
        self.nonce = hash.update(self.nonce).finalize()


    def NewKey(self, key):
        self.key = key

            
    def GetKey(self):
        return self.key

    
    def GetNonce(self):
        return self.nonce
