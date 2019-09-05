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

class RSA(asycalgori):
    def __init__(self, SaveKeyPath = None):
        super()
        if SaveKeyPath == None:
            self.NewKey()
        else:
            self.LoadKey(SaveKeyPath)
        
        
    # create new RSA KEY
    def NewKey(self):
        self.PrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self._CreatePublicKey()


    # use private to sign data
    def sign(self, message):
        return self.PrivateKey.sign(
                    message.encode(encoding='utf_8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
        
            
    # use "others" public key to vertify data            
    def verify(self, public_key, signature, message):
        try:
            public_key.verify(
                signature,
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
    
        
    
    # use "others" public key to encrypt data      
    def encrypt(self, public_key, message):
        return public_key.encrypt(
                    message.encode(encoding='utf_8'),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

    
    # use private key to decrypt data
    def decrypt(self, ciphertext):
        return self.PrivateKey.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode(encoding='utf_8')

    
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