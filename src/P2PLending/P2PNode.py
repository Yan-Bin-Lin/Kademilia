# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
from pathlib import Path
import json
import time
import ast

from ..node.KadeNode import KadeNode
from ..crypto.DHKeyExchange import DH
from ..crypto.AEAD import AEAD
from .P2Pnetwork import P2PConnect
from ..util.hash import GetHash
from ..util.error import CheckError

from ..util.log import log
logger = log()

class P2PNode(KadeNode):
    '''
    This is the main node application in p2p lending inheribit from Kademlia node
    '''
    @CheckError()
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super().__init__(*args, **kwargs)
        self.secrete = {}
        self.SecreteFresh = {}
        
    @CheckError()
    def WebInit(self):
        self.web = P2PConnect()

    @CheckError()
    def chat(self, ID, msg, *, node = None, content = ''):
        '''
        send a message to other node
        
        Arguments:
            ID (bstr): the ID of node the msg send to
            msg: msg need to be send
            node (NodeData): a dict of NodeData of node the msg send to
        '''
        self.send(ID, 'POST', 'message', msg, node = node, content = content)
        
    @CheckError()
    def broadcast(self, msg, content = '', post = True):    
        '''
        broadcast a post or msg to all node in bucket
        
        Arguments:
            msg: msg need to be send
            post (bool): True for post, else chat  
        '''
        nodes = [list(v.values()) for v in self.GetAllNode().values()]
        for node in nodes:
            for n in node:
                if post:
                    self.post('', msg, node = n, content = content)
                else:
                    self.chat('', msg, node = n, content = content)
            
    @CheckError()
    def post(self, ID, msg, *, node = None, content = ''):
        '''
        send a post to other node
        
        Arguments:
            ID (bstr): the ID of node the msg send to
            msg: msg need to be send
            node (NodeData): a dict of NodeData of node the msg send to
        '''
        self.send(ID, 'POST', 'post', msg, node = node, content = content)
        
    @CheckError()
    def GetChat(self, peer):
        '''get a chat record'''
        return self.GetRecord('chat', peer)
        
    @CheckError()
    def GetRecord(self, type_, peer):
        '''
        get the chat(or contract) record file in local of the peer chat with

        Arguments:
            type_: should be 'chat' or 'contract'
            peer: the record with a peer
        '''
        path = Path(self.SavePath, type_, peer + '.txt')
        if path.exists():
            file = json.loads(path.read_text())
            logger.debug(f'In GetRecord, file is {file}')
            return file
        else:
            return None
        
    @CheckError()
    def GetPost(self, ID = None):
        '''
        get all post in local or from another node
        
        Arguments:
            ID: default None, if give an ID, the function will get post from specify node else just get from local
        '''
        if ID == None:
            FileNames = [f for f in Path(self.SavePath, 'post').glob('*.txt')]
            files = [json.loads(f.read_text()) for f in FileNames]
            return files
        else:
            result = self.request(ID, 'GET', 'post')[0]
            result = ast.literal_eval(result)
            return result

    @CheckError()
    def DelPost(self, time, ID = None):
        '''     
        delete a post
        
        Arguments
            ID (bstr): the ID of node you want him delete the post, if None, will delete the post in local
            time (float): linux time of the post you want to delete
        '''
        if ID == None:
            
            FileNames =  [f for f in Path(self.SavePath, 'post').glob('*.txt')]
            files = [json.loads(f.read_text()) for f in FileNames]
            
            delete = False
            
            # search for the post
            for i in range(len(files)):
                for j in range(len(files)):
                    if files[i][j]['time'] == time:
                        delete = True
                        break
        
                if delete:
                    break
            
            if delete:
                del files[i][j]
            
                for post in files:
                    folder = Path(self.SavePath, "post")
            
                    folder.mkdir(parents=True, exist_ok=True) 
                    file = folder / (post[0]['from']['ID'] + '.txt')
                    file.write_text(json.dumps(post))
    
        else:
            self.send(ID, 'DELETE', 'post', str(time))
            
            
    
    @CheckError()
    def GetTmpContract(self, ID):
        '''get a tmp contract(not finish or upload yet)'''
        return self.GetRecord('contract', ID)
        
    @CheckError()
    def WriteContract(self, lender = True, transation = None, other = '', **kwargs):
        '''
        write the contract
        
        Arguments:
            lender (bool): True if self is a lender, False to be a brower
            kwargs (dict): everything you want to write in the transation        
        '''
        transation = kwargs if transation == None else transation
        return {
            'Trader' : {
                'lender' if lender else 'brower' : {
                    'node' : self.NodeData.GetData(),
                    'time' : time.time(),
                    'sign' : {
                        'signature' : self.RSA.sign(str(transation)).decode('utf-8'), 
                        'message' : str(transation),
                        'public_key' : self.NodeData.GetByteStringPubKey()
                    }
                 },
                'brower' if lender else 'lender' : other
            },
            'Transation' : transation
        }
    
    @CheckError()
    def SendContract(self, lender = True, *, ID = '', node = None, transation = None, other = '', **kwargs):
        '''
        send the contract to peer or upload to website
        
        Arguments:
            lender (bool): True if self is a lender, False to be a brower
            ID (str): Node ID you want to send to
            node: Node you want to send to 
            transation: the contract data of transation that has already save in local
            kwargs (dict): everything you want to write in the transation
        '''
        contract = self.WriteContract(lender, transation, other, **kwargs)
        self.send(ID, 'POST', 'contract', node = node, content = contract)
        return contract
    
    @CheckError()
    def SignMsg(self, msg):
        '''sign for a message'''
        cyphertext = self.RSA.sign(msg).decode('utf-8')
        logger.warning(f"{self.ID} 開始簽章， 文本為 {msg}, 簽章為 {cyphertext}")
        return {
                'plaintext' : msg, 
                'cyphertext' : cyphertext,
                'public_key' : self.NodeData.GetByteStringPubKey()
            }
        
    @CheckError()
    def EncryptMsg(self, ID, msg):
        '''encrypt and sign for a secrete message'''
        SecreteKey = self.secrete.get(ID, None)
        # if secrete key not initial yet
        if SecreteKey == None or type(SecreteKey) == DH:
            sign = self.SignMsg(msg)            
        # if secrete key exist
        else: 
            sign = self.SignMsg(GetHash(msg))
            encrypter = AEAD()
            encrypter.NewKey(self.secrete[ID])
            cypher = list(encrypter.encrypt(msg))
            logger.warning(f"{self.ID} 開始進行加密， 文本為 {msg}， 密文為 {cypher[0]} ，參數為 {cypher[1:]}")
            msg = cypher
        return {
            'sign' : sign,
            'msg' : msg 
        }

    @CheckError()
    def Whisper(self, ID, msg = '', *, node = None):
        '''
        send encrypt msg, must initial(call SecreteInit) first
        '''
        self.send(ID, 'POST', 'secrete', node = node, content = self.EncryptMsg(ID, msg))
        
    @CheckError()
    def SecreteInit(self, ID, *, data = None):
        '''
        initial for DH share key for secrete chat
        
        Returns:
            bool: True for this secrete key need to initial, False for secrete key already done
        '''
        if data != None:
            if data['content']['sign']['plaintext'].find('-----BEGIN PUBLIC KEY-----') == -1:
                return False
            PK = self.RSA.LoadPublicKey(data['content']['sign']['plaintext'].encode('utf-8'))
        else:
            PK = None
        
        # if there is no DH exist 
        if self.secrete.get(ID, None) == None:
            # test if the DH public key is worng
            try:
                logger.warning(f"{self.ID} 開始建構自己的Diffie-Hellman")
                self.secrete[ID] = DH(PK)
            except:
                logger.warning(f"建構錯誤!!  'worng DH PK !!!!!'")
                return 'worng DH PK !!!!!'
            logger.warning(f"{self.ID} 傳送 Diffie-Hellman 公鑰給 {ID}")
            self.Whisper(ID, self.secrete[ID].DumpPublicKey().decode('utf-8'))
            # if there is a node send data to this node first
            if data != None:
                self.secrete[ID] = self.secrete[ID].GetShareKey()
                logger.warning(f"{self.ID} 成功建構出 share key {self.secrete[ID]}")
                self.SecreteFresh[ID] = data['origin']['PublicKey']
            return True
        # if it's DH andget publickey from other node
        elif type(self.secrete[ID]) == DH and data != None:
            # test if the DH public key is worng
            try:
                logger.warning(f"{self.ID} 開始建構自己的 share key")
                self.secrete[ID].CreateShareKey(PK)
            except:
                logger.warning(f"建構錯誤!!  'worng DH PK !!!!!'")
                return 'worng DH PK !!!!!'
            self.secrete[ID] = self.secrete[ID].GetShareKey()
            self.SecreteFresh[ID] = data['origin']['PublicKey']
            logger.warning(f"{self.ID} 成功建構出 share key {self.secrete[ID]}")
            return True
        return False