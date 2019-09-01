'''
Created on 2019年9月1日

@author: danny
'''
from network.connect import Connect

node1 = Connect(6687)
node1.run()

IP = '192.168.0.7'  #i need ip...

while True:
    # 接受控制台的输入
    data = input()
    # 对数据进行编码格式转换，不然报错
    node1.send(IP, data)