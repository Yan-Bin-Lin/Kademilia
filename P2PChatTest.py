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
        
        input('wait for instruct to get chat and  post')
        print(f"the chat record of 11 is {server.GetChat('11')}")
        print(f"the post is {server.GetPost()}")
        
    elif instruc == 'n':
        with open('Save/00.txt', 'rb') as file:
            s = pickle.load(file)
                
        end = P2PNode(ID = '11', node = s)    
        end.chat('01', 'hi')    
    
    elif instruc == 'm':
        with open('Save/00.txt', 'rb') as file:
            n = pickle.load(file)
                
            end = P2PNode(ID = '11', node = n)    
            end.post('00', 'hi')   
            end.broadcast('hihihihihihi')
            


    while(1):
        pass


if __name__ == "__main__":
    ChatTest()