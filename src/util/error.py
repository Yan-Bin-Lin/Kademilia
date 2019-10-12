# -*- coding: UTF-8 -*-
'''
Created on 2019年10月13日

@author: danny
'''
import sys
import traceback
import test
import functools

from ..util.log import log
logger = log()

def ExceptionHadle(e):
    '''if something error happen, this function will deal it'''
    errMsg = ''
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    CallStacks = traceback.extract_tb(tb)
    for i in range(len(CallStacks)):
        lastCallStack = CallStacks[i] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        text = lastCallStack[3] #取得發生的文本
        errMsg += "\n  File \"{}\", line {}, in {}: \n    {}".format(fileName, lineNum, funcName, text)
    logger.error('Oh NO!!!!! something ERROR!!!!!!!!!!!!\nTraceback (most recent call last):' + errMsg + f"\n[{error_class}] {detail}")


def CheckError(default=None):
    '''decorator for try and catch for error'''
    def decorator(func, *args, **kwargs):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ExceptionHadle(e)
                return default
        return wrapper
    return decorator

