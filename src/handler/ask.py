# -*- coding: UTF-8 -*-
'''
Created on 2019年9月9日

@author: danny
'''
import threading 

from ..network.communicate import *
from ..util.web import _DataFill
from ..node.NodeData import NodeData


import logging
logger = logging.getLogger( 'loglog' )

def AskNode(data, type_, connect = None, address = None):
    connect = connect[1] if connect != None else None
    logger.debug(f'AskNode connect type = {type(connect)}, connect is {connect}')
    if type_ == 'request':
        return request(data, connect, address)
    else:
        threading._start_new_thread(send, (data, connect, address))                     
        #send(data, connect, address)
    return None


# connect = (ConnectNode, ConnectSocket)
# instruct = ('GET', 'node', '00000000')
# type_ should be 'request' or 'send'
def Ask(SelfNode, type_, *instruct, connect = None, address = None, data = {}, destination = None, content = ''):
    '''
    send a request to other node
    
    Args:
        SelfNode (dict): the node who send request
        type_ (str): if type_ == 'request' will wait for respond
        connect (tuple): connect instant tuple (ConnectNode, ConnectSocket)
        address (tuple): you should give IP address if you don't give connect
        data: the request data from other node, default = {}
        destination (dict): destination of this request, default = None
        content: the request body
        
    Returns:
        msg respond of other node
    '''
    logger.debug(f"SelfNode = {SelfNode},type_ {type_}, instruct {instruct}, connect {connect},address {address}, data {data} destination {destination}, content {content}")
    # fill data
    data = _DataFill(SelfNode, *instruct, data = data, destination = destination, content = content)
    # send to connect node
    return AskNode(data, type_, connect, address)

'''
# reject the request
def Reject(SelfNode, data):
    data['instruct'].insert(0, 'REJECT')
    address = data['path'][-1]['address']
    data['fail'].append(SelfNode['ID'])
    data = _DataFill(SelfNode, data = data)
    AskNode(data, 'send', None, address)
'''