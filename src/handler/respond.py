# -*- coding: UTF-8 -*-
'''
Created on 2019年9月6日

@author: danny
'''
import json
from pathlib import Path
import time

from ..network.communicate import *
from ..util.hash import *
from ..util.web import _DataFill
from ..node.NodeData import NodeData
from .ask import Ask #Reject

from ..util.log import log
logger = log()
    

def ReplyGetNode(data, KadeNode):
    '''
    reply to GET node request
    '''
    DestinateID = data['destination']['ID']
    SelfNode = KadeNode.NodeData.GetData()
    logger.debug(f'receive a "Get node" request, the receive data is {data}')
    logger.debug(f'self node is {KadeNode.NodeData.GetData()}')
    if SelfNode['ID'] == DestinateID:
        logger.warning(f'此node {SelfNode["ID"]} 即為查找目標，回傳此node資料給予node {data["origin"]["ID"]}')
        #SendData = _DataFill(SelfNode, 'REPLY', 'node', data = data, destination = SelfNode)
        logger.debug(f'Reply back to origin node, origin address is {data["origin"]["address"]}')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], destination = SelfNode, data = data)
    else:
        logger.warning(f'此node {SelfNode["ID"]} 非查找目標，執行LookUP function')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], data = data,
             content = KadeNode.LookUp(DestinateID, data))       
        
        

def ReceiveGetNode(data, KadeNode):
    '''receive the request node'''
    if data['destination'].get('address', None) != None and data['destination'].get('ID', None) != KadeNode.ID:
        KadeNode.update(data['destination'])
        logger.warning(f'LookUp success!!!!!!!   I find the node {data["destination"]["ID"]}')
    else:
        try:
            logger.warning(f'Get node receive reply, add the node into bucket {[node["ID"] for node in data["content"]]}')
            for node in data['content']:
                KadeNode.update(node)
        except:
            logger.info(f'Get node receive reply, but the content is empty')
        

def _SaveFile(data, KadeNode):
    logger.info(f'node {KadeNode.ID} 開始將File {data["content"]} 存於本地')
    name = data['instruct'][2] + '.txt'
    folder = Path(KadeNode.SavePath, 'file')
    FileID = data['content']['FileID'] if type(data['content']) == type({}) else data['content'][0]['FileID']
    
    KadeNode.lock.acquire()
    
    # cirtical section
    folder.mkdir(parents=True, exist_ok=True) 
    file = folder / name
    
    if not file.exists():
        # save the file in local
        file.write_text(json.dumps([data['content']] if type(data['content']) == dict else data['content']))
    
    else:
        OriginFile = json.loads(file.read_text())
        same = False
        for of_ in OriginFile:
            # if save file has exist, update saver
            if of_['FileID'] == data['content']['FileID']:
                saver = {s[0]['ID'] : s for s in json.loads(file.read_text())[0]['saver']}
                for s in data['content']['saver']:
                    saver[s[0]['ID']] = saver.get(s[0]['ID'], 0) if saver.get(s[0]['ID'], [0, 0])[1] > s[1] else s
                data['content']['saver'] = list(saver.values()) 
                same = True
                break
            
        # if there is a file but not same to this file, append to the tail
        if not same:
            OriginFile.append(data['content'])
            
        file.write_text(json.dumps(OriginFile))

    # cirtical section
    
    KadeNode.lock.release()
    return data

def ReplyPostFile(data, KadeNode):
    '''
    reply to POST node request
    '''
    SelfNode = KadeNode.NodeData.GetData()
    
    data['content']['saver'].append([SelfNode, time.time()])
    _SaveFile(data, KadeNode)
    
    # if no distination, just save the file
    #if len(data['instruct']) < 3:
    #    return 
    # if this node is the distanation
    if data['instruct'][2] == SelfNode['ID']:
        data['destination'] = SelfNode
        logger.warning(f'這份檔案已送達目標 {data["instruct"][2]}，將檔案送往靠近自己的node')
        
    data['content']['saver'].extend(KadeNode.UpLoadFile('', data) ) 
    
    Ask(SelfNode, 'send', 'REPLY', 'postfile', data['instruct'][2], address = data['origin']['address'], data = data)
        

#receive the notice of upload file result
def ReceivePostFile(data, KadeNode):
    '''receive the reply of post node request'''
    data = _SaveFile(data, KadeNode)
    for saver in data['content']['saver']:
        KadeNode.update(saver[0])
    logger.warning(f'Update File success!!!!!!!  存到檔案的節點有{[peer[0]["ID"] for peer in data["content"]["saver"][1:]]}')
    
    
def ReplyGetFile(data, KadeNode):
    '''
    reply to GET file request
    '''
    SelfNode = KadeNode.NodeData.GetData()
    file = KadeNode.GetFile(data['content']['FileID'], data)
    # if local own target file
    if file != []:
        Ask(SelfNode, 'send', 'REPLY', 'getfile',  data['instruct'][2], address = data['origin']['address'], data = data, content = file, 
            destination = SelfNode)
    else:
        logger.warning(f'node {SelfNode["ID"]} 沒有指定檔案 ，也沒有其他node可以查找，request終止')

            
def ReceiveGetFile(data, KadeNode):
    if data['content'][0].get('FileID', None) != None:
        _SaveFile(data, KadeNode)
        logger.warning(f'Get File success!!!!!!! 我拿到檔案 {data["content"]} 了!!!!!!!!')
    else:
        for node in data['content']:
            KadeNode.update(node)
        logger.warning(f'未取得檔案，將可能存有檔案的node {[node["ID"] for node in data["content"]]} 跟新到本地bucket')
    

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
