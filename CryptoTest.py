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
from cryptography.hazmat.backends import default_backend

if __name__ == '__main__':
    
    alice = RSA()
    bob = RSA()
    
    alice_byte_RSA_publickey = alice.DumpPublicKey()
    alice_RSA_publickey = bob.LoadPublicKey(alice_byte_RSA_publickey)
    print(alice.PublicKey.public_numbers())
    print(alice_RSA_publickey.public_numbers())
    
    aliceDH = DH()
    print(aliceDH.GetShareKey())    
    print(type(DH()) is DH)
    alice_byte_DH_publickey = aliceDH.DumpPublicKey()
    alice_sign = alice.sign(alice_byte_DH_publickey)
    print(bob.verify(alice_RSA_publickey, alice_sign, alice_byte_DH_publickey))
    
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
    print(len(bobDH.GetShareKey()))
    
    Alice = AEAD()
    Alice.NewKey(aliceDH.GetShareKey())
    ct = Alice.encrypt('This is Alice')
    Bob = AEAD()
    Bob.NewKey(bobDH.GetShareKey())
    print(Bob.decrypt(*ct))