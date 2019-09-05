# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
import threading
import time
import socket

# msg, connect(a client socket to send*), wait(wait time), 
# args only exist when connect is None, args[0] sould be an address
#def request(msg, connect = None, *args, wait = 2): 


# create a client socket and connect to server
def link(address, wait = 5):
    # create a new client
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set connect time limit
    peer.settimeout(wait)
    try:
        peer.connect(address)
    except:
        # connect fail
        peer = None
    return peer
    

# send message to other node that need to respond in a few time, ex. ping,...  
# a connect should be a socket that has connect or accept
# if connect = None, create a new socket and "address" should be gave
# blocking
def request(msg, connect = None, address = None, wait = 5):
    if connect == None:
        connect = link(address, wait)
        if connect == None:
            # create socket fail
            print(' create socket fail')
            return None
        
    # 发送数据
    connect.sendall(msg.encode('utf-8'))
    time.sleep(wait)
    try:
        print('try receive..')
        response = connect.recv(1024)
    except:
        response = None
    print('request response = ' + str(response))
    return response
    
    
# send message to other node that don't need to respond in a few time
# no blocking    
def send(msg, connect = None, address = None):
    threading._start_new_thread(request, (msg, connect, address))                 


# test if a node is online
def ping(address):
    print('ping address is ' + str(address))
    return True if request('ping', None, address) != None else False
