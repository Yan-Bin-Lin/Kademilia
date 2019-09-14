# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
import hashlib


# return bit like string(0110101.......)
def _HashFormat(HashHexCode, OutSize = 8):
    return bin(int(HashHexCode, 16))[2:].zfill(OutSize)[-OutSize:]
    

# hash a data, which length is OutSize
def GetHash(data, OutSize=2):
    HashFunc = hashlib.md5()
    HashFunc.update(data.encode(encoding='utf-8')) 
    return _HashFormat(HashFunc.hexdigest(), OutSize)


# hash a big file
def GetHashFile(path, OutSize=8):
    HashFunc = hashlib.md5()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(1024), b""):
            HashFunc.update(chunk)
    return _HashFormat(HashFunc.hexdigest(), OutSize)
    

# count the distance of other node and self
def CountDistance(SelfID, OtherID):
    length = len(SelfID)
    for i in range(length):
        if SelfID[i] != OtherID[i]:
            break
    return length - i


if __name__ == '__main__':
    data = ('122331', 'pooe')
    print(GetHash(data))

