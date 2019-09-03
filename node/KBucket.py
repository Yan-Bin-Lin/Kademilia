# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

from collections import OrderedDict

    
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
        
    
    # return a NodeData if it is in the bucket, else return None 
    def GetNode(self, ID):
        return self.bucket.get(ID, None)
        
    
    # check if the node is exist
    def IsExist(self, ID):
        pass
        # call handler function here...
    
    
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
        