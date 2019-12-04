# -*- coding: UTF-8 -*-
'''
Created on 2019年10月10日

@author: danny
'''
import pickle
from src.P2PLending.P2PNode import P2PNode

def ContractTest():
    instruc = input('key in "s" for a first node, key in "n" for a second node, key in "m" for a third node, else the last node\n')
        
    if instruc == 's':
        server = P2PNode(ID = '00')
        server.save()
        
        input('wait for instruct to get contract')
        print(f"the contract record of 11 is {server.GetTmpContract('11')}")
        contract = server.SendContract(True, ID = '11', transation = server.GetTmpContract('11')[0]['msg']['Transation'], other = server.GetTmpContract('11')[0]['msg']['Trader']['brower'])
        server.UpLoadFile(str(contract))
        
    elif instruc == 'n':
        with open('Save/00/00.txt', 'rb') as file:
            server = pickle.load(file)
                
        end = P2PNode(ID = '11', node = server)
        end.save()
        
        end.SendContract(False, ID = '00', money = '$', date = '2019', amount = 900)
        
        input('wait for instruct to get contract')
        print(f"the contract record of 00 is {end.GetTmpContract('00')}")

    while(1):
        pass


if __name__ == "__main__":
    ContractTest()