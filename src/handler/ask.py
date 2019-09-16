# -*- coding: UTF-8 -*-
'''
Created on 2019年9月9日

@author: danny
'''
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
        send(data, connect, address)
    return None


# connect = (ConnectNode, ConnectSocket)
# instruct = ('GET', 'node', '00000000')
# type_ should be 'request' or 'send'
def Ask(SelfNode, type_, *instruct, connect = None, address = None, data = {}, destination = None, content = ''):
    # fill data
    data = _DataFill(SelfNode, *instruct, data = data, destination = destination, content = content)
    # send to connect node
    return AskNode(data, type_, connect, address)


# reject the request
def Reject(SelfNode, data):
    data['instruct'].insert(0, 'REJECT')
    address = data['path'][-1]['address']
    data['fail'].append(SelfNode['ID'])
    data = _DataFill(SelfNode, data = data)
    AskNode(data, 'send', None, address)
