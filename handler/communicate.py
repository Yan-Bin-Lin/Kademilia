# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
def writefile(connect,data,receive): #receive代表要開啟的檔案 data是要存入的內容 
    if data != 'end' and receive != '':
        filename = '/Users/jerrylin/Desktop/105703044/專題/Kademilia-master-3/' + receive +'.txt'
        f = open(filename,'a',encoding = 'UTF-8')
        f.write(data)
        f.close()
        return True
    else:
        return False