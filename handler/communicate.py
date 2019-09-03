# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
def writefile(connect,data,receive): #receive代表要開啟的檔案 data是要存入的內容 
    if data != 'end' and receive != '':
        filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/Kademilia/' + receive +'.txt'
        f = open(filename,'a',encoding = 'UTF-8')
        f.write(data)
        print('finish wirte')
        f.close()
        return True
    else:
        return False

def testwrite(receive,connect,data,receiver):
    if receive == False:
        receive = True
        receiver = str(data, encoding = "utf-8")
        receive = writefile(connect,str(data, encoding = "utf-8"),receiver)
        print(receiver)
        if receive == False: #代表不再需要存入
            receiver = ''
        return receiver
    else:
        receive = writefile(connect,str(data, encoding = "utf-8"),receiver)
        if receive == False: #代表不再需要存入
            receiver = ''
        return receiver