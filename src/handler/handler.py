# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
import ast
import json
from .respond import *

# main handler here
def MainHandle(connect, data, KadeNode):
    print(f'server receive data, data is {data}')
    # change string to dict
    data = json.loads(data)
    instruct = data.get('instruct', None)
    '''
    origin = data.get('origin', None)
    destination = data.get('destination', None)
    path = data.get('data', None)
    '''
    # if condition here
    if instruct[0] == 'TRACE':
        # handle for 'ping' request
        print('Get a ping request, return ok')
        connect.sendall(b'ping ok')
    
    elif instruct[0] == 'GET':
        # handle for get node request
        if instruct[1] == 'node':
            print('Get a GET node request return replyGETNODE')
            ReplyGetNode(data, KadeNode)
    
    elif instruct[0] == 'REPLY':
        # handle for reply node
        if instruct[1] == 'node':
            ReceiveNode(data, KadeNode)

        