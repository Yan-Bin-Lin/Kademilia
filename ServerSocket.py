# -*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''

from network.connect import Connect

serveport = 6687

node1 = Connect(serveport)
node1.run()

while(1):
    pass