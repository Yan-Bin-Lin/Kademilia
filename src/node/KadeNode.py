'''
Created on 2019年9月1日

@author: danny
'''
import pickle
from pathlib import Path
import time
import threading

from .KBucket import KBucket
from .NodeData import NodeData
from .RouteTable import RouteTable
from ..crypto.RSASign import RSA
from ..network.connect import Connect
from ..util.hash import *
from ..handler.respond import *
from ..handler.ask import Ask
from ..util.error import CheckError

from ..util.log import log
logger = log()
# a single kade node
class KadeNode():
    '''
    Kademlia 最基礎結構，每個KadeNode代表一個peer，
       作為網路通信的一員
    
    Attributes:
        RSA: a RSA class use for rsa method
        web: a connect class content server and client socket for connect
        address: a tuple of (IPAddress, port) of server socket bind
        ID: the only ID of this node in the network
        NodeData: a NodeData class present this node, conntent RSA publicKey, address and ID
        table: a dict with key i: subtree split of the network and value:the bucket class of NodeData containt
             the route table of this node
        Savepath: path for the file save
        lock: lock for write file
    '''
    @CheckError()
    def __init__(self, **kwargs):
        self.RSA = RSA()
        self.WebInit()
        self.address = self.web.GetServeAddress()
        self.ID = kwargs.get('ID', GetHash(self.address[0] + str(self.address[1])))#random ID here
        self.NodeData = NodeData(self.address, self.RSA.GetPublicKey(), self.ID)
        # routing table content all Kbucket, initial create empty table, key = distance, value = bucket
        self.table = RouteTable(self.NodeData)
        self.SavePath = self.ID + '_Save'
        self.lock = threading.Lock()
        # start for connect
        self.run()
        logger.warning(f'node {self.ID} 上線了!!!')
        # create bucket
        if kwargs.get('node', None) != None:
            self.update(kwargs['node'], getbucket = True)
        
        
    @CheckError()
    def WebInit(self):
        self.web = Connect()
            
    @CheckError()
    def update(self, node, getbucket = False):
        '''add new node to bucket in the table'''
        if node['ID'] == self.ID:
            return
        self.table.AddNode(node)
        # get bucket of the node
        if getbucket:
            self.GetBucket(node['ID'])
        
    
    # request to other node
    # blocking
    @CheckError()
    def request(self, ID, *instruct, node = None, content = '', destination = None):
        if node == None:
            node = self.GetNode(ID, closest = False)
        return self.web.Ask(self.NodeData.GetData(), 'request', *instruct,  address = node['address'], content = '', destination = None) if node != None else None
          
          
    # send to other node
    # no blocking
    @CheckError()
    def send(self, ID, *instruct, node = None, content = '', destination = None):
        if node == None:
            node = self.GetNode(ID, closest = False)
            if node == []:
                # no such node in local, start to lookup
                self.LookUp(ID)
                return
            else:
                node = node[0]
        self.web.Ask(self.NodeData.GetData(), 'send', *instruct, address = node['address'], content = content, destination = destination)
        
    
    # get a node in the distance bucket, 
    # if ID is not none will count distance with ID and self ID and return the same distance node
    # return ( nodedata, socket )
    @CheckError()
    def GetDistanceNode(self, distance, ID = None, *, recursive = True, ExceptList = None):
        return (self.table[distance].GetNode(recursive = recursive, ExceptList = ExceptList) if ID == None
                    else self.table[CountDistance(self.ID, ID)].GetNode(ID, recursive = recursive, ExceptList = ExceptList))
        
    
    # if no argument is given, search for a exist node
    # get a node data, if the node not found, will return a same distance node if recurive is True
    # return ( nodedata, socket )
    @CheckError()
    def GetNode(self, ID, *, closest = True, ping = True, data = None, ExceptList = None):
        '''
        get a node data, if the node not found, will return a same distance node if closest is True
        '''
        return self.table.GetNode(ID, closest = closest, ping = ping, data = data, ExceptList = ExceptList)
        
    @CheckError()
    def LookUp(self, ID, data = None):
        '''
        find a node from network
        
        Args:
            ID: the node ID to find
            data: the request data from other node, default = {}
        '''
        logger.debug(f" in lookup data is {data}")
        logger.warning(f'node {self.ID} 開始查找 node {ID} ， 雙方距離差距為 {int(CountDistance(self.ID, ID), 2)}' + 
                       f'，位於bucket {self.table._CheckDistanceIndex(ID)}')
        
        result = self.GetNode(ID, data = data)
        
        data = {} if data == None else data
        if len(result) == 0:
            logger.warning(f'no node has find, 回傳  {data.get("origin", {}).get("ID", "")} 查找結果  "nothing"')
            # no node has find
            return ''
        
        elif result[0]['ID'] != ID or data.get('destination', {}).get('address', False):
            # the node not in bucket, start to search
            logger.warning(f'node {self.ID} 準備向 {[r["ID"] for r in result]} 發出查找 node {ID} 的請求')
            for r in result:
                self.web.Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, address = r['address'],
                    destination = data.get('destination', {'ID' : ID}))       
             
        elif data == {}:
            # return the correct node
            logger.warning(f'node {ID} 存於本地， 回傳{result[0]}')
            return result[0]
        
        else:
            logger.warning(f'node {ID} 存於本地， 要求node {result[0]} 聯繫 node {data["origin"]["ID"]}')
            self.web.Ask(self.NodeData.GetData(), 'send', 'GET', 'node', ID, data = data, address = result[0]['address'])
        
        logger.warning(f'回傳  {data.get("origin", {}).get("ID", "")} 查找結果 {[r["ID"] for r in result]}')
        return result
       
    @CheckError()
    def GetBucket(self, ID = None):
        '''    
        initial to fullfill self bucket by ask other node to find self
        '''
        nodes = self.GetNode(ID)     
        logger.warning(f'node {self.ID} 開始向 {[node["ID"] for node in nodes]}， 請求find self')
        # get a node, start to ask for bucket
        for node in nodes:
            self.web.Ask(self.NodeData.GetData(), 'send', 'GET', 'node', self.ID, address = node['address'], destination = self.NodeData.GetData())       

    
    # save node data
    @CheckError()
    def save(self, name = '', json = False):
        '''save self NodeData to a file'''
        name = (self.ID if name == '' else name) + '.txt'
        Path(self.SavePath).mkdir(parents=True, exist_ok=True) 
        folder = Path(self.SavePath)
        file = folder / name
        with file.open('wb') as f:
            pickle.dump(self.NodeData.GetData(), f)
        logger.debug(file.resolve())
            
    @CheckError()
    def UpLoadFile(self, file, data = None, *, FilePath = '', TargetHash = ''):
        '''
        upload a file to network
        
        Args:
            file: file to upload, must be a hashable value
            data: the request data from other node, default = {}
        '''
        # initial for kwargs
        kwargs = {}
        if data != None:
            ExceptList = [saver[0]['ID'] for saver in data['content']['saver'] if (time.time() - saver[1]) < 86400]
            HashCode = data['instruct'][2]
            logger.debug(f"ExceptList = {ExceptList}, data['content']['saver'] = {data['content']['saver']}")    
        else:
            ExceptList = list()
            HashCode = GetHashFile(Path(FilePath)) if FilePath != '' else GetHash(file)
            kwargs['content'] = {'FileID' : HashCode, 'saver' : [[self.NodeData.GetData(), time.time()]], 'file' : file}
            kwargs['destination'] = {'ID' : TargetHash if TargetHash != '' else HashCode}
            
        logger.debug(f'HashCode = {HashCode}')    
        TargetHash = TargetHash if TargetHash != '' else HashCode
        nodes = self.GetNode(TargetHash, data = data, ExceptList = ExceptList)
        logger.warning(f'node {self.ID} 開始上傳檔案到網路，將資料傳給node {[node["ID"] for node in nodes]}')            
        for node in nodes:
            self.web.Ask(self.NodeData.GetData(), 'send', 'POST', 'file', TargetHash, address = node['address'],
                data = data, **kwargs)
        
        if data == None:
            data = {}
        logger.warning(f'回傳  {data.get("origin", {}).get("ID", "")}， node {[[node["ID"], 0] for node in nodes]} 為下一個儲存對象')
        return [[node, 0] for node in nodes]
        
    @CheckError()
    def GetFile(self, HashCode, data = None):
        '''
        Get a file from network
        
        Args:
            HashCode: the Hashcode of file content
            data: the request data from other node, default = {}
        '''
        data = {} if data == None else data
        logger.warning(f'node {self.ID} 收到GET file請求，開始查找本地有無該檔案')
        path = Path(self.SavePath, 'file', HashCode + '.txt')
        logger.debug(f'search: {path}')
        # strat to search file from web
        if not path.exists():
            logger.warning(f'本地查無該檔案，向其他節點查找')
            # send to other node to search
            nodes = self.GetNode(HashCode, data = data)
            logger.warning(f'向 {[node["ID"] for node in nodes]} 發出GET file 請求')
            for node in nodes:
                self.web.Ask(self.NodeData.GetData(), 'send', 'GET', 'file', HashCode, address = node['address'], data = data, content = {'FileID' : HashCode})
            return nodes
        
        else:
            file = json.loads(path.read_text())
            logger.warning(f'node {self.ID} 擁有該檔案 {file}，回傳該檔')
            logger.debug(f'In GetFile, file is {file}')
            return file
    
    @CheckError()
    def GetAllNode(self):
        '''
        get all NodeData in table, return list of node
        
        Returns:
            list with all node in this
        '''
        result = {}
        for i in range(128):
            if len(self.table.table[i].bucket) > 0:
                result.update({i : self.table.table[i].bucket})
        return result
            
    @CheckError()
    def run(self):
        # giveout self instance to server which will call handler to handle
        self.web.server.KadeNode = self
        self.web.run()
        
    @CheckError()
    def closs(self):
        pass