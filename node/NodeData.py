# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

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
     