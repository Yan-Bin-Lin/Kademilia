# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
import sys
import traceback

from ..network.connect import Connect
from ..network.server import Server
from ..handler.handler import RespondHandle
from .P2Phandler import P2PHandle

from ..util.log import log
logger = log()

from ..util.error import CheckError

class P2PServer(Server):
    '''
    a class inherit from Server class
    '''
    @CheckError()
    def __init__(self, ServePort=0):
        super().__init__(ServePort)
    
    @CheckError()
    def CallHandle(self, connect, data, KadeNode):
        '''overwrite call handler to extend P2Phandler'''
        logger.info(f'P2P server receive data, data is {data}')
        if not RespondHandle(connect, data, KadeNode):
            logger.info(f'start to call P2PHandle...')
            P2PHandle(connect, data, self.KadeNode)


class P2PConnect(Connect):
    '''
    a class inherit from Connect class
    '''
    @CheckError()
    def __init__(self, ServePort=0):
        '''
        Constructor
        '''
        self.server = P2PServer(ServePort)
        self.clients = {}
        