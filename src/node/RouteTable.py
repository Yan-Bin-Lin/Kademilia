# -*- coding: UTF-8 -*-
'''
Created on 2019年9月24日

@author: danny
'''
from ..util.hash import CountDistance
from .KBucket import KBucket

from ..util.log import log
logger = log()


class RouteTable():
    def __init__(self, SelfNode):
        self.SelfNode = SelfNode
        self.table = {i : KBucket(self.SelfNode) for i in range(128)}
        self.amount = [0]*128
        self.length = 0
        
        
    def _CheckDistanceIndex(self, OtherNode, distance = None):
        return (CountDistance(self.SelfNode.GetID(), OtherNode) if distance == None else distance).find('1') + 1
        
        
    def _UpdateAmount(self, dis):
        '''update amount of node in table'''
        self.length += self.table[dis].length() - self.amount[dis]
        self.amount[dis] = self.table[dis].length()
        
        
    def AddNode(self, OtherNode, distance = None):
        '''
        add a new node into route table
        '''
        # node should locate in the bucket with index of first '1'
        dis = self._CheckDistanceIndex(OtherNode['ID'], distance)
        self.table[dis].AddNode(OtherNode)
        self._UpdateAmount(dis)
        logger.debug(f'add the node {self.table[self._CheckDistanceIndex(OtherNode["ID"], distance)].bucket[OtherNode["ID"]]}')

    
    def GetNode(self, NodeID = None, *, closest = True, ping = True, num = 8, data = None, ExceptList = None):
        '''
        return the most closest specify NodeData. 
        
        Attributes:
            NodeID (str): the ID of node to find
            num (int): number of  return node, if closest is false, it will be set to 1
            closest: if node not found will return k most closest NodeData of NodeID if closest is True else return None
            ping: if ping is true will ping the node before return the node 
        '''
        logger.debug(f" NodeID is {NodeID}, closest = {closest}, ping = {ping}, num = {8}, data is {data}, ExceptList = {ExceptList}")
        
        # check for no give ID
        if NodeID == None:
            NodeID = self.SelfNode.GetID()
        
        # check for search number of node
        if not closest:
            num = 1
        num = min(num, self.length)
        
        # initial for loop...
        result = []
        deviation = 0
        exc = 0
        sign = [-1, 0]
        pre_dis = self._CheckDistanceIndex(NodeID)
        if data != None:
            ExceptList = ExceptList if ExceptList != None else []
            ExceptList.extend([d['ID'] for d in data['path']])

        logger.debug(f"data is {data}, ExceptList is {ExceptList}")
        
        # find the closest node
        while deviation < 128 and len(result) < num:
            dis = (pre_dis + deviation) % 128
            logger.debug(f"bucket deviation is {deviation}, min number is {num}, self.length = {self.length}, exc is {exc}")
            
            if self.table[dis].length() != 0:
                logger.debug(f'in the bucket of distance pre_dis is {pre_dis} deviation is {deviation}\n to find the node {NodeID}, the bucket content {self.table[dis].bucket}')            
                tmp = self.table[dis].GetNode(NodeID, closest = closest, ping = ping, ExceptList = ExceptList)
                result.extend(tmp)
                # if node in bucket content ExceptList node
                exc += self.table[dis].length() - len(tmp)
                logger.debug(f'在 node {self.SelfNode.GetID()}的 bucket {dis} 中 找到 靠近 node {NodeID} 的節點{tmp}')                # for debug here    

            deviation = -1 * deviation + sign[0 if deviation >= 0 else 1]

            # 下修查找節點
            self._UpdateAmount(dis)
            num = min(num, self.length - exc)

        logger.debug(f"return {result[:num]}")
        return result[:num]