# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
from cryptography.hazmat.primitives import serialization


class NodeData():
    '''
    a NodeData should content IP, PublicKey and ID
    
    Attributes:
        _address (tuple): binding (IPAddress, port)
        _PublicKey: RSA PublicKey for sign
        _ID: Node ID
        
    note:
        you should not change data!!
    '''
    
    #address(IP, port), PublicKey, ID
    def __init__(self, address = None, PublicKey = None, ID = None):
        '''
        Args:
            address (tuple): binding (IPAddress, port)
            PublicKey: RSA PublicKey for sign
            ID: Node ID
        '''
        self._address = address
        self._PublicKey = PublicKey
        self._ID = ID
    
    
    def GetData(self): 
        '''
        return self in "dict" format
        
        Returns:
            {
            'address' : self._address,
            'PublicKey' : self.GetByteStringPubKey(),
            'ID' : self._ID
            }
        '''
        return {
                    'ID' : self._ID,
                    'address' : self._address,
                    'PublicKey' : self.GetByteStringPubKey(),
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
    
    
    def GetByteStringPubKey(self):
        '''convert public key to "string" format if you need to send to other or save at disk'''
        return None if self._PublicKey == None else self._PublicKey.public_bytes(
                                                                                encoding=serialization.Encoding.PEM,
                                                                                format=serialization.PublicFormat.SubjectPublicKeyInfo
                                                                                ).decode("utf-8")