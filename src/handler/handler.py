# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
import ast
import json
from .respond import *
from .ask import *
from ..util.web import _DataFill
import logging
logger = logging.getLogger( 'loglog' )

# main handler here
def RespondHandle(connect, data, KadeNode):
    logger.debug(f'server receive data, data is {data}')
    # change string to dict
    data = json.loads(data)
    instruct = data.get('instruct', None)
    
    # update Kbucket
    path = data.get('path', None)
    tmp = {}
    for node in path:
        if node['ID'] not in tmp:
            tmp[node['ID']] = True
            KadeNode.update(node)
    
    # if condition here
    if instruct[0] == 'TRACE':
        # handle for 'ping' request
        logger.debug('Get a ping request, return ok')
        connect.sendall(b'ping ok')
    
    elif instruct[0] == 'GET':
        # handle for get node request
        if instruct[1] == 'node':
            logger.debug('Get a GET node request return replyGETNODE')
            ReplyGetNode(data, KadeNode)
        # handle for get file request
        if instruct[1] == 'file':
            logger.debug('Get a GET file request return replyGETFile')
            ReplyGetFile(data, KadeNode)
        # handle for get bucket request
        if instruct[1] == 'bucket':
            logger.debug('Get a GET file request return replyGETFBUCKET')
            connect.sendall(ReplyGetBucket(KadeNode))
    
    elif instruct[0] == 'REPLY':
        # handle for reply  GET node
        if instruct[1] == 'getnode':
            ReceiveGetNode(data, KadeNode)
        # handle for reply POST file
        if instruct[1] == 'postfile':
            ReceivePostFile(data, KadeNode)
        # handle for reply GET file
        if instruct[1] == 'getfile':
            ReceiveGetFile(data, KadeNode)
    
    elif instruct[0] == 'POST':
        # handle for save a file
        if instruct[1] == 'file':
            ReplyPostFile(data, KadeNode)
            
    elif instruct[0] == 'REJECT':
        # the request has been reject
        ReceiveReject(data, KadeNode)
            
            