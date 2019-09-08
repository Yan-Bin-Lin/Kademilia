'''
Created on 2019年9月1日

@author: danny
'''
import pickle

from .KBucket import KBucket
from .NodeData import NodeData
from ..crypto.RSASign import RSA
from ..network.connect import Connect
from ..util.hash import *
from ..handler.respond import *

# a single kade node
class KadeNode():
    '''
    a kadenode should content node data
    node data should content IP, port, PublicKey, ID
    '''
    def __init__(self, **kwargs):
        self.RSA = RSA()
        self.web = Connect()
        self.address = self.web.GetServeAddress()
        self.ID = kwargs.get('ID', GetHash(self.address[0] + str(self.address[1])))#random ID here
        self.NodeData = NodeData(self.address, self.RSA.GetPublicKey(), self.ID)
        # routing table content all Kbucket, initial create empty table, key = distance, value = bucket
        self.table = {i : KBucket(self.NodeData) for i in range(1, 128)}
        self.run()
        
        
    # add new node to bucket in the table    
    def update(self, node):
        print('update ID = ' + node['ID'])
        distance = CountDistance(self.ID, node['ID'])
        self.table[distance].AddNode(node)
        
    
    # request to other node
    # blocking
    def request(self, node, instruct):
        #self.web.send(node.GetAddress(), instruct)
        self.web.request(node.GetAddress(), instruct)
        # call function to get the node by handler here...
        # node = ...
          
          
    # send to other node
    # no blocking
    def send(self, instruct, node, connect = None):
        self.web.send(instruct, node, connect)
            
            
    # find a node
    def LookUp(self, ID, data = {}):
        distance = CountDistance(self.ID, ID)
        #result[0] = nodedata, result[1] = socket
        result = self.table[distance].GetNode(ID)
        print(f' LookUp result is {result}')
        if result == None:
            print('LookUp: Id not in local bucket, strart to send to search')
            # if node not in table, ask other node in same distance to find the target node
            # SearchNode = [node, socket] or None
            SearchNode = self.table[distance].GetNode()            
            print(f' SearchNode result is {SearchNode}')
            if SearchNode != None:
                # SendGetNode(from, to, destination, data)
                SendGetNode(self.NodeData.GetData(), ID, data, SearchNode[0], SearchNode[1])
        elif data != {}:
            SendGetNode(self.NodeData.GetData(), ID, data, result[0], result[1])
        return result
        
    
    # save node data
    def save(self, path='test_save'):
        #path += '/' + self.ID
        with open(path, 'wb') as file:
            pickle.dump(self.NodeData.GetData(), file)
        
    
    def run(self):
        # giveout self instance to server which will call handler to handle
        self.web.server.KadeNode = self
        self.web.run()
        
    
    def closs(self):
        pass
    
    '''
    # get a node data and connect socket
    # a peer sould be a Nodedata or ID
    def _GetNode(self, ID):
        distance = self.CountDistance(ID)
        result = self.table[distance].GetNode(ID)   
        # save the connect socket
        if result != None:
            self.connect[ID] = result[1]
        return result, distance
    '''