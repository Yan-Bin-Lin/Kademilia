# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
from .asycrypto import asycalgori

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Generate some parameters. These can be reused.
default_parameters = dh.generate_parameters(generator=2, key_size=2048,
                                    backend=default_backend())

class DH(asycalgori):
    def __init__(self, PublicKey = None, parameters = default_parameters):
        # Generate a private key for use in the exchange.
        self.PrivateKey = parameters.generate_private_key()
        # create public key
        self._CreatePublicKey()
        
        if PublicKey != None:
            self.CreateShareKey(PublicKey)
        
    
    # use other public key to generate share key
    def CreateShareKey(self, OtherPublicKey):
        # Perform key derivation.
        self.ShareKey = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(self.PrivateKey.exchange(OtherPublicKey))
        
        
    def GetShareKey(self):
        return self.ShareKey