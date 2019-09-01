'''
Created on 2019年9月1日

@author: danny
'''
import threading

from .client import Client
from .server import Server


# handle server and client connect
class Connect():
    def __init__(self, port):
        self.server = Server(port)
        self.clients = {}
    
    
    def run(self):
        self.server.start()
      
        
    def _request(self, IP, msg):        
        result = self.clients[IP].request(msg)    
        if result == 'ERROR':
            del self.client[IP]
            #do something...
        
        
    def _CheckClient(self, IP):
        if IP not in self.clients:
            self.clients[IP] = Client(IP)
      
      
    # send message to other IP    
    def send(self, IP, msg):
        self._CheckClient(IP)
        threading._start_new_thread(self._request, (IP, msg))                 

            

        
        