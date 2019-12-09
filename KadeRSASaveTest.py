# -*- coding: UTF-8 -*-
'''
Created on 2019年12月10日

@author: danny
'''
from src.node.KadeNode import KadeNode

def RSASaveTest():
    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')
        
    if instruc == 's':
        server = KadeNode(ID = '00')
        server.SaveRSA()
        print(server.NodeData.GetData())
        
    else:       
        end = KadeNode(ID = '00', RSASave = True)
        print(end.NodeData.GetData())

    while(1):
        pass


if __name__ == "__main__":
    RSASaveTest()