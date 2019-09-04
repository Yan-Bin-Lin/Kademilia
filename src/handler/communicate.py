# -*- coding: UTF-8 -*-
'''
Created on 2019年9月2日

@author: danny
'''
import os

def writefile(filename,data): #receive代表要開啟的檔案 data是要存入的內容 功能是寫入內容       
    path1=os.path.abspath('..') 
    filesite = path1 + filename +'.txt'
    f = open(filesite,'a',encoding = 'UTF-8')
    f.write(data) #finish write
    f.close()

def modify(filename,data):
    path1=os.path.abspath('..') 
    filesite = path1 + filename +'.txt'
    f = open(filesite,'r')
    filelist = f.readlines()
    filelist[1] = data #決定改第幾行的部分還沒寫
    f = open(filename,'w')
    f.writelines(filelist)
    f.close()

def read(filename):
    path1=os.path.abspath('..') 
    filesite = path1 + filename +'.txt'
    f = open(filesite,'r')
    filelist = f.readlines()
    return filelist



    
def cut_mode(msg):
    return msg[0]

def cut_ID(msg):
    return msg[1:161]

def cut_data(msg):
    return msg[161:]        

def select_mode(mode,ID,filename,data):
    if mode == 1 : #append
        writefile(filename,data)
    if mode == 2 : 
        modify(filename,data)
    
        
    
