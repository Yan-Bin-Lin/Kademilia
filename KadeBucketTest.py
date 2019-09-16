# -*- coding: UTF-8 -*-
'''
Created on 2019年9月14日

@author: danny
'''

import pickle

from src.node.KadeNode import KadeNode
from src.util.hash import GetHash

def BucketTest():
    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')
    
    if instruc == 's':
        server = KadeNode(ID = '00')
        server.save()
    
    elif instruc == 'n':
                
        next = KadeNode(ID = '01')
        next.save()
        
    elif instruc == 'm':
        mid = KadeNode(ID = '10')
        mid.save()
    
        with open('Save/00.txt', 'rb') as file:
            s = pickle.load(file)
        with open('Save/01.txt', 'rb') as file:
            n = pickle.load(file)   
        
        mid.update(s)
        mid.update(n)
    
    else:
        with open('Save/10.txt', 'rb') as file:
            m = pickle.load(file)
                
        end = KadeNode(ID = '11', node = m)        
        
    while(1):
        pass

if __name__ == '__main__':
    BucketTest()