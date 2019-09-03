# -*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
import threading

from .client import Client
from .server import Server


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
    
        
    def _request(self, ConnectIP, msg):        
        result = self.clients[ConnectIP].request(msg)    
        if result == 'ERROR':
            del self.clients[ConnectIP]
            #do something...
        
        
    def _CheckClient(self, ConnectIP, port):
        if ConnectIP not in self.clients:
            self.clients[ConnectIP] = Client(ConnectIP, port)
      
      
    # send message to other IP    
    def send(self, ConnectIP, port, msg):
        self._CheckClient(ConnectIP, port)
        threading._start_new_thread(self._request, (ConnectIP, msg))                 

            

        
        