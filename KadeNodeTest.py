# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

from src.node.KadeNode import KadeNode


if __name__ == '__main__':
    a = KadeNode()
    a.update(3, a.NodeData)
    print(a.LookUp(101010101).GetID())