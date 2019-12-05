# -*- coding: UTF-8 -*-
'''
Created on 2019年10月12日

@author: danny
'''
import pickle
from src.P2PLending.P2PNode import P2PNode

def WhisperTest():
    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')
        
    if instruc == 's':
        server = P2PNode(ID = '00')
        server.save()
    
        input('wait for whisper...')

        while(1):
            server.Whisper('11', input('wait for whisper...'))
        
    elif instruc == 'n':
        with open('Save/00/00.txt', 'rb') as file:
            s = pickle.load(file)
                
        end = P2PNode(ID = '11', node = s)    
        end.SecreteInit('00') 
        
        while(1):
            end.Whisper('00', input('wait for whisper...'))


if __name__ == "__main__":
    WhisperTest()
