# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

from collections import OrderedDict
import time

from ..handler.ask import Ask
from ..util.hash import CountDistance
from ..util.thread import TreadPool
    
import logging
logger = logging.getLogger( 'loglog' )      

class KBucket():
    '''
    a KBucket mean each distance content number of "MAX" k node
    '''
    def __init__(self, SelfNode, K = 8):
        #max nuber of a bucket
        self.K = K
        self.bucket = OrderedDict()
        self.fresh = {}
        self.SelfNode = SelfNode
    
    
    def AddNode(self, node):
        '''
        Add the node if the bucket is not full or the last node in bucket not exist(clean node success)
        
        Args:
            node(dict): NodeData to save
        '''
        logger.debug(f'check for add node...')
        if not self.IsFull() or self.clean():     
            self.bucket[node['ID']] = node
            self.fresh[node['ID']] = 0
            logger.debug(f'add the node: {self.bucket[node["ID"]]}')           
    
    
    def DelNode(self, ID):
        '''
        delete a node data of a bucket
        Args:
            ID: the node to delete
        '''
        self.bucket.pop(ID, None)
        
    
    def CheckNode(self, ID):
        '''
        check if a node is in bucket and alive
        Args:
            ID: the node to delete
        '''
        if ID in self.bucket:
            return self.IsExist(ID)
        return None
    

    def GetNode(self, GetID, recursive = True, closest = True, ping = True, num = 8, ExceptList = []):
        '''
        return a NodeData 
            
        Args:
            closest: if true, return "k" most closest node if the node not found in the bucket
            ping: if true, check if the node is exist before return
            num (int): return number of cloest node
            *args (tuple): For ID to get specufy node, 
                if return the node and connect socket if it is in the bucket, else return None 
        
        Returns:
            connect (tuple): (ConnectNode, ConnectSocket) if success connect else None
        '''
        logger.debug(f'in kbucket getnode...\n Kbucket size = {self.length()}, GetID = {GetID}\n the bucket is {self.bucket.values()}')
        #logger.debug(f'args is {args}, recursive = {recursive}, ping = {ping}')
        logger.debug(f'ExceptList = {ExceptList}')     
        
        if self.length() == 0:
            return []
        
        # check if the ID in the ExceptList
        IDs = set(self.bucket.keys()).difference(set(ExceptList))
        logger.debug(f" the IDs to find is {IDs}, ExceptList = {ExceptList}")            
            
        if GetID not in IDs:
            # return none for only ask one value
            if not closest:
                return []
        
        # start to ping to check exist
        if ping:
            tp = TreadPool()
            for ID in IDs:
                tp.AddTask(self.IsExist, ID)
            result = tp.WaitResult()            
            logger.debug(f'the result is {result}')
            IDs = [r['para'][0][0] for r in result if r['return_']]
            
        # sort for most closest distance
        IDs.sort(key=lambda ID: int(CountDistance(ID, GetID), 2))
        logger.debug(f'the IDs is {IDs}, return {[self.bucket[ID] for ID in IDs]}')
        if IDs == []:
            return []
        else:
            return [self.bucket[ID] for ID in IDs]
        
        '''
        # if receive parmeter "ID"
        if len(args) == 1:
            ID = args[0]
            # if ping is False
            if not ping:
                return self.bucket.get(ID, None)
            # if not recursive
            if ID not in ExceptList and not recursive:
                connect = self.CheckNode(ID)
                return None if connect == None else [self.bucket[ID], connect]
        
        # if no parmeter or except is True
        items = copy.deepcopy(self.bucket).items()
        for ID_, node in items:
            # except the given ID
            if ID_ not in ExceptList:
                # if not ping
                if not ping:
                    return self.bucket[ID_]
                
                connect = self.IsExist(ID_)
                if connect != None:
                    return  [self.bucket[ID_], connect]
        return None
        '''
        
    
    def IsExist(self, ID, NodeData = None):
        '''check if the node in bucket is exist'''
        # if node is fresh, don't ping
        if time.time() - self.fresh.get(ID, 0) < 3600:
            return True
        
        destination = self.bucket[ID] if NodeData == None else NodeData
        connect = Ask(self.SelfNode.GetData(), 'request', 'TRACE', 'ping', destination = destination, address = self.bucket[ID]['address'])
        logger.debug(f'the return will be {[True if connect[1] != None else False]}')
        if connect == None and NodeData == None:
            self.DelNode(ID)
        
        # the node is online
        if connect[1] != None:
            self.fresh[ID] = time.time()
            return True
        
        return False
        
            
    def length(self):
        '''return number of node in the Kbucket'''
        return len(self.bucket)
        
    
    def IsFull(self):
        '''check if the number of node in Kbucket >= k'''
        return True if self.length() >= self.K else False
    
    
    def clean(self):
        '''
        del a no response node. return True
        if all node exist, check the oldest(first) node is exist or not
        if the oldest node exist still exist, move the nose to the newest(first) and return fail 
        '''
        # check if there is node in the bucket
        if self.length() == 0:
            return False
        # pop the last node
        ID, NodeData = self.bucket.popitem(False)
        # if the pop node is exist, add back to the first
        if not self.IsExist(ID, NodeData):
            self.bucket[ID] = NodeData
            # clean false
            return False
        return True

        