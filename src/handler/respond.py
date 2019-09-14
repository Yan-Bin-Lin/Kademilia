# -*- coding: UTF-8 -*-
'''
Created on 2019年9月6日

@author: danny
'''
import json
from pathlib import Path

from ..network.communicate import *
from ..util.hash import *
from ..util.web import _DataFill
from ..node.NodeData import NodeData
from .ask import Ask, Reject

import logging
logger = logging.getLogger( 'loglog' )
    
# reply to someone send GET node
def ReplyGetNode(data, KadeNode):
    DestinateID = data['destination']['ID']
    SelfNode = KadeNode.NodeData.GetData()
    logger.debug(f'receive a "Get node" request, the receive data is {data}')
    logger.debug(f'self node is {KadeNode.NodeData.GetData()}')
    if SelfNode['ID'] == DestinateID:
        #SendData = _DataFill(SelfNode, 'REPLY', 'node', data = data, destination = SelfNode)
        logger.debug(f'Reply back to origin node, origin address is {data["origin"]["address"]}')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], destination = SelfNode, data = data)
    else:
        KadeNode.LookUp(DestinateID, data)
        

# receive the request node
def ReceiveGetNode(data, KadeNode):
    KadeNode.update(data['destination'])
    logger.info(f'LookUp success!!!!!!!   I find the node {data["destination"]["ID"]}')
    

def _SaveFile(data, KadeNode):
    name = data['content']['FileID'] + '.txt'
    folder = Path(KadeNode.SavePath, 'file')
    folder.mkdir(parents=True, exist_ok=True) 
    file = folder / name
    # save the file in local
    file.write_text(json.dumps(data['content']))
    

def ReplyPostFile(data, KadeNode):
    logger.info('IN ReplyPostFile...')
    SelfNode = KadeNode.NodeData.GetData()
    data['content']['saver'].append([SelfNode, 1])
    _SaveFile(data, KadeNode)
    if len(data['path']) < 7:
        if data['instruct'][2] == SelfNode['ID']:
            data['instruct'][2] = GetHash(SelfNode['ID'])
        KadeNode.UpLoadFile('not need', data)
    else:
        Ask(SelfNode, 'send', 'REPLY', 'postfile', address = data['origin']['address'], destination = SelfNode, data = data)        


#receive the notice of upload file result
def ReceivePostFile(data, KadeNode):
    _SaveFile(data, KadeNode)
    logger.info(f'Update File success!!!!!!!')
    
    
def ReplyGetFile(data, KadeNode):
    SelfNode = KadeNode.NodeData.GetData()
    file = KadeNode.GetFile(data['content']['FileID'], data)
    # if local own target file
    if file != None:
        logger.info('I have the file, give you')
        Ask(SelfNode, 'send', 'REPLY', 'getfile', address = data['origin']['address'], data = data, content = file, 
            destination = SelfNode)

            
def ReceiveGetFile(data, KadeNode):
    _SaveFile(data, KadeNode)
    logger.info(f'Get File success!!!!!!!')
    

def ReplyGetBucket(KadeNode):
    result = []
    for distance, bucket in KadeNode.table.items():
        if KadeNode.table[distance].length() != 0:
            result.extend(KadeNode.table[distance].bucket.values())
    logger.debug(f'IN ReplyGetBucket... result = {result}')
    return json.dumps(result).encode('utf-8') if result != [] else None
    
    
def ReceiveReject(data, KadeNode):
    logger.info('In receive reject...')
    SelfNode = KadeNode.NodeData.GetData()
    FailNode = data['path'].pop()
    logger.debug(f'failnode is {FailNode["ID"]}, and I am node {SelfNode["ID"]}')
    # delete self and it will add back later
    del data['path'][-1]
    logger.debug(f'from now on, the path is {data["path"]}')
    AnotherNode = KadeNode.GetDistanceNode(0, FailNode['ID'], except_ = True)
    logger.debug(f'the another node is {AnotherNode}')
    #if there is another node
    if AnotherNode != None:
        Ask(SelfNode, 'send')
    # if this is not the first node, continue reject
    elif len(data['path']) > 0:
        Reject(SelfNode, data)
    # the request fail
    else:    
        logger.info('oops! the request fail!!!!!!!!!!!')
