# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

from collections import OrderedDict

from ..handler.communicate import ping
    
class KBucket():
    '''
    a KBucket mean each distance content number of "MAX" k bucket
    '''
    def __init__(self, K = 8):
        #max nuber of a bucket
        self.K = K
        self.bucket = OrderedDict()
    
    
    # add a new node data to bucket
    def AddNode(self, node):
        # if the bucket is full, delete a node
        if self.IsFull():
            self.clean()
        self.bucket[node.GetID()] = node
        
        
    # delete a node data of a bucket    
    def DelNode(self, ID):
        self.bucket.pop(ID, None)
        
    
    # check if a node is in bucket and alive
    def CheckNode(self, ID):
        if ID in self.bucket:
            return self.IsExist(ID)
        return False
    

    def GetNode(self, *args):
        '''
        return a NodeData 
        if there is a parmeter "ID", return the node if it is in the bucket, else return none 
        if you don't give any parmeter, return a alive node, or return false if there is no alive node       
        '''
        #print('args = ' + args[0])
        # if receive parmeter "ID"
        if len(args) == 1:
            print('i am in GetNode(ID) len1, i will return')
            print(self.bucket[args[0]])
            return self.bucket[args[0]] if self.CheckNode(args[0]) else None
        # if no parmeter
        else:
            for ID, node in self.bucket.items():
                if self.IsExist(ID):
                    return self.bucket[ID]
        return  None
        
    
    # check if the node in bucket is exist
    def IsExist(self, ID):
        return ping(self.bucket[ID].GetAddress())
        
            
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
        