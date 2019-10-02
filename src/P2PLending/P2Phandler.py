# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
import json

import logging
logger = logging.getLogger( 'loglog' )


def ReplyPostPost(data, KadeNode):
    '''reply to a post request'''
    logger.info(f"node {data['path'][-1]['ID']} send a message to you, the message is: \n\t {data['instruct'][2]}")


def ReplyPostMsg(data, KadeNode):
    '''reply to chat request'''
    logger.info(f"node {data['path'][-1]['ID']} send a message to you, the message is: \n\t {data['instruct'][2]}")


def P2PHandle(connect, data, KadeNode):
    '''
    the extend handler for P2P extnd function

    Args:
        data: the request data from other node
        KadeNode: a KadeNode object who call this function    
    '''
    logger.debug(f'server receive data, data is {data}')
    # change string to dict
    data = json.loads(data)
    instruct = data.get('instruct', None)
    
    # update Kbucket of the last node in path(from_ node)
    KadeNode.update(data['path'][-1])
    if len(data['path']) >= 8:
        return False
    
    if instruct[0] == 'POST':
        # a node send message
        if instruct[1] == 'message':
            ReplyPostMsg(data, KadeNode)
        elif instruct[1] == 'post':
            ReplyPostPost(data, KadeNode)