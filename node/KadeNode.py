'''
Created on 2019年9月1日

@author: danny
'''

from ..network.connect import Connect
from .KBucket import bucket

class KadeNode():
    def __init__(self):
        port = 6687
        self.web = Connect(port)
        self.Kbucket = {}
    
    def run(self):
        self.web.run()
        
    
    def closs(self):
        pass
    
    