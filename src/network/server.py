#-*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
import socket
import threading

from ..handler.communicate import writefile
from ..handler.communicate import testwrite
from ..util.web import GetLocalIP
from ..handler.handler import MainHandle


# a server socket class
class Server():
    def __init__(self, ServePort=0):
        #server local IP
        self.LocalIP = GetLocalIP()#self._get_host_ip()
        # 创建一个socket套接字，该套接字还没有建立连接
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定监听端口，这里必须填本机的IP192.168.27.238，localhost和127.0.0.1是本机之间的进程通信使用的
        self.server.bind((self.LocalIP, ServePort)) 
        # 开始监听，并设置最大连接数
        self.server.listen(5)        
        print(self.LocalIP)
        self.receive_data = False
        self.receiver = ''
    
    
    def start(self):
        #start serving
        threading._start_new_thread(self._WaitConnect, ())                     
        
        
    # get the sever socket bindind address    
    def GetAddress(self):
        return self.server.getsockname()

        
    def _communicate(self, connect, host, port):
        while True:
            # 接受客户端的数据
            data = connect.recv(1024)
            MainHandle(data)
            # 下面這一坨讓main handle決定要用哪些function
            '''
            # 如果接受到客户端要quit就结束循环
            if data == b'quit' or data == b'':
                print(b'the client has quit.')
                break
            else:
                # 发送数据给客户端 
                connect.sendall(b'your words has received.')
                print(b'the client say:' + data)
                data = str(data, encoding = "utf-8")
                if data == 'trans':
                    self.transaction = 0
                self.receiver = testwrite(self.receive_data, data,self.receiver,self.transaction)
                if self.receiver == '' and self.transaction >= 0: #改檔名
                    self.transaction = -1
                    self.receive_data = False
                elif self.receiver == '':
                    self.receive_data = False
                elif self.transaction >= 0:
                    self.transaction = self.transaction + 1
                else:
                    self.receive_data = True
            '''
            # 上面這一坨讓main handle決定要用哪些function
            
    def _WaitConnect(self):
        while True:
            print(u'waiting for connect...')
            # 等待连接，一旦有客户端连接后，返回一个建立了连接后的套接字和连接的客户端的IP和端口元组
            connect, (host, port) = self.server.accept()
            print(u'the client %s:%s has connected.' % (host, port))
            threading._start_new_thread(self._communicate, (connect, host, port))        
        
    
