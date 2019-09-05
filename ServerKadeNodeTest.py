# -*- coding: UTF-8 -*-
'''
Created on 2019年9月5日

@author: danny
'''
from src.node.KadeNode import KadeNode
import pickle
    

if __name__ == '__main__':
    server = KadeNode(ID = '01010100')
    
    with open('test_save', 'wb') as file:
        pickle.dump(server.NodeData.GetData(), file)
    
    while(1):
        pass