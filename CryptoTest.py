# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
import pickle
import hashlib

from src.util.hash import *
from src.crypto.AEAD import AEAD
from src.crypto.DHKeyExchange import DH
from src.crypto.RSASign import RSA
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    
if __name__ == '__main__':
    
    alice = RSA()
    bob = RSA()
    '''
    alice_byte_RSA_publickey = alice.DumpPublicKey()
    alice_RSA_publickey = bob.LoadPublicKey(alice_byte_RSA_publickey)
    print(alice.PublicKey.public_numbers())
    print(alice_RSA_publickey.public_numbers())
    
    message = 'This is alice'
    alice_sign = alice.sign(message)
    print(bob.verify(alice_RSA_publickey, alice_sign, message))
    '''
    aliceDH = DH()
    alice_byte_DH_publickey = aliceDH.DumpPublicKey()
    alice_DH_publickey = bob.LoadPublicKey(alice_byte_DH_publickey)
    print(aliceDH.PublicKey.public_numbers().y)
    print(alice_DH_publickey.public_numbers().y)
    
    bobDH = DH(alice_DH_publickey)
    bob_byte_DH_publickey = bobDH.DumpPublicKey()
    bob_DH_publickey = alice.LoadPublicKey(bob_byte_DH_publickey)
    print(bobDH.PublicKey.public_numbers().y)
    print(bob_DH_publickey.public_numbers().y)
    
    aliceDH.CreateShareKey(bob_DH_publickey)
    print(aliceDH.GetShareKey())    
    print(bobDH.GetShareKey())
    print(len(bin(bobDH.GetShareKey())))
    
    Alice = AEAD()
    Bob = AEAD()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    '''
    Alice.NewKey(aliceDH.GetShareKey())
    data = 'This is Alice'
    ct = Alice.encrypt(data)
    print(Bob.decrypt(*ct, key = bobDH.GetShareKey()))
    '''
    '''     

    alice = DH()
    
    Bob = DH(alice.GetPublicKey())
    print(Bob.GetShareKey())
    
    alice.CreateShareKey(Bob.GetPublicKey())
    print(alice.GetShareKey())
    '''