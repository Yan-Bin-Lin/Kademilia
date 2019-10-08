# -*- coding: UTF-8 -*-
'''
Created on 2019年9月28日

@author: danny
'''
import threading
import copy
import time

from ..util.log import log
logger = log() 
    
class ReturnTread():
    '''
    a single thread class with return value
    
    Attributes:
        return_: return value of given function
    '''
    def __init__(self, fun, *args, **kwargs):
        '''
        Arguments:
            fun (function): function to run in child thread
            *args: argument for fun
            **kwargs: kwargs for fun
        '''
        self.return_= None
        self.para = (args, kwargs)
        self.fun = fun.__name__
        threading._start_new_thread(self._ReturnFun, (fun, *args), kwargs)
        
        
    def _ReturnFun(self, fun, *args, **kwargs):
        '''get copy(not reference) of return value'''
        #check if serialize object
        result = fun(*args, kwargs)
        self.return_ = copy.deepcopy(result)
        
        
    def GetResult(self):
        '''return the return value of given function'''
        return {'fun' : self.fun, 'para' : self.para, 'return_' : self.return_}

        
        
        
class TreadPool():
    '''
    A thread pool for multy return thread class
    
    Attributes:
        pool (list): all running ReturnTread class
    '''
    def __init__(self):
        self.pool = []


    def AddTask(self, fun, *args, **kwargs):
        '''
        run the function
        
        Arguments:
            fun (function): function to run in child thread
            *args: argument for fun
            **kwargs: kwargs for fun
        '''
        self.pool.append(ReturnTread(fun, *args, **kwargs))
        
        
    def WaitResult(self, wait = 10, get = True):
        '''
        waiting for return value of thread, if there is no return value after waiting time, 
        interrupt the thread
        
        Arguments:
            wait (int): max waiting time
            get (bool): return self.GetResult if True, Else None 
        '''
        now = time.time()
        while time.time() - now < wait:
            # let wait < 0 to break the loop
            wait *= -1
            for thread in self.pool:
                # if there is still some thread no finish
                if thread.GetResult()['return_'] == None:
                    # keep waiting
                    wait *= -1
                    break
        logger.debug(f"wait time is {time.time() - now}, wait is {wait}")
        return self.GetResult() if get else None
        
    
    def GetResult(self):
        '''
        return all return value and task with parameter
        
        Returns:
            tuples, each item is a dict of {'fun' : FunctionName, 'para' : (args, kwargs), 'return_' : ReturnValue}
        '''
        logger.debug(f"return the thread result {[result.GetResult() for result in self.pool]}")
        return [result.GetResult() for result in self.pool]
        
    
if __name__ == '__main__':
    
    def foo(*args, **kwargs):
        return args
    
    l = TreadPool()
    for i in range(10):
        l.AddTask(foo, i, kwargs = i)
        
    print(*l.WaitResult())