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

if __name__ == '__main__':
    
    instruct = input('please enter m for a middle node or for end node\n')
                
    if instruct == 'm':
        
        print(' i am a middle node...   ID = "01010101"')
        middle = KadeNode(ID = '01010101')
        middle.save('client_save')

        with open('server_save', 'rb') as file:
            server = pickle.load(file)

        middle.update(server)
        
        middle.LookUp('00000000')
        
    else:
        print(' i am a end node...   ID = "11111111"')
        end = KadeNode(ID = '11111111')
        
        with open('client_save', 'rb') as file:
            middle = pickle.load(file)
            
        end.update(middle)
        
        end.LookUp('10101010')
        
        end.LookUp('00000000')
            
    while(1):
        pass