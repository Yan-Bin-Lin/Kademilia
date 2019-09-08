# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
from ..network.client import Client
        
    
# create a client socket and connect to server
def link(address, connect, wait):
    # check to create a new client or not
    if connect != None:
        return connect
    # create a new client
    peer = Client(address, wait)
    return peer if peer.GetConnect() != None else None


def _deal(msg, connect, address, wait, instruct):
    print(f'start to try to send data, data = {msg}')
    connect = link(address, connect, wait)
    if connect == None:
        return None
    if instruct == 'request':
        # type = request
        response = connect.request(msg)
        print(f'receive the request of respond data, data = {response}')
        return response, connect
    else:
        # type = send
        connect.send(msg)
        
        
'''
send message to other node that need to respond in a few time, ex. ping,...  
a connect should be a socket that has connect or accept
if connect = None, create a new socket and "address" should be gave
blocking
return response(response text), connect(socket) 
'''
def request(msg, connect = None, address = None, wait = 5):
    return _deal(msg, connect, address, wait, 'request')
    
    
# send message to other node that don't need to respond in a few time
# no blocking    
def send(msg, connect = None, address = None):
    _deal(msg, connect, address, 5, 'send')              
