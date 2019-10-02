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

import logging
logger = logging.getLogger( 'loglog' )


class P2PServer(Server):
    '''
    a class inherit from Server class
    '''
    def __init__(self, ServePort=0):
        super().__init__(ServePort)
    
    
    def _CallHandle(self, connect, data, KadeNode):
        '''overwrite call handler to extend P2Phandler'''
        if not RespondHandle(connect, data, KadeNode):
            P2PHandle(connect, data, self.KadeNode)
     
            

class P2PConnect(Connect):
    '''
    a class inherit from Connect class
    '''
    def __init__(self, ServePort=0):
        '''
        Constructor
        '''
        super().__init__()
        self.server = P2PServer(ServePort)


        