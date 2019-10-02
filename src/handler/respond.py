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
from .ask import Ask #Reject

import logging
logger = logging.getLogger( 'loglog' )
    

def ReplyGetNode(data, KadeNode):
    '''
    reply to GET node request
    '''
    DestinateID = data['destination']['ID']
    SelfNode = KadeNode.NodeData.GetData()
    logger.debug(f'receive a "Get node" request, the receive data is {data}')
    logger.debug(f'self node is {KadeNode.NodeData.GetData()}')
    if SelfNode['ID'] == DestinateID:
        logger.info(f'此node {SelfNode["ID"]} 即為查找目標，回傳此node資料給予node {data["origin"]["ID"]}')
        #SendData = _DataFill(SelfNode, 'REPLY', 'node', data = data, destination = SelfNode)
        logger.debug(f'Reply back to origin node, origin address is {data["origin"]["address"]}')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], destination = SelfNode, data = data)
    else:
        logger.info(f'此node {SelfNode["ID"]} 非查找目標，執行LookUP function')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], data = data,
             content = KadeNode.LookUp(DestinateID, data))       
        
        

def ReceiveGetNode(data, KadeNode):
    '''receive the request node'''
    if data['destination'].get('address', None) != None:
        KadeNode.update(data['destination'])
        logger.info(f'LookUp success!!!!!!!   I find the node {data["destination"]["ID"]}')
    else:
        logger.info(f'Get node receive reply, add the node into bucket {data["content"]}')
        for node in data['content']:
            KadeNode.update(node)
        

def _SaveFile(data, KadeNode):
    logger.info(f'node {KadeNode.ID} 開始將FileID為 {data["content"]["FileID"]} 的檔案存於本地')
    name = data['content']['FileID'] + '.txt'
    folder = Path(KadeNode.SavePath, 'file')
    folder.mkdir(parents=True, exist_ok=True) 
    file = folder / name
    # save the file in local
    file.write_text(json.dumps(data['content']))
    

def ReplyPostFile(data, KadeNode):
    '''
    reply to POST node request
    '''
    SelfNode = KadeNode.NodeData.GetData()
    
    data['content']['saver'].append([SelfNode, 1])
    _SaveFile(data, KadeNode)
    
    # if no distination, just save the file
    if len(data['instruct']) < 3:
        return 
    # if this node is the distanation
    elif data['instruct'][2] == SelfNode['ID']:
        del data['instruct'][2]
        data['destination'] = SelfNode
        logger.info(f'這份檔案已送達目標，將檔案送往靠近自己的node')
        
    KadeNode.UpLoadFile('', data)        
        

#receive the notice of upload file result
def ReceivePostFile(data, KadeNode):
    '''receive the reply of post node request'''
    _SaveFile(data, KadeNode)
    logger.info(f'Update File success!!!!!!!  存到檔案的節點有{[peer[0]["ID"] for peer in data["content"]["saver"][1:]]}')
    
    
def ReplyGetFile(data, KadeNode):
    '''
    reply to GET file request
    '''
    SelfNode = KadeNode.NodeData.GetData()
    file = KadeNode.GetFile(data['content']['FileID'], data)
    # if local own target file
    if file != None:
        logger.info(f'node {SelfNode["ID"]} 擁有指定檔案 ，回傳給node {data["origin"]["ID"]}')
        Ask(SelfNode, 'send', 'REPLY', 'getfile', address = data['origin']['address'], data = data, content = file, 
            destination = SelfNode)

            
def ReceiveGetFile(data, KadeNode):
    _SaveFile(data, KadeNode)
    logger.info(f'Get File success!!!!!!! 我拿到檔案了!!!!!!!!')
    

def ReplyGetBucket(KadeNode):
    '''
    reply to GET bucket request
    '''
    result = []
    for distance, bucket in KadeNode.table.items():
        if KadeNode.table[distance].length() != 0:
            result.extend(KadeNode.table[distance].bucket.values())
    logger.debug(f'IN ReplyGetBucket... result = {result}')
    logger.info(f'即將回傳bucket中其他節點資料')    
    return json.dumps(result).encode('utf-8') if result != [] else None
    
    
def ReceiveReject(data, KadeNode):
    logger.debug('In receive reject...')
    SelfNode = KadeNode.NodeData.GetData()
    # add failnode to fail
    FailNode = data['path'].pop()
    data['fail'].append(FailNode['ID'])
    # delete self and it will add back later
    del data['path'][-1]
    logger.debug(f'from now on, the path is {data["path"]}')
    AnotherNode = KadeNode.GetDistanceNode(0, FailNode['ID'], ExceptList = data['fail'])
    #if there is another node
    if AnotherNode != None:
        logger.debug(data['fail'])
        logger.info(f'找另一節點node {AnotherNode[0]["ID"]} 傳送資料')
        KadeNode._getallnode()
        Ask(SelfNode, 'send', connect = AnotherNode)
    # if this is not the first node, continue reject
    elif len(data['path']) > 0:
        logger.info(f'找無其他節點傳送 ，回傳給node {data["path"][-1]["ID"]} 請求拒絕')
        Reject(SelfNode, data)
    # the request fail
    else:    
        logger.info('oops! the request fail!!!!!!!!!!!')
