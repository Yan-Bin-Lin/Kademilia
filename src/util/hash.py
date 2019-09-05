# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
import hashlib

# hash a data, which length is OutSize
def GetHash(data, OutSize=8):
    MD5 = hashlib.md5()
    MD5.update(data.encode(encoding='utf-8')) 
    return bin(int(MD5.hexdigest(), 16))[2:].zfill(OutSize)[:OutSize]

if __name__ == '__main__':
    data = ('122331', 'pooe')
    print(GetHash(data))