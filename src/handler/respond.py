# -*- coding: UTF-8 -*-
'''
Created on 2019年9月6日

@author: danny
'''
import json

from ..network.communicate import *
from ..util.hash import CountDistance
from ..node.NodeData import NodeData


# return the data in protocol format
# *args = ['REPLY', 'ID', 'args...', ] (instruct)
# **kwargs = origin, destination, instruct, SelfNodes
def _DataFill(SelfNode, *args, data = {}, **kwargs):
    # new request
    if data == {}:
        data['origin'] = SelfNode
        data['destination'] = kwargs['destination']
        data['instruct'] = args
        data['path'] = [SelfNode]
    # update request
    else:
        data['origin'] = kwargs.get('origin', data['origin'])
        data['destination'] = kwargs.get('destination', data['destination'])
        data['instruct'] = args if len(args) != 0 else data['instruct']
        data['path'].append(SelfNode)
    return json.dumps(data)


# send to someone for a GET node request
def SendGetNode(SelfNode, DestinateID = None, data = {}, ToNode = None, connect = None):
    if data == {}:
        data = _DataFill(SelfNode, 'GET', 'node', data = data, destination = NodeData(ID = DestinateID).GetData())
    else:
        data = _DataFill(SelfNode, 'GET', 'node', data = data)
    print(f'start to send to node {ToNode["ID"]} to find node {DestinateID}, the data is {data}')
    send(data, connect)
    
    
# reply to someone send GET node
def ReplyGetNode(data, KadeNode):
    DestinateID = data['destination']['ID']
    SelfNode = KadeNode.NodeData.GetData()
    print(f'receive a "Get node" request, the receive data is {data}')
    print(f'self node is {KadeNode.NodeData.GetData()}')
    if SelfNode['ID'] == DestinateID:
        SendData = _DataFill(SelfNode, 'REPLY', 'node', data = data, destination = SelfNode)
        print(f'Reply back to origin node, origin address is {data["origin"]["address"]}')
        send(SendData, None, data['origin']['address'])
    else:
        KadeNode.LookUp(DestinateID, data)
        

# receive the request node
def ReceiveNode(data, KadeNode):
    KadeNode.update(data['destination'])
    print('LookUp success!!!!!!!')
    

# test if a node is online, if true return socket else none
def ping(DestinateNode, SelfNode = None):
    #return connect(socket) or None
    data = _DataFill(SelfNode, 'TRACE', 'ping', destination = DestinateNode)
    return request(data, None, DestinateNode['address'])[1]