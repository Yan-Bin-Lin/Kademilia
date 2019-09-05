'''
Created on 2019年9月1日

@author: danny
'''
from .KBucket import KBucket
from .NodeData import NodeData
from ..crypto.RSASign import RSA
from ..network.connect import Connect
from ..util.hash import GetHash

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
        # routing table content all Kbucket, initial create empty table
        self.table = {i : KBucket() for i in range(128)}
        self.run()
        
        
    # add new node to bucket in the table    
    def update(self, node):
        distance = self.CountDistance(node.GetID())
        self.table[distance].AddNode(node)
    
    
    # count the distance of other node and self
    def CountDistance(self, ID):
        length = len(ID)
        for i in range(length):
            if ID[i] != self.ID[i]:
                break
        return length - i 
    
    
    def request(self, node, instruct):
        #self.web.send(node.GetAddress(), instruct)
        self.web.request(node.GetAddress(), instruct)
        # call function to get the node by handler here...
        # node = ...
            
            
    # find a node
    def LookUp(self, ID):
        distance = self.CountDistance(ID)
        node = self.table[distance].GetNode(ID)
        # if node not in table
        '''
        if node == None:
            SameDistanceNode = self.table[distance].GetNode()
            if SameDistanceNode != None:
                self.request(SameDistanceNode, 'search:' + 'ID')
        '''
        return node
        
    
    def run(self):
        self.web.run()
        
    
    def closs(self):
        pass