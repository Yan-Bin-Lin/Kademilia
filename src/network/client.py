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
    
    
    # re connect to server
    def ReConnect(self):
        # create a client socket and connect to server
        self._connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set connect time limit
        self._connect.settimeout(self.wait)
        self._connect.connect(self.address)
        '''
        try:
            self._connect.connect(self.address)
        except:
            # connect fail
            self._connect = None
        '''
        
    
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
        time.sleep(self.wait)       
        try:
            response = self._connect.recv(1024)
        except:
            # response time out
            response = None
            print('client fail to get response')
        else:
            print('client success to get response')
            # success get response
            response = response.decode('utf-8')      
            #self._connect.sendall(f'receive the request of respond data, data = {response}'.encode('utf-8'))
        return response
    
    
    '''
    send message to other node that don't need to respond in a few time, ex. ping,...  
    no blocking    
    '''
    def send(self, msg):
        self._connect.sendall(msg.encode('utf-8'))