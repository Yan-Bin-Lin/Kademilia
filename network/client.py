# -*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
import socket
import time

class Client():
    def __init__(self, ConnectIP, ConnectPort):
        #IP = '192.168.0.7'
        #server local IP
        self.ConnectIP = ConnectIP
        # 创建一个socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 主动去连接局域网内IP为192.168.27.238，端口为6688的进程
        self.client.connect((self.ConnectIP, ConnectPort))
        # no blocking socket
        self.client.setblocking(0)

    
    #client request to server
    def request(self, msg):
        # 发送数据
        self.client.sendall(msg.encode('utf-8'))
        # 接收服务端的反馈数据
        time.sleep(2)
        try:
            self.client.recv(1024)
        except:
            return "ERROR"
        return "OK"
    
    
        
        