# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''

import socket


#get local IP
def GetLocalIP(self):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip