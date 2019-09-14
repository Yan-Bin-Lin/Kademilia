'''
Created on 2019年9月1日

@author: danny
'''
import pickle
import json
from pathlib import Path

from .KBucket import KBucket
from .NodeData import NodeData
from ..crypto.RSASign import RSA
from ..network.connect import Connect
from ..util.hash import *
from ..handler.respond import *
from ..handler.ask import Ask


# a single kade node
class KadeNode():
    '''
    a kadenode should content node data
    node data should content IP, port, PublicKey, ID
    '''
    def __init__(self, **kwargs):
        self.RSA = RSA()
        self.web = Connect()
        self.address = self.web.GetServeAddress()
        self.ID = kwargs.get('ID', GetHash(self.address[0] + str(self.address[1])))#random ID here
        self.NodeData = NodeData(self.address, self.RSA.GetPublicKey(), self.ID)
        # routing table content all Kbucket, initial create empty table, key = distance, value = bucket
        self.table = {i : KBucket(self.NodeData) for i in range(1, 128)}
        self.SavePath = 'Save'
        # start for connect
        self.run()
        # create bucket
        node = kwargs.get('node', None)
        if node != None:
            self.update(node, getbucket = True)
        
        
    # add new node to bucket in the table    
    def update(self, node, getbucket = False):
        print('update ID = ' + node['ID'])
        distance = CountDistance(self.ID, node['ID'])
        self.table[distance].AddNode(node)
        # get bucket of the node
        if getbucket:
            self.GetBucket()
        
    
    # request to other node
    # blocking
    def request(self, node, instruct):
        #self.web.send(node.GetAddress(), instruct)
        self.web.request(node.GetAddress(), instruct)
        # call function to get the node by handler here...
        # node = ...
          
          
    # send to other node
    # no blocking
    def send(self, instruct, node, connect = None):
        self.web.send(instruct, node, connect)

    
    # get a node in the distance bucket, 
    # if ID is not none will count distance with ID and self ID and return the same distance node
    # return ( nodedata, socket )
    def GetDistanceNode(self, distance, ID = None, *, except_ = False):
        return (self.table[distance].GetNode(except_ = except_) if ID == None
                    else self.table[CountDistance(self.ID, ID)].GetNode(except_ = except_))
        
    
    # if no argument is given, search for a exist node
    # get a node data, if the node not found, will return a same distance node if recurive is True
    # return ( nodedata, socket )
    def GetNode(self, *, ID = None, recuricive = True):
        if ID != None:
            distance = CountDistance(self.ID, ID)
            result = self.table[distance].GetNode(ID)
            if result == None and recuricive:
                return self.GetDistanceNode(distance)
        else:
            for distance, bucket in self.table.items():
                if self.table[distance].length() != 0:
                    result = self.table[distance].GetNode()
                    if result != None:
                        break            
        return result
    
            
    # find a node
    def LookUp(self, ID, data = {}):
        result = self.GetNode(ID = ID, recuricive = False)
        print(f' LookUp result is {result}')
        if result == None:
            print('LookUp: ID not in local bucket, strart to send to search')
            # if node not in table, ask other node in same distance to find the target node
            # SearchNode = [node, socket] or None
            SearchNode = self.GetDistanceNode(0, ID)            
            print(f' SearchNode result is {SearchNode}')
            if SearchNode != None:
                Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, connect = SearchNode, destination = {'ID' : ID})
        elif data != {}:
            Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, connect = result)
        return result
        
    
    # get the bucket of any node or given ID node
    def GetBucket(self, ID = None):
        connect = self.GetNode(ID = ID, recuricive = False)        
        # get a node, start to ask for bucket
        if connect != None:
            result = Ask(self.NodeData.GetData(), 'request', 'GET', 'bucket', connect = connect)
            print(f'nodes = {result}')
            # get a dict of other table
            if result != None:
                nodes = json.loads(result[0])
                for node in nodes:
                    self.update(node)
                print('GetBucket Success!!!!!!')
                return connect[0]['ID']
        return None
        
    
    # save node data
    def save(self, name = '', json = False):
        name = (self.ID if name == '' else name) + '.txt'
        Path(self.SavePath).mkdir(parents=True, exist_ok=True) 
        folder = Path(self.SavePath)
        file = folder / name
        with file.open('wb') as f:
            pickle.dump(self.NodeData.GetData(), f)
        print(file.resolve())
            
        
    # update a file to network
    def UpLoadFile(self, file, data = {}):
        if data == {}:
            HashCode = GetHash(file)
            content = {'FileID' : HashCode, 'saver' : [self.NodeData.GetData()], 'file' : file}
            destination = {'ID' : HashCode}
        else:
            HashCode = data['instruct'][2]
            content = data['content']
            destination = data['destination']
        print(f'HashCode = {HashCode}')
        node = self.GetNode(ID = HashCode)
        if node != None:
            Ask(self.NodeData.GetData(), 'send', 'POST', 'file', HashCode, connect = node,
                destination = destination, data = data, content = content)
        else:
            return 'something error'
        
             
    # Get a file from web
    def GetFile(self, HashCode, data = {}):
        path = Path(self.SavePath, 'file', HashCode + '.txt')
        print(f'search: {path}')
        # strat to search file from web
        if not path.exists():
            # this request is not handle by too many node, this request can keep search
            if data != {}:
                # this request is handle by too many node
                if len(data['path']) > 10:
                    return None
                # if target file not in target node, hash the HashCodeone more time and keep search
                if data['instruct'][2] == self.ID:
                    data['instruct'][2] = GetHash(data['instruct'][2])
                    HashCode = data['instruct'][2]
    
            # send to other node to search
            node = self.GetNode(ID = HashCode)
            if node == None:
                return None
    
            Ask(self.NodeData.GetData(), 'send', 'GET', 'file', HashCode, connect = node, data = data, content = {'FileID' : HashCode})
            return None
        
        else:
            file = json.loads(path.read_text())
            print(f'In GetFile, file is {file}')
            return file
    
    
    def run(self):
        # giveout self instance to server which will call handler to handle
        self.web.server.KadeNode = self
        self.web.run()
        
    
    def closs(self):
        pass