# -*- coding: UTF-8 -*-
'''
Created on 2019年9月3日

@author: danny
'''
import json
import socket
'''
# for json save KadeNodeType
class AdvancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if hasattr(obj, 'GetData'):
            return obj.GetData()
        
        return json.JSONEncoder.default(self, obj)
'''
# return the data in protocol format
# *args = ['REPLY', 'ID', 'args...', ] (instruct)
# **kwargs = origin, destination, instruct, SelfNodes
def _DataFill(SelfNode, *args, data = {}, **kwargs):
    # new request
    if data == {}:
        data['origin'] = SelfNode
        data['destination'] = kwargs['destination']
        data['instruct'] = args
        data['path'] = [SelfNode]
        data['content'] = kwargs.get('content', '')
    # update request
    else:
        #data['origin'] = kwargs.get('origin', data['origin'])
        data['destination'] = kwargs['destination'] if kwargs['destination'] != None else data['destination']
        data['instruct'] = args if len(args) != 0 else data['instruct']
        data['path'].append(SelfNode)
        data['content'] = kwargs['content'] if kwargs['content'] != '' else data['content']
    print(data)
    return json.dumps(data)#), cls=AdvancedJSONEncoder)


#get local IP
def GetLocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip