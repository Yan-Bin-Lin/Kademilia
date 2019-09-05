# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
def writefile(data,receive,transaction): #receive代表要開啟的檔案 data是要存入的內容 功能是寫入內容
    if data != 'end' and receive != '':
        if transaction >= 0:
            filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/Kademilia/' + 'temp' +'.txt'
        else:
            filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/Kademilia/' + receive +'.txt'
        f = open(filename,'a',encoding = 'UTF-8')
        if transaction >= 0:
            transaction_template = copy(transaction)
            f.write(transaction_template)
        f.write(data) #finish write
        f.close()
        return True
    elif transaction >= 0:
        return False
    else:
        return False

def testwrite(receive,data,receiver,transaction): #receive 代表是否正在寫入某個檔案 receiver代表要開啟的檔案 data是要存入的內容 功能是判段是否正在寫入 
    if receive == False:
        receive = True
        receiver = data
        receive = writefile(data,receiver,transaction)
        if receive == False: #代表不再需要存入
            receiver = ''
        return receiver
    else:
        receive = writefile(data,receiver,transaction)
        if receive == False: #代表不再需要存入
            receiver = ''
        return receiver

def modify(receive,line,data):
    filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/Kademilia/' + receive +'.txt'
    f = open(filename,'r')
    filelist = f.readlines()
    filelist[line] = data
    f = open(filename,'w')
    f.writelines(filelist)
    f.close()

def copy(transaction):
    filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/Kademilia/transaction.txt'
    f = open(filename,'r')
    filelist = f.readlines()
    return filelist[transaction]