# -*- coding: UTF-8 -*-
'''
Created on 2019年10月2日

@author: danny
'''
import json
from pathlib import Path 
import time

from ..crypto.AEAD import AEAD
from ..util.log import log
from ..node.KadeNode import KadeNode
from cv2 import instr
logger = log()


def _SaveMsg(data, KadeNode, type_):
    name = data['origin']['ID'] + '.txt'
    folder = Path(KadeNode.SavePath, type_)
    
    KadeNode.lock.acquire()
    record = {'msg' : data['instruct'][2], 'time' : time.time(), 'from' : data['origin']}

    # cirtical section
    folder.mkdir(parents=True, exist_ok=True) 
    file = folder / name
    
    if not file.exists():
        # save the file in local
        file.write_text(json.dumps([record]))
    
    else:
        OriginFile = json.loads(file.read_text())
        # append to the tail
        OriginFile.append(record)
        file.write_text(json.dumps(OriginFile))
    # cirtical section
    
    KadeNode.lock.release()


def ReplyPostPost(data, KadeNode):
    '''reply to a post request'''
    logger.warning(f"node {data['path'][-1]['ID']} send a post to you, the post is: \n\t {data['instruct'][2]}")
    _SaveMsg(data, KadeNode, 'post')
    

def ReplyPostMsg(data, KadeNode):
    '''reply to chat request'''
    logger.warning(f"node {data['path'][-1]['ID']} send a message to you, the message is: \n\t {data['instruct'][2]}")
    _SaveMsg(data, KadeNode, 'chat')


def ReplyPostContract(data, KadeNode):
    '''reply to a contract request'''
    peer = data['content']['Trader'].get('lender', data['content']['Trader'].get('brower', None))['sign']
    logger.warning(f"{KadeNode.ID} 開始驗證來自 {data['path'][-1]['ID']}的簽章 ， 簽章為 {peer['signature']}，文本為 {peer['message']}")
    if KadeNode.RSA.verify(
                    KadeNode.RSA.LoadBytePublicKey(peer['public_key'].encode('utf-8')), 
                    peer['signature'], peer['message']):
        logger.warning(f"node {data['path'][-1]['ID']} send a contract to you, the contract is: \n\t {data['content']}")
        data['instruct'].append(data['content'])
        _SaveMsg(data, KadeNode, 'contract')
    else:
        logger.warning(f"node {data['path'][-1]['ID']} send a error sign to you, thraw this contract away") 


def ReplyDelSecrete(data, Kademlia, *, ID = None):
    '''reply to a delete secrete request'''
    ID = data['instruct'][2] if ID == None else ID
    if Kademlia.secrete.get(ID, None) != None:
        del Kademlia.secrete[ID]
    logger.info(f"initial secrete with node {ID} fail, please retry") 
    

def ReplyPostSecrete(data, KadeNode):
    '''reply to a secrete request'''
    peer = data['content']['sign']
    logger.warning(f"{KadeNode.ID} 開始驗證來自 {data['path'][-1]['ID']}的簽章 ， 簽章為 {peer['cyphertext']}，文本為 {peer['plaintext']}")
    if KadeNode.RSA.verify(
                    KadeNode.RSA.LoadBytePublicKey(peer['public_key'].encode('utf-8')), 
                    peer['cyphertext'], peer['plaintext']):
        InitResult = KadeNode.SecreteInit(data['origin']['ID'], data = data)
        # if secrete key already finish
        if not InitResult:
            # if the secrete of other node has changed before, restart to initial
            if KadeNode.SecreteFresh.get(data['origin']['ID'], data['origin']['PublicKey']) != data['origin']['PublicKey']:
                # DH initial fail, resatart the secrete initial
                KadeNode.send(data['origin']['ID'], 'DELETE', 'secrete', KadeNode.ID)
                logger.info(f"initial secrete fail, please retry") 
                ReplyDelSecrete(data, KadeNode, ID = data['origin']['ID'])
                return
                
            decrypter = AEAD()
            decrypter.NewKey(KadeNode.secrete[data['origin']['ID']])
            msg = decrypter.decrypt(*data['content']['msg'])
            logger.warning(f"node {data['path'][-1]['ID']} send a Whisper to you, the Whisper is: \n\t {data['content']['msg']}, it mean {msg}")

        # if the dh key got some error
        elif InitResult == 'worng DH PK !!!!!':
            # DH initial fail, resatart the secrete initial
            logger.info(f" 'worng DH PK !!!!!'") 
            KadeNode.send(data['origin']['ID'], 'DELETE', 'secrete', KadeNode.ID)
            ReplyDelSecrete(data, KadeNode, ID = data['origin']['ID'])
        
        # if secrete key not finish 
        else:
            logger.info(f"node {data['path'][-1]['ID']} Ask for a Whisper, start to initail the secrete key")
    
    else:
        logger.info(f"node {data['path'][-1]['ID']} send a error sign to you, thraw this contract away") 


def ReplyGetPost(data, KadeNode):
    '''reply to Get Post'''
    content = json.dumps(KadeNode.GetPost())
    KadeNode.send(data['origin']['ID'], 'REPLY', 'getpost', KadeNode.ID, content = content)
    return content
    
    
def ReceiveGetPost(data, KadeNode):
    '''receive reply of get post'''
    data['content'] =  json.loads(data['content'])
    logger.warning(f"node {data['path'][-1]['ID']} reply the post to you, the post is: \n\t {data['content']}")

    for post in data['content']:
        folder = Path(KadeNode.SavePath, "post")
    
        KadeNode.lock.acquire()
    
        # cirtical section
        folder.mkdir(parents=True, exist_ok=True) 
        file = folder / (post[0]['from']['ID'] + '.txt')
        
        if not file.exists():
            # save the file in local
            file.write_text(json.dumps(post))
        
        else:
            OriginFile = json.loads(file.read_text())
            # append to the tail
            OriginFile.extend(post)
            file.write_text(json.dumps(OriginFile))
        # cirtical section
        
        KadeNode.lock.release()
    
    return data['content']
    
def P2PHandle(connect, data, KadeNode):
    '''
    the extend handler for P2P extnd function

    Args:
        data: the request data from other node
        KadeNode: a KadeNode object who call this function    
    '''
    logger.info(f'In P2PHandle, data is {data}, node is {KadeNode.ID}')
    # change string to dict
    data = json.loads(data)
    instruct = data.get('instruct', None)
    logger.info(f'{KadeNode.ID} areceive a {instruct}')
    
    # update Kbucket of the last node in path(from_ node)
    KadeNode.update(data['path'][-1])
    if len(data['path']) >= 8:
        return False
    
    if instruct[0] == 'POST':
        # a node send message
        if instruct[1] == 'message':
            ReplyPostMsg(data, KadeNode)
        # a node post message
        elif instruct[1] == 'post':
            ReplyPostPost(data, KadeNode)
        # a node post a contract
        elif instruct[1] == 'contract':
            ReplyPostContract(data, KadeNode)
        # a node post a secrete
        elif instruct[1] == 'secrete':
            ReplyPostSecrete(data, KadeNode)
    if instruct[0] == 'GET':
        # a node request post
        if instruct[1] == 'post':
            connect.sendall(ReplyGetPost(data, KadeNode).encode(encoding='utf_8'))
    if instruct[0] == 'REPLY':
        # a node request post
        if instruct[1] == 'getpost':
            ReceiveGetPost(data, KadeNode)
    if instruct[0] == 'DELETE':
        # the secrete initial fail
        if instruct[1] == 'secrete':
            ReplyDelSecrete(data, KadeNode)