# -*- coding: UTF-8 -*-
'''
Created on 2019/9/1

@author: danny
'''
import socket

from ..handler import communicate


class Client():
    def __init__(self, address):
        #IP = '192.168.0.7'
        #server local IP
        self.address  = address 
        self.client = communicate.link(address)
        '''
        # 创建一个socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 主动去连接局域网内IP为192.168.27.238，端口为6688的进程
        self.client.connect(self.address)
        '''
        # response of last request
        self.RequestStatus = False
        
    
    # client request to server for a respond
    # blocking
    def request(self, msg, wait=5):
        return communicate.request(self.client, msg, wait)

