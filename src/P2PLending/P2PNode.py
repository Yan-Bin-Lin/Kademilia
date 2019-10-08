# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
from ..node.KadeNode import KadeNode
from ..crypto.DHKeyExchange import DH
from .P2Pnetwork import P2PConnect

from ..util.log import log
logger = log()

class P2PNode(KadeNode):
    '''
    This is the main node application in p2p lending inheribit from Kademlia node
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super().__init__(*args, **kwargs)
        self.secrete = {}
        
        
    def WebInit(self):
        self.web = P2PConnect()

    
    def chat(self, ID, msg, *, node = None, content = ''):
        '''
        send a message to other node
        
        Arguments:
            ID (bstr): the ID of node the msg send to
            msg: msg need to be send
            node (NodeData): a dict of NodeData of node the msg send to
        '''
        self.send(ID, 'POST', 'message' if content == '' else 'post', msg, node = node, content = content)
        
    
    def broadcast(self, msg, content = ''):    
        '''
        broadcast message to all node in bucket
        '''
        for node in self.GetAllNode():
            self.chat('', msg, node = node, content = content)
            
    
    def SignMsg(self):
        pass
    
    
    def Whisper(self, msg):
        '''
        send encrypt msg, must initial(call SecreteInit) first
        '''
        pass
    
    
    def SecreteInit(self, ID, *, data = {}, node = None):
        node = self.GetNode(ID, closest = False) if node == None else None
        if node == None:
            logger.info(f"node not found")
            return None
        
        PK = None if data == {} else data['content']['sign']['plaintext']
        
        SecreteKey = self.secrete.get([node['ID']], None)
        # if there is no DH exist 
        if SecreteKey == None:
            SecreteKey = DH(PK)
            msg = SecreteKey.DumpPublicKey()
            self.Whisper(msg)
        elif type(SecreteKey) == DH:
            pass
        