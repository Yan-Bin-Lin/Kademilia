# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class AEAD():
    '''Authenticated encryption with associated data (AEAD)'''
    def __init__(self, aad = '0', key = None, nonce = os.urandom(12)):
        self.key = key
        self.nonce = nonce
        self.aad = aad.encode(encoding='utf-8')
        self.aead = AESGCM(self.key) if key != None else None
        #self.hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        
    
    def _methodinit(self, key = None):
        '''initial for encrypt and decrypt'''
        if key != None:
            self.key = key
        if self.aead == None:
            self.aead = AESGCM(self.key)
    
    
    # encrypt data    
    def encrypt(self, msg, nonce=None, *, key = None):
        self._methodinit(key = key)
        if nonce == None:
            self.NewNonce()
            return self.aead.encrypt(self.nonce, msg.encode(encoding='utf-8'), self.aad), self.nonce, self.aad
        else:
            return self.aead.encrypt(nonce, msg.encode(encoding='utf-8'),self.aad), self.nonce, self.aad
        
    
    # decrypt chiper text
    def decrypt(self, ct, nonce=None, aad = '0', *, key = None):
        print(ct)
        print(nonce)
        print(aad)
        self._methodinit(key = key)
        if nonce == None:
            return self.aead.decrypt(self.nonce, ct, aad).decode(encoding='utf-8')
        else:
            return self.aead.decrypt(nonce, ct, aad).decode(encoding='utf-8')
    
    
    # don't reuse nonce
    def NewNonce(self):
        self.nonce = os.urandom(12)


    def NewKey(self, key):
        self.key = key

            
    def GetKey(self):
        return self.key

    
    def GetNonce(self):
        return self.nonce
