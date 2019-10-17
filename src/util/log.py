# -*- coding: UTF-8 -*-
'''
Created on 2019年10月6日

@author: danny
'''
from . import setup

import logging
import threading
import time

lock = threading.Lock()

class log():
    '''
    encapsulation and set up for logging to slow down
    
    Attributes:
        logger: logging.getlogger( 'loglog' )
    '''
    def __init__(self):
        self.logger =  logging.getLogger( 'loglog' )
        
        
    def error(self, msg):     
        '''logging error'''
        self.logger.error(msg)
        
        
    def warning(self, msg):     
        '''logging warning'''
        self.logger.warning(msg)
        
    
    def debug(self, msg):
        '''logging debug'''
        self.logger.debug(msg)    
    
        
    def info(self, msg):
        '''logging info'''
        threading._start_new_thread(self._info, (msg,))

    
    def _info(self, msg):
        '''extend info for wait some time'''
        lock.acquire()
        now = time.time()
        self.logger.info(msg)
        if float(setup.wait) > 0:
            print('waiting', end='')
            while time.time() - now < float(setup.wait):
                print('.', end='', flush = True)
                time.sleep(0.5)
            print('')
        lock.release()