'''
Created on 2019年9月1日

@author: danny
'''

from .KBucket import KBucket
from .NodeData import NodeData
from ..crypto.RSASign import RSA
from ..network.connect import Connect

# a single kade node
class KadeNode():
    '''
    a kadenode should content node data
    node data should content IP, port, PublicKey, ID
    '''
    def __init__(self, **kwargs):
        self.RSA = RSA()
        ID = kwargs.get('ID', 101010101)#random ID here
        self.web = Connect()
        self.NodeData = NodeData(self.web.GetServeAddress(), self.RSA.GetPublicKey(), ID)
        # routing table content all Kbucket
        self._BuildTable()
        
        
    # add new node to bucket in the table    
    def update(self, distance, node):
        self.table[distance].AddNode(node)
    
    
    # count the distance of other node and self
    def CountDistance(self, ID):
        return 3# call function...
    
    
    # find a node
    def LookUp(self, ID):
        distance = self.CountDistance(ID)
        node = self.table[distance].GetNode() 
        # if node not in table
        if node == None:
            pass
        return node
        
    
    def run(self):
        self.web.run()
        
    
    def closs(self):
        pass
    
    
    # create empty table
    def _BuildTable(self):
        self.table = {i : KBucket() for i in range(128)}