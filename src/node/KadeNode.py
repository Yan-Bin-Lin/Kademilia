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
from ..handler.ask import Ask, Reject
import logging
logger = logging.getLogger( 'loglog' )

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
        if kwargs.get('node', None) != None:
            self.update(kwargs['node'], getbucket = True)
        logger.info(f'node {self.ID} 上線了!!!')
        
        
    # add new node to bucket in the table    
    def update(self, node, getbucket = False):
        if node['ID'] == self.ID:
            return
        logger.debug(f'node {self.ID} 開始將 node {node["ID"]} 資料跟新於本地bucket中')
        distance = CountDistance(self.ID, node['ID'])
        self.table[distance].AddNode(node)
        # get bucket of the node
        if getbucket:
            self.GetBucket(node['ID'])
        
    
    # request to other node
    # blocking
    def request(self, ID, *instruct):
        result = self.GetNode(ID)
        Ask(self.NodeData.GetData(), 'request', instruct, connect = result)
          
          
    # send to other node
    # no blocking
    def send(self, ID, instruct):
        result = self.GetNode(ID)
        Ask(self.NodeData.GetData(), 'request', instruct, connect = result)
        
    
    # get a node in the distance bucket, 
    # if ID is not none will count distance with ID and self ID and return the same distance node
    # return ( nodedata, socket )
    def GetDistanceNode(self, distance, ID = None, *, recursive = True, ExceptList = []):
        return (self.table[distance].GetNode(recursive = recursive, ExceptList = ExceptList) if ID == None
                    else self.table[CountDistance(self.ID, ID)].GetNode(ID, recursive = recursive, ExceptList = ExceptList))
        
    
    # if no argument is given, search for a exist node
    # get a node data, if the node not found, will return a same distance node if recurive is True
    # return ( nodedata, socket )
    def GetNode(self, *, ID = None, recursive = True, data = {}):
        logger.debug(f'data["fail"] = {data.get("fail", None)}')
        ExceptList = data.get('fail', [])
        logger.debug(f'In GetNode ... ExceptList = {ExceptList}')
        if ID != None:
            distance = CountDistance(self.ID, ID)
            result = self.table[distance].GetNode(ID, recursive = recursive, ExceptList = ExceptList)
            if result == None and recursive:
                return self.GetDistanceNode(distance, ExceptList = ExceptList)
        else:
            for distance, bucket in self.table.items():
                if self.table[distance].length() != 0:
                    result = self.table[distance].GetNode(ExceptList = ExceptList)
                    if result != None:
                        break            
        return result
    
            
    # find a node
    def LookUp(self, ID, data = {}):
        logger.info(f'node {self.ID} 開始查找 node {ID} ， 雙方距離差距為 {CountDistance(self.ID, ID)}')
        result = self.GetNode(ID = ID, recursive = False, data = data)
        logger.debug(f' LookUp result is {result}')
        if result == None:
            logger.info(f'查找結果： node {ID} 並不在 node {self.ID} 的 bucket中，開始向同距離的其他node查找')
            # if node not in table, ask other node in same distance to find the target node
            # SearchNode = [node, socket] or None
            SearchNode = self.GetDistanceNode(0, ID, ExceptList = data.get('fail', []))  
            if SearchNode != None:
                logger.info(f'node {self.ID} 準備向  node {SearchNode[0]["ID"]} 發出查找 node {ID} 的請求')
                Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, connect = SearchNode, destination = {'ID' : ID})
            else:
                logger.info(f'同距離節點不存在或無法回應，請求拒絕，即將回退資料')
                Reject(self.NodeData.GetData(), data)
        elif data != {}:
            logger.info(f'查找結果： node {ID} 存在於 node {self.ID} 的 bucket中，開始請求node {ID} 聯繫 node {data["origin"]["ID"]}')
            Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, connect = result)
        else:
            logger.info(f'node {ID} 存於本地，無需向網路查找')
        return result
        
    
    # get the bucket of any node or given ID node
    def GetBucket(self, ID = None):
        connect = self.GetNode(ID = ID, recursive = False)        
        # get a node, start to ask for bucket
        if connect != None:
            logger.info(f'node {self.ID} 開始向 node {connect[0]["ID"]}， 請求bucket')
            result = Ask(self.NodeData.GetData(), 'request', 'GET', 'bucket', connect = connect)
            logger.debug(f'nodes = {result}')
            # get a dict of other table
            if result != None:
                logger.info(f'node {self.ID} 成功取得bucket，開始跟新到己方bucket')
                nodes = json.loads(result[0])
                for node in nodes:
                    self.update(node)
                logger.info(f'node {self.ID} 跟新bucket成功')
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
        logger.debug(file.resolve())
            
        
    # update a file to network
    def UpLoadFile(self, file, data = {}):
        if data == {}:
            HashCode = GetHash(file)
            content = {'FileID' : HashCode, 'saver' : [[self.NodeData.GetData(), 1]], 'file' : file}
            destination = {'ID' : HashCode}
        else:
            HashCode = data['instruct'][2]
            content = data['content']
            destination = data['destination']
        logger.debug(f'HashCode = {HashCode}')
        node = self.GetNode(ID = HashCode, data = data)
        if node != None:
            logger.info(f'node {self.ID} 開始上傳檔案到網路，將資料傳給node {node[0]["ID"]}')            
            Ask(self.NodeData.GetData(), 'send', 'POST', 'file', HashCode, connect = node,
                destination = destination, data = data, content = content)
        else:
            logger.info(f'node {self.ID} 沒有其他節點可以通往目標，請求拒絕')
            Reject(self.NodeData.GetData(), data)
        
             
    # Get a file from web
    def GetFile(self, HashCode, data = {}):
        logger.info(f'node {self.ID} 收到GET file請求，開始查找本地有無該檔案')
        path = Path(self.SavePath, 'file', HashCode + '.txt')
        logger.debug(f'search: {path}')
        # strat to search file from web
        if not path.exists():
            logger.info(f'本地查無該檔案，即將判斷是否要向其他節點查找')
            # this request is not handle by too many node, this request can keep search
            if data != {}:
                # this request is handle by too many node
                if len(data['path']) > 10:
                    logger.info(f'這份資料已經超過轉手上限，請求拒絕')
                    return None
                # if target file not in target node, hash the HashCodeone more time and keep search
                if data['instruct'][2] == self.ID:
                    data['instruct'][2] = GetHash(data['instruct'][2])
                    HashCode = data['instruct'][2]
    
            # send to other node to search
            node = self.GetNode(ID = HashCode, data = data)
            if node == None:
                Reject(self.NodeData.GetData(), data)
           
            logger.info(f'向node {node[0]["ID"]} 發出GET file 請求')
            Ask(self.NodeData.GetData(), 'send', 'GET', 'file', HashCode, connect = node, data = data, content = {'FileID' : HashCode})
            return None
        
        else:
            logger.info(f'node {self.ID} 本地擁有該檔案，回傳該檔')
            file = json.loads(path.read_text())
            logger.debug(f'In GetFile, file is {file}')
            return file
    
    
    def run(self):
        # giveout self instance to server which will call handler to handle
        self.web.server.KadeNode = self
        self.web.run()
        
    
    def closs(self):
        pass