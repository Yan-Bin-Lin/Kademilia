# -*- coding: UTF-8 -*-
'''
Created on 2019年9月15日

@author: danny
'''

import pickle

from src.node.KadeNode import KadeNode
from src.util.hash import GetHash

def RejectTest():

    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')
    
    if instruc == 's':
        server = KadeNode(ID = '111')
        server.save()
    
    elif instruc == 'n':
                
        next = KadeNode(ID = '001')
        next.save()
        
        with open('Save/111.txt', 'rb') as file:
            s = pickle.load(file)
        
        next.update(s)
        
    elif instruc == 'm':
        mid = KadeNode(ID = '010')
        mid.save()
    
        with open('Save/001.txt', 'rb') as file:
            n = pickle.load(file)
        
        mid.update(n)
    
    else:
        with open('Save/010.txt', 'rb') as file:
            m = pickle.load(file)
                
        end = KadeNode(ID = '100')
        end.update(m)       
        
        end.LookUp('000')
    
    while(1):
        pass
    
if __name__ == '__main__':
    RejectTest()