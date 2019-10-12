# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
from pathlib import Path
import json
import time

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
        for node in self.GetAllNode().values():
            if post:
                self.post('', msg, node = node, content = content)
            else:
                self.chat('', msg, node = node, content = content)
            
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
    def GetPost(self):
        '''get all post in local'''
        FileNames = [f for f in Path(self.SavePath, 'post').glob('*.txt')]
        files = [json.loads(f.read_text()) for f in FileNames]
        return files
    
    @CheckError()
    def GetTmpContract(self, ID):
        '''get a tmp contract(not finish or upload yet)'''
        return self.GetRecord('contract', ID)
        
    @CheckError()
    def WriteContract(self, lender = True, transation = None, **kwargs):
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
                 }
            },
            'Transation' : transation
        }
    
    @CheckError()
    def SendContract(self, lender = True, *, ID = '', node = None, transation = None, **kwargs):
        '''
        send the contract to peer or upload to website
        
        Arguments:
            lender (bool): True if self is a lender, False to be a brower
            ID (str): Node ID you want to send to
            node: Node you want to send to 
            transation: the contract data of transation that has already save in local
            kwargs (dict): everything you want to write in the transation
        '''
        contract = self.WriteContract(lender, transation, **kwargs)
        self.send(ID, 'POST', 'contract', node = node, content = contract)
        return contract
    
    @CheckError()
    def SignMsg(self, msg):
        '''sign for a message'''
        return {
                'plaintext' : msg, 
                'cyphertext' : self.RSA.sign(msg).decode('utf-8'),
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
            msg = list(encrypter.encrypt(msg))
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
                self.secrete[ID] = DH(PK)
            except:
                return 'worng DH PK !!!!!'
            self.Whisper(ID, self.secrete[ID].DumpPublicKey().decode('utf-8'))
            # if there is a node send data to this node first
            if data != None:
                self.secrete[ID] = self.secrete[ID].GetShareKey()
                self.SecreteFresh[ID] = data['origin']['PublicKey']
            return True
        # if it's DH andget publickey from other node
        elif type(self.secrete[ID]) == DH and data != None:
            # test if the DH public key is worng
            try:
                self.secrete[ID].CreateShareKey(PK)
            except:
                return 'worng DH PK !!!!!'
            self.secrete[ID] = self.secrete[ID].GetShareKey()
            self.SecreteFresh[ID] = data['origin']['PublicKey']
            return True
        return False