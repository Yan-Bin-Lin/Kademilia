# -*- coding: UTF-8 -*-
'''
Created on 2019年9月5日

@author: danny
'''
from src.node.KadeNode import KadeNode
    

if __name__ == '__main__':
    server = KadeNode(ID = '00000000')
    server.save('server_save')
    
    while(1):
        pass