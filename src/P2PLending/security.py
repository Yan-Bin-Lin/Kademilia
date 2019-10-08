# -*- coding: UTF-8 -*-
'''
Created on 2019年10月3日

@author: danny
'''
from ..crypto.DHKeyExchange import DH

from ..util.log import log
logger = log()


def SecreteInit(KadeNode, ID, *, data = {}, node = None):
        node = KadeNode.GetNode(ID, closest = False) if node == None else None
        if node == None:
            logger.info(f"node not found")
            return None
        
        PK = None if data == {} else data['content']['sign']['plaintext']
        
        SecreteKey = KadeNode.secrete.get([node['ID']], None)
        # if there is no DH exist 
        if SecreteKey == None:
            KadeNode.secrete[node['ID']] = DH(PK)
        elif type(SecreteKey) == DH:
            pass

def CheeckSign(RSA, public_key, sign, msg):
    '''
    verify a signature
    '''
    return RSA.verify(public_key, sign, msg)

