# -*- coding: UTF-8 -*-
'''
Created on 2019年9月4日

@author: danny
'''
import ast

from .file import *
from .communicate import *

# main handler here
def MainHandle(connect, data):
    print('i got handle')
    print(f'data is {data}')
    #刪除下面
    connect.sendall(b'ok')
    #刪除上面
    # change string to dict
    '''
    data = ast.literal_eval(data)
    instruction = data.get('instruction', ping)
    from_ = data.get('from_', '10101010')
    '''
    # if condition here
    #if instruction.find('ping'):
    if data.find(b'ping'):
        pass
        '''
        # set to no block
        connect.setblocking(0) 
        print(request('ok'))
        '''