# -*- coding: UTF-8 -*-
'''
Created on 2019年9月1日

@author: danny
'''
from network.connect import Connect

serveport = 6699  #這裡亂改
node1 = Connect(serveport)


IP = '192.168.0.6'  #i need ip...
port = 6687

while True:
    # 接受控制台的输入
    data = input()
    # 对数据进行编码格式转换，不然报错
    node1.send(IP, port, data)