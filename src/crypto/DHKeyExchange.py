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

'''
# Generate some parameters. These can be reused.
default_parameters = dh.generate_parameters(generator=2, key_size=512,
                                    backend=default_backend())
'''
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2

params_numbers = dh.DHParameterNumbers(p,g)
default_parameters = params_numbers.parameters(default_backend())

class DH(asycalgori):
    def __init__(self, PublicKey = None, parameters = default_parameters):
        # Generate a private key for use in the exchange.
        self.PrivateKey = parameters.generate_private_key()
        # create public key
        self._CreatePublicKey()

        if PublicKey != None:
            self.CreateShareKey(PublicKey)
        else:
            self.ShareKey = None
    
    
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