# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
from . import setup

import hashlib
from pathlib import Path

OutSize = int(setup.OutSize)
# return bit like string(0110101.......)
def _HashFormat(HashHexCode, OutSize = OutSize):
    return bin(int(HashHexCode, 16)).zfill(OutSize)[-OutSize:]
    

def GetHash(data, OutSize=OutSize):
    '''
    hash a data
    
    Args:
        OutSize (int): output length
        
    Returns:
        str: hash string in bit string format
    '''
    HashFunc = hashlib.md5()
    HashFunc.update(data.encode(encoding='utf-8')) 
    return _HashFormat(HashFunc.hexdigest(), OutSize)


# hash a big file
def GetHashFile(path, OutSize=OutSize):
    HashFunc = hashlib.md5()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(1024), b""):
            HashFunc.update(chunk)
    return _HashFormat(HashFunc.hexdigest(), OutSize)
    

def CountDistance(SelfID, OtherID):
    '''
    count the distance of two node ID(by xor)
    
    Returns:
        str: distance in bit string format
    '''
    return ''.join(str(r) for r in (ord(x) ^ ord(y) for x, y in zip(SelfID, OtherID)))


if __name__ == '__main__':
    print(GetHash('4'))
    data = '10101010'
    print(GetHash(data))

    compare = '10110101'
    print(int(CountDistance(data, compare), 2))
    
    print(GetHashFile(Path('../../Test.log')))