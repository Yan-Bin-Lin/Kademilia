# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
from ..node.KadeNode import KadeNode

class P2PNode(KadeNode):
    '''
    This is the main node application in p2p lending inheribit from Kademlia node
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super.__init__(*args, **kwargs)
        
    
    def chat(self, ID, msg, *, node = None, content = ''):
        '''
        send a message to other node
        
        Arguments:
            ID (bstr): the ID of node the msg send to
            msg: msg need to be send
            node (NodeData): a dict of NodeData of node the msg send to
        '''
        self.send(ID,'send', 'POST', 'message' if content == '' else 'post', msg, node = node, content = content)
        
    
    def broadcast(self, msg, content = ''):    
        '''
        broadcast message to all node in bucket
        '''
        for node in self.GetAllNode():
            self.chat('', msg, node = node, content = content)