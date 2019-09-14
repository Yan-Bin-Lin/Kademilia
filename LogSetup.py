# -*- coding: UTF-8 -*-
'''
Created on 2019年9月15日

@author: danny
'''
import logging
#from logging.handlers import TimedRotatingFileHandler
#請你給我一個 Log 的分身，他的名字叫做.... loglog (function 的名稱)！！
logger = logging.getLogger( 'loglog' )

def some_method():
    
    from KadeRejectTest import RejectTest 
    RejectTest()


def main():
    #設定這個log 分身他要處理的情報等級
    logger.setLevel(logging.DEBUG)
    #關於 log 將要輸出的檔案，請你按照下面的設定，幫我處理一下
    #fh = logging.FileHandler('receive.log', 'w', 'utf-8')
    #設定這個檔案要處理的情報等級，只要是 INFO 等級或以上的就寫入檔案
    #fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    #關於 console(也就是cmd 那個黑黑的畫面)，請你按照下面的設定，幫我處理一下
    ch = logging.StreamHandler()
    #設定 Console 要處理的情報等級，只要是 DEBUG 等級的就印出來
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    # log 印出來的格式
    formatter = logging.Formatter('%(asctime)s %(module)s. line:%(lineno)d -%(levelname)s- %(message)s')
    #將 印出來的格式和 File Handle, Console Handle 物件組合在一起
    #fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    #加上這個!!!!!每天深夜換檔案，receive.log 當然可以使用日期當作檔名，就自己去玩拉！
    #logHandler = TimedRotatingFileHandler("receive.log",when="midnight")
    # add the handlers to the logger
    #log 的分身組合 File Handle 和 Console Handle
    #logger.addHandler(fh)
    logger.addHandler(ch)
    #logger.addHandler(logHandler) #加上這個!!!!!

    some_method()

if __name__ == '__main__':
    main()   


'''     
import logging
logger = logging.getLogger( 'my_module' )
def some_method():
    logger.debug('begin of some_method')
def main():

    # Produce formater first
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup Handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    # Setup Logger
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    some_method()

if __name__ == '__main__':
    main()
'''