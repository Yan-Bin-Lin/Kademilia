# -*- coding: UTF-8 -*-
'''
Created on 2019/9/1

@author: danny
'''
import socket
import time


class Client():
    def __init__(self, address, wait = 5):
        self.address = tuple(address) 
        self.wait = wait
        self.ReConnect()
        # response of last request
        self.RequestStatus = False
        
        
    # createe a new connect
    def NewConnect(self):
        pass
    
    
    def _WaitResponse(self, type_ = 'request'):
        now = time.time()
        ConnectStatus = False
        while time.time() - now < self.wait and ConnectStatus == False:
            try:
                if type_ == 'connect':
                    self._connect.connect(self.address)
                else:
                    response = self._connect.recv(10240)
            except:
                pass
            else:
                ConnectStatus = True
        if type_ != 'connect':
            return response.decode('utf-8') if ConnectStatus else None
        return self._connect if ConnectStatus else None
                
                    
    # re connect to server
    def ReConnect(self):
        # create a client socket and connect to server
        self._connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set connect time limit
        self._connect.settimeout(self.wait)
        print(f'start to connect {self.address}')
        return self._WaitResponse('connect')
        
    
    def GetConnect(self):
        return self._connect
    
    
    '''
    send message to other node that need to respond in a few time, ex. ping,...  
    blocking
    return response(response text)
    '''
    def request(self, msg):
        # 发送数据
        self._connect.sendall(msg.encode('utf-8'))
        return self._WaitResponse()
    
    
    '''
    send message to other node that don't need to respond in a few time, ex. ping,...  
    no blocking    
    '''
    def send(self, msg):
        self._connect.sendall(msg.encode('utf-8'))