'''
Created on 2019年9月1日

@author: danny
'''

from ..network.connect import Connect
from .KBucket import KBucket
from .NodeData import NodeData
from ..crypto.RSASign import RSA


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
        self.RoutingTable = {}
        
    
    def run(self):
        self.web.run()
        
    
    def closs(self):
        pass
    
    