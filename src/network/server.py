#-*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
import socket
import threading

from ..handler.communicate import read
from ..handler.communicate import select_mode
from ..handler.communicate import cut_ID
from ..handler.communicate import cut_data
from ..handler.communicate import cut_mode
from ..util.web import GetLocalIP


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
    
    
    def start(self):
        #start serving
        threading._start_new_thread(self._WaitConnect, ())                     
        
        
    # get the sever socket bindind address    
    def GetAddress(self):
        return self.server.getsockname()

        
    def _communicate(self, connect, host, port):
        while True:
            # 接受客户端的数据
            msg = connect.recv(1024)
            # 如果接受到客户端要quit就结束循环
            if msg == b'quit' or msg == b'':
                print(b'the client has quit.')
                break
            else:
                # 发送数据给客户端 
                connect.sendall(b'your words has received.')
                print(b'the client say:' + msg)
                msg = str(msg, encoding = "utf-8")
                if cut_mode(msg) == 0 : 
                    content = read(cut_ID(msg))
                else:
                    select_mode(cut_mode(msg),cut_ID(msg),cut_ID(msg),cut_data(msg))


            
    def _WaitConnect(self):
        while True:
            print(u'waiting for connect...')
            # 等待连接，一旦有客户端连接后，返回一个建立了连接后的套接字和连接的客户端的IP和端口元组
            connect, (host, port) = self.server.accept()
            print(u'the client %s:%s has connected.' % (host, port))
            threading._start_new_thread(self._communicate, (connect, host, port))        

        
    
