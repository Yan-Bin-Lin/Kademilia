# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

from collections import OrderedDict
import copy

from ..handler.ask import Ask
    
import logging
logger = logging.getLogger( 'loglog' )      

class KBucket():
    '''
    a KBucket mean each distance content number of "MAX" k bucket
    '''
    def __init__(self, SelfNode, K = 8):
        #max nuber of a bucket
        self.K = K
        self.bucket = OrderedDict()
        self.SelfNode = SelfNode
    
    
    # add a new node data to bucket
    def AddNode(self, node):
        if self.bucket.get(node['ID'], False) != False:
            return
        # if the bucket is full, delete a node
        if self.IsFull():
            self.clean()
        self.bucket[node['ID']] = node
        
        
    # delete a node data of a bucket    
    def DelNode(self, ID):
        self.bucket.pop(ID, None)
        
    
    # check if a node is in bucket and alive
    def CheckNode(self, ID):
        if ID in self.bucket:
            return self.IsExist(ID)
        return None
    
    
    '''
    return a NodeData 
    if there is a parmeter "ID", return the node and connect socket if it is in the bucket, else return None 
    if there is a 'second' parmeter "except" = False, will return anothe node except of given ID
    if you don't give any parmeter, return a alive node and connect socket, or return None if there is no alive node       
    '''
    def GetNode(self, *args, except_ = False, ping = True):
        logger.info('in kbucket getnode...')
        logger.debug(f'args is {args}, except_ = {except_}, ping = {ping}')
        ID = ''
        # if receive parmeter "ID"
        if len(args) == 1:
            ID = args[0]
            # if ping is False
            if not ping:
                return self.bucket.get(ID, None)
            # if not except
            if not except_:
                connect = self.CheckNode(ID)
                return None if connect == None else [self.bucket[ID], connect]
        
        # if no parmeter or except is True
        items = copy.deepcopy(self.bucket).items()
        for ID_, node in items:
            # except the given ID
            if ID_ != ID:
                # if not ping
                if not ping:
                    return self.bucket[ID_]
                
                connect = self.IsExist(ID_)
                if connect != None:
                    return  [self.bucket[ID_], connect]
        return None
        
    
    # check if the node in bucket is exist
    def IsExist(self, ID):
        connect = Ask(self.SelfNode.GetData(), 'request', 'TRACE', 'ping', destination = self.bucket[ID], address = self.bucket[ID]['address'])
        if connect == None:
            self.DelNode(ID)
        return connect[1]
        
            
    # return number of node in the Kbucket
    def length(self):
        return len(self.bucket)
        
    
    # check if the number of node in Kbucket >= k
    def IsFull(self):
        return True if self.length() >= self.K else False
    
    
    # del a no response node.
    # if all node exist, del the oldest(first) node 
    def clean(self):
        for ID, node in self.bucket.items():
            if not self.IsExist(ID):
                self.DelNode(ID)
                return
        # del the first node
        self.bucket.popitem(False)
        