# -*- coding: UTF-8 -*-
'''
Created on 2019年9月13日

@author: danny
'''
import pickle
import time

from src.node.KadeNode import KadeNode
from src.util.hash import GetHash

instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')

if instruc == 's':
    server = KadeNode(ID = '00')
    server.save()
    server.SavePath = 'ServerSave'
    
elif instruc == 'n':
    with open('Save/00.txt', 'rb') as file:
        s = pickle.load(file)
            
    next = KadeNode(ID = '01')
    next.save()
    next.update(s)
    next.SavePath = 'NextSave'
    
  
elif instruc == 'm':
    with open('Save/01.txt', 'rb') as file:
        n = pickle.load(file)
            
    mid = KadeNode(ID = '10')
    mid.save()
    mid.update(n)    
    mid.SavePath = 'MidSave'
    
    mid.UpLoadFile('4')

else:
    with open('Save/01.txt', 'rb') as file:
        n = pickle.load(file)
            
    end = KadeNode(ID = '11')
    end.save()
    end.update(n)       
    end.SavePath = 'EndSave'
    
    end.GetFile(GetHash('4'))
    
while(1):
    pass