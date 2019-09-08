# -*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
import threading

from .client import Client
from .server import Server
from ..network import communicate

# handle server and client connect
class Connect():
    def __init__(self, ServePort=0):
        self.server = Server(ServePort)
        self.clients = {}
    
    
    def run(self):
        self.server.start()
      
        
    # return server binding address
    def GetServeAddress(self):
        return self.server.GetAddress() 
    
        
    def _CheckConnect(self, ID, connect, address, wait = 5):
        self.clients[ID] = communicate.link(address, connect, wait)
        
      
    # send message to other node that don't need to respond in a few time
    # no blocking
    #def send(msg, peer, connect = None, address = None, wait = 5):
    def send(self, msg, node, connect):
        ID = node.GetID()
        self._CheckClient(ID, connect)
        communicate.send(msg, self.clients[ID], node.GetAddress())
            
    
    # send message to other node that need to respond in a few time, ex. ping...   
    # blocking        
    def request(self, address, msg):  
        self._CheckClient(address)      
        result = self.clients[address].request(msg)
        
    
    # send message to other node that need to respond in a few time, ex. ping...   
    # blocking
    def CheckResponse(self, address):
        if self.clients[address].RequestStatus:
            return True
        else:
            del self.clients[address]
            return False