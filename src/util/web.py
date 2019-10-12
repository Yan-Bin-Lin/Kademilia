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

def _DataFill(SelfNode, *args, data = None, **kwargs):
    '''
    fill up the header of data need to send
    
    Args:
        data: the request data from other node, default = {}
        *args: remain for instruct ( ['REPLY', 'ID', 'args...', ] )
        **kwargs: for origin, destination, instruct, SelfNodes that need to write in data
    '''
    # new request
    if data == None or data == {}:
        data = {}
        data['origin'] = SelfNode
        data['destination'] = kwargs['destination']
        data['instruct'] = args
        data['path'] = [SelfNode]
        data['content'] = kwargs.get('content', '')
    # update request
    else:
        print(f"data = {data}")
        #data['origin'] = kwargs.get('origin', data['origin'])
        data['destination'] = kwargs['destination'] if kwargs.get('destination', None) != None else data['destination']
        data['instruct'] = args if len(args) != 0 else data['instruct']
        data['path'].append(SelfNode)
        data['content'] = kwargs['content'] if kwargs.get('content', '') != '' else data['content']
    return json.dumps(data)#), cls=AdvancedJSONEncoder)



def GetLocalIP():
    '''get local IP'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip