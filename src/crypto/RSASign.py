# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
from .asycrypto import asycalgori

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import base64

class RSA(asycalgori):
    def __init__(self, SaveKey = None):
        if SaveKey == None:
            self.NewKey()
        else:
            self.LoadBytePublicKey(SaveKey)
        self._CreatePublicKey()
        
        
    def NewKey(self):
        '''create new RSA KEY'''
        self.PrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=512,
            backend=default_backend()
        )


    def sign(self, message):
        '''use private to sign data'''
        message = message.encode(encoding='utf_8') if type(message) != type(b'') else message
        return base64.b64encode(
            self.PrivateKey.sign(
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
            )
        
                      
    def verify(self, public_key, signature, message):
        '''use "others" public key to verify data'''
        message = message.encode(encoding='utf_8') if type(message) != type(b'') else message
        try:
            public_key.verify(
                base64.b64decode(signature),
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        # verify error
        except InvalidSignature:
            return False
        # something error
        except:
            return False
        # verify complete
        else: 
            return True
    
        
    def encrypt(self, public_key, message):
        '''use "others" public key to encrypt data'''
        message = message.encode(encoding='utf_8') if type(message) != type(b'') else message
        return public_key.encrypt(
                    message,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

    
    def decrypt(self, ciphertext):
        '''use private key to decrypt data'''
        return self.PrivateKey.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode(encoding='utf_8')

    
    def LoadBytePublicKey(self, public_pem_data):
        '''load byte sting publickey to a publickey class'''
        return load_pem_public_key(public_pem_data, backend=default_backend())
    '''
    
    if data too big for sign
    
        >>> from cryptography.hazmat.primitives.asymmetric import utils
    >>> chosen_hash = hashes.SHA256()
    >>> hasher = hashes.Hash(chosen_hash, default_backend())
    >>> hasher.update(b"data & ")
    >>> hasher.update(b"more data")
    >>> digest = hasher.finalize()
    >>> sig = private_key.sign(
    ...     digest,
    ...     padding.PSS(
    ...         mgf=padding.MGF1(hashes.SHA256()),
    ...         salt_length=padding.PSS.MAX_LENGTH
    ...     ),
    ...     utils.Prehashed(chosen_hash)
    ... )
    
    if data too big for verify
        >>> chosen_hash = hashes.SHA256()
    >>> hasher = hashes.Hash(chosen_hash, default_backend())
    >>> hasher.update(b"data & ")
    >>> hasher.update(b"more data")
    >>> digest = hasher.finalize()
    >>> public_key.verify(
    ...     sig,
    ...     digest,
    ...     padding.PSS(
    ...         mgf=padding.MGF1(hashes.SHA256()),
    ...         salt_length=padding.PSS.MAX_LENGTH
    ...     ),
    ...     utils.Prehashed(chosen_hash)
    ... )
    '''