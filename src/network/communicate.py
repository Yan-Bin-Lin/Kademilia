# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
from ..network.client import Client

import logging
logger = logging.getLogger( 'loglog' )        


def link(address, connect, wait):
    '''
    create and check a client socket connect to server
    
    Returns:
        client socket if connect success else None
    '''
    # check to create a new client or not
    if connect != None:
        return connect
    # create a new client
    peer = Client(address, wait)
    return peer if peer.GetConnect() != None else None


def _deal(msg, connect, address, wait, instruct):
    logger.debug(f'start to try to send data, data = {msg}')
    connect = link(address, connect, wait)
    logger.debug(f'_deal connect type = {type(connect)}, instruct is {instruct}')
    if connect == None:
        return None
    if instruct == 'request':
        # type = request
        response = connect.request(msg)
        logger.debug(f'receive the request of respond data, data = {response}')
        return response, connect
    else:
        # type = send
        connect.send(msg)
        
        
def request(msg, connect = None, address = None, wait = 5):
    '''
    send message to other node that need to respond in a few time, ex. ping,...  
    
    Args:
        connect: a socket that has connect or accept
        address: if connect = None, create a new socket and "address" should be gave
    
    Note:
        blocking method
        
    Returns:
        tuple: (response text, ConnectSocket) 
    '''    
    return _deal(msg, connect, address, wait, 'request')
        
   
def send(msg, connect = None, address = None):
    '''
    send message to other node that don to respond in a few time 
    
    Args:
        connect: a socket that has connect or accept
        address: if connect = None, create a new socket and "address" should be gave
    
    Note:
        no blocking method 
    ''' 
    _deal(msg, connect, address, 5, 'send')              
