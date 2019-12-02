# -*- coding: UTF-8 -*-
'''
Created on 2019年10月1日

@author: danny
'''
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.P2PLending.P2PNode import P2PNode
from src.node.NodeData import NodeData
from src.util import hash

from src.util import setup

from src.util.log import log
logger = log()

def FinalTest():
    instruct = input('please enter "s" for a server node ID = "00000000", ' +
    ' "c" for 8 specify node, "r" for 8 random node,or just key in something else to be user node for conteol\n')
    
    if instruct == 's':
        
        node = P2PNode(ID = '00000000')
        node.save()
        
    elif instruct == 'c':
        
        with open('Save/00000000/00000000.txt', 'rb') as file:
            server = pickle.load(file)
        
        nodes = []
        ID = '00000000'
        for i in range(8):
            nodes.append(P2PNode(ID = ID.replace('0', '1', i), node = server))
            
    elif instruct == 'r':
        
        with open('Save/00000000/00000000.txt', 'rb') as file:
            server = pickle.load(file)

        for i in range(8):
            nodes.append(P2PNode(node = server))        

    else:
            
        with open('Save/00000000/00000000.txt', 'rb') as file:
            server = pickle.load(file)
            
        node = P2PNode(node = server)
        
        while(1):
            
            instruct = input('\nwaiting for user key in instruction...\n' + 
                             '"getnode", "lookup", "uploadfile", "getfile", "chat", ' + 
                             '"broadcast", "post", "getchat", "getpost", "gettmpcontract", ' +
                             '"sendcontract", "whisper", "secreteinit", "gethash" \n'
                            )
            
            if instruct == 'getnode':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                print(f"{ node.GetNode(parm, closest = False)}")
                
            elif instruct == 'lookup':
                parm = input('please key in ID to specify\n')
                try:
                    print(f"{[n['ID'] for n in node.LookUp(parm)]}")
                except:
                    print(f"{node.LookUp(parm)['ID']}")
                    
            elif instruct == 'uploadfile':
                parm = input('please key in something as a file\n')
                parm2 = input('please key in something as Hashcode\n')
                node.UpLoadFile(parm, parm2)
                
            elif instruct == 'getfile':
                parm = input('please key FileID to specify\n')
                print(node.GetFile(parm))
            
            elif instruct == 'chat':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                parm2 = input('please key in msg\n')
                node.chat(parm, parm2)
                
            elif instruct == 'broadcast':
                parm = input('please key in msg\n')
                node.broadcast(parm)
                
            elif instruct == 'post':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                parm2 = input('please key in msg\n')
                node.post(parm, parm2)

            elif instruct == 'getchat':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                print(node.GetChat(parm))
                
            elif instruct == 'getpost':
                ID = input('please key in ID to specif, or just enter to get locao post record\n')
                if ID == '':
                    print(node.GetPost())
                else:
                    print(node.GetPost(ID))
                   
            elif instruct == 'gettmpcontract':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                print(node.GetTmpContract(parm))
                               
            elif instruct == 'sendcontract':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = True if input('please key in "y" that you are lender else brower\n') == 'y' else False
                parm2 = input('please key in ID to specify\n')
                parm3 = input('please key in anything for content of contract\n')
                node.SendContract(parm, ID = parm2, contract = parm3)
                
            elif instruct == 'whisper':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify, NOTE: remember to call "secreteinit" first\n')
                parm2 = input('please key in message you want to send\n')
                node.Whisper(parm, parm2)     
                 
            elif instruct == 'secreteinit':
                print(f'all node in self is {[list(v.keys()) for v in node.GetAllNode().values()]}')
                parm = input('please key in ID to specify\n')
                node.SecreteInit(parm)
                
            elif instruct == 'gethash':
                parm = input('please key in something to get hash\n')
                print(hash.GetHash(parm))

    while(1):
        pass

if __name__ == '__main__':
    FinalTest()