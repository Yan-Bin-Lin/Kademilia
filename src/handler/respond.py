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
from .ask import Ask

'''
# send to someone for a GET node request
def SendGetNode(SelfNode, DestinateID = None, data = {}, ToNode = None, connect = None):
    if data == {}:
        data = _DataFill(SelfNode, 'GET', 'node', data = data, destination = NodeData(ID = DestinateID).GetData())
    else:
        data = _DataFill(SelfNode, 'GET', 'node', data = data)
    print(f'start to send to node {ToNode["ID"]} to find node {DestinateID}, the data is {data}')
    send(data, connect)
''' 
    
# reply to someone send GET node
def ReplyGetNode(data, KadeNode):
    DestinateID = data['destination']['ID']
    SelfNode = KadeNode.NodeData.GetData()
    print(f'receive a "Get node" request, the receive data is {data}')
    print(f'self node is {KadeNode.NodeData.GetData()}')
    if SelfNode['ID'] == DestinateID:
        #SendData = _DataFill(SelfNode, 'REPLY', 'node', data = data, destination = SelfNode)
        print(f'Reply back to origin node, origin address is {data["origin"]["address"]}')
        Ask(SelfNode, 'send', 'REPLY', 'getnode', address = data['origin']['address'], destination = SelfNode, data = data)
    else:
        KadeNode.LookUp(DestinateID, data)
        

# receive the request node
def ReceiveGetNode(data, KadeNode):
    KadeNode.update(data['destination'])
    print(f'LookUp success!!!!!!!   I find the node {data["destination"]["ID"]}')
    

def _SaveFile(data, KadeNode):
    name = data['content']['FileID'] + '.txt'
    folder = Path(KadeNode.SavePath, 'file')
    folder.mkdir(parents=True, exist_ok=True) 
    file = folder / name
    # save the file in local
    file.write_text(json.dumps(data['content']))
    

def ReplyPostFile(data, KadeNode):
    print('IN ReplyPostFile...')
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
    print(f'Update File success!!!!!!!')
    
    
def ReplyGetFile(data, KadeNode):
    SelfNode = KadeNode.NodeData.GetData()
    file = KadeNode.GetFile(data['content']['FileID'], data)
    # if local own target file
    if file != None:
        print('I have the file, give you')
        Ask(SelfNode, 'send', 'REPLY', 'getfile', address = data['origin']['address'], data = data, content = file, 
            destination = SelfNode)

            
def ReceiveGetFile(data, KadeNode):
    _SaveFile(data, KadeNode)
    print(f'Get File success!!!!!!!')
    

def ReplyGetBucket(KadeNode):
    result = []
    for distance, bucket in KadeNode.table.items():
        if KadeNode.table[distance].length() != 0:
            result.extend(KadeNode.table[distance].bucket.values())
    print(f'IN ReplyGetBucket... result = {result}')
    return json.dumps(result).encode('utf-8') if result != [] else None
    
    
def ReceiveReject(dara, KadeNode):
    pass
    
'''
# test if a node is online, if true return socket else none
def ping(DestinateNode, SelfNode = None):
    #return connect(socket) or None
    data = _DataFill(SelfNode, 'TRACE', 'ping', destination = DestinateNode)
    return request(data, None, DestinateNode['address'])[1]
'''