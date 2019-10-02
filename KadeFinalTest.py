# -*- coding: UTF-8 -*-
'''
Created on 2019年10月1日

@author: danny
'''
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.node.KadeNode import KadeNode
from src.node.NodeData import NodeData

def FinalTest():
    instruct = input('please enter "s" for a node ID = "00000000", or just key in something else to be other ID\n')
    
    if instruct == 's':
        
        node = KadeNode(ID = '00000000')
        node.save()       
    
    else:

        with open('Save/00000000.txt', 'rb') as file:
            server = pickle.load(file)

        node = KadeNode(ID = '00000001', node = server)
            
    while(1):
        pass  

if __name__ == '__main__':
    FinalTest()