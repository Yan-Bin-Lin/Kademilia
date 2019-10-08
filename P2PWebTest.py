# -*- coding: UTF-8 -*-
'''
Created on 2019年10月3日

@author: danny
'''

from kademilia.src.P2PLending.P2Pnetwork import P2PConnect

def WebTest():
    c = P2PConnect()
    c.run()
    c.Ask({'ID' : '001', 'address' : '125'}, 'request', 'a')

    while(1):
        pass
    
if __name__ == "__main__":
    WebTest()