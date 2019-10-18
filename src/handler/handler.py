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
from ..util.log import log
logger = log()


def RespondHandle(connect, data, KadeNode):
    '''
    main handler to deal with the receive data
    
    Args:
        data: the request data from other node
        KadeNode: a KadeNode object who call this function
    '''
    # change string to dict
    data = json.loads(data)
    instruct = data.get('instruct', None)

    logger.warning(f'node {KadeNode.ID} 收到 node {data["path"][-1]["ID"]} 的  {instruct} 請求')

    # update Kbucket of the last node in path(from_ node)
    KadeNode.update(data['path'][-1])
    if len(data['path']) >= 8:
        return False

    # if condition here
    if instruct[0] == 'TRACE':
        # handle for 'ping' request
        logger.debug(f'node {KadeNode.ID} 收到 node {data["origin"]["ID"]} 的ping 請求，回傳OK')
        connect.sendall(b'ping ok')
        return True
    
    elif instruct[0] == 'GET':
        # handle for get node request
        if instruct[1] == 'node':
            logger.info(f'node {KadeNode.ID} Get a GET node request from node {data["path"][-1]["ID"]}')
            ReplyGetNode(data, KadeNode)
            return True
        # handle for get file request
        elif instruct[1] == 'file':
            logger.info(f'node {KadeNode.ID} Get a GET file request from node {data["path"][-1]["ID"]}')
            ReplyGetFile(data, KadeNode)
            return True
        # handle for get bucket request
        elif instruct[1] == 'bucket':
            logger.info(f'node {KadeNode.ID} Get a GET bucket request from node {data["path"][-1]["ID"]}')
            connect.sendall(ReplyGetBucket(KadeNode))
            return True
    
    elif instruct[0] == 'REPLY':
        # handle for reply  GET node
        if instruct[1] == 'getnode':
            logger.info(f'node {KadeNode.ID} 的 GET node 請求收到回應了')
            ReceiveGetNode(data, KadeNode)
            return True
        # handle for reply POST file
        elif instruct[1] == 'postfile':
            logger.info(f'node {KadeNode.ID} 的 update file 請求收到回應了')
            ReceivePostFile(data, KadeNode)
            return True
        # handle for reply GET file
        elif instruct[1] == 'getfile':
            logger.info(f'node {KadeNode.ID} 的 GET file 請求收到回應了')
            ReceiveGetFile(data, KadeNode)
            return True
    
    elif instruct[0] == 'POST':
        # handle for save a file
        if instruct[1] == 'file':
            logger.info(f'node {KadeNode.ID} Get a POST file request from node {data["path"][-1]["ID"]}')
            ReplyPostFile(data, KadeNode)
            return True

    logger.info(f'無符合的 KadeNode 內建  handle function ，呼叫P2P擴充function')
    return False

            