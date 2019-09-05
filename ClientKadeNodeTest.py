# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.node.KadeNode import KadeNode
from src.node.NodeData import NodeData

if __name__ == '__main__':
    client = KadeNode()
    
    with open('test_save', 'rb') as file:
        DictNode = pickle.load(file)
    
    DictNode['PublicKey'] = serialization.load_pem_public_key(
                                DictNode['PublicKey'],
                                backend=default_backend()
                            )

    client.update(NodeData(DictNode['address'], DictNode['PublicKey'], DictNode['ID']))
    print('update success')
    print(client.LookUp('01010100').GetID())
