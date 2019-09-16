# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.node.KadeNode import KadeNode
from src.node.NodeData import NodeData

def FindNodeTest():
    instruct = input('please enter "s" for a server node please enter "m" for a middle node, "n" for the next of middle node or else for end node\n')
    
    if instruct == 's':
        
        server = KadeNode(ID = '00000000')
        server.save()       
    
    elif instruct == 'n':
        
        next = KadeNode(ID = '00000001')
        next.save()

        with open('Save/00000000.txt', 'rb') as file:
            server = pickle.load(file)

        next.update(server)
        
        next.LookUp('00000000')
                
    elif instruct == 'm':
        
        middle = KadeNode(ID = '01010101')
        middle.save()

        with open('Save/00000001.txt', 'rb') as file:
            next = pickle.load(file)

        middle.update(next)
        
        middle.LookUp('00000001')
        
    else:
        end = KadeNode(ID = '11111111')
        
        with open('Save/01010101.txt', 'rb') as file:
            middle = pickle.load(file)
            
        end.update(middle)
                
        end.LookUp('00000000')
            
    while(1):
        pass  

if __name__ == '__main__':
    FindNodeTest()
