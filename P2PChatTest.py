# -*- coding: UTF-8 -*-
'''
Created on 2019年10月3日

@author: danny
'''
import pickle
from src.P2PLending.P2PNode import P2PNode

def ChatTest():
    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')

    if instruc == 's':
        server = P2PNode(ID = '00')
        server.save()
        
    else:
        with open('Save/00.txt', 'rb') as file:
            m = pickle.load(file)
                
        end = P2PNode(ID = '11', node = m)    
        end.chat('00', 'hi')    
        print(end.GetAllNode())
    while(1):
        pass


if __name__ == "__main__":
    ChatTest()