# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class asycalgori():
    def __init__(self):
        self.PrivateKey
        self.PublicKey
        
        
    # generate public key from private key    
    def _CreatePublicKey(self):
        self.PublicKey = self.PrivateKey.public_key()
        
        
    # load exist KEY    
    def LoadKey(self, SavePath):
        with open(SavePath, "rb") as key_file:
            self.PrivateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )       
        
        
    # make a binary KEY for save
    def SaveKey(self, SavePath):
        with open(SavePath, 'wb') as file:
            file.write(
                self.PrivateKey.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    #encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
                    encryption_algorithm=serialization.NoEncryption()
                )
            )        
            
        
    # return private key
    def GetPrivateKey(self):
        return self.PrivateKey
    
        
    # return public key
    def GetPublicKey(self):
        return self.PublicKey