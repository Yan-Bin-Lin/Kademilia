# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
from cryptography.hazmat.primitives import serialization

class NodeData():
    '''
    a NodeData shoule content IP, PublicKey and ID
    !!you should not change data!!
    '''
    #address(IP, port), PublicKey, ID
    def __init__(self, address, PublicKey, ID):
        self._address = address
        self._PublicKey = PublicKey
        self._ID = ID
    
    
    # return self id dict format
    def GetData(self): 
        return {
                    'address' : self._address,
                    'PublicKey' : self.GetBytePubKey(),
                    'ID' : self._ID
                }
    
        
    def GetID(self):
        return self._ID

    
    def GetIP(self):
        return self._address[0]
    
    
    def GetPort(self):
        return self._address[1]
    
    
    def GetAddress(self):
        return self._address
    
    
    def GetPublicKey(self):
        return self._PublicKey
    
    
    # convert public key to byte format if you need to send to other or save at disk
    def GetBytePubKey(self):
        return self._PublicKey.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
                )