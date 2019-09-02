# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''

from crypto.AEAD import AEAD
from crypto.DHKeyExchange import DH
from crypto.RSASign import RSA
    
if __name__ == '__main__':

    alice = RSA()
    print(alice.PublicKey)
    alice.SaveKey('./test_save')
    alice.LoadKey('./test_save')
    print(alice.PublicKey)
    del alice
    alice = RSA('./test_save')
    
    public_key = alice.GetPublicKey()
    
    
    bob = RSA()
    
    message = 'oh yeah'
    signature = alice.sign(message)
    print(bob.verify(public_key, signature, message))
    
    print(message)
    ciphertext = bob.encrypt(public_key, message)
    print(ciphertext)
    print(alice.decrypt(ciphertext))
    
            

    alice = DH()
    
    Bob = DH(alice.GetPublicKey())
    print(Bob.GetShareKey())
    
    alice.CreateShareKey(Bob.GetPublicKey())
    print(alice.GetShareKey())