# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class asycalgori():
    '''
    a class of basic method and attribute for Asymmetric algorithms
    
    Attributes:
        PrivateKey: private key
        PublicKey: public key
    '''
    def __init__(self):
        pass
        
       
    def _CreatePublicKey(self):
        '''generate public key from private key''' 
        self.PublicKey = self.PrivateKey.public_key()
        
         
    def LoadKey(self, SavePath):
        '''load exist binary KEY'''   
        with open(SavePath, "rb") as key_file:
            self.PrivateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )       
        self._CreatePublicKey()
        
        
    def SaveKey(self, SavePath):
        '''make a binary KEY for save'''
        with open(SavePath, 'wb') as file:
            file.write(
                self.PrivateKey.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    #encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
                    encryption_algorithm=serialization.NoEncryption()
                )
            )        
            
    
    def LoadPublicKey(self, public_key_data):
        '''conver byte format public key to public key class'''
        return load_pem_public_key(public_key_data, backend=default_backend())
    
    
    def DumpPublicKey(self):
        '''return a byte public to send'''
        return self.PublicKey.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
               )
        
        
    def GetPrivateKey(self):
        '''return private key class'''
        return self.PrivateKey
    
        
    def GetPublicKey(self):
        '''return public key class'''
        return self.PublicKey