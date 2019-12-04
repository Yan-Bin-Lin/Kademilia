# -*- coding: UTF-8 -*-
'''
Created on 2019年12月4日

@author: danny
'''

import json
from pathlib import Path

SavePath = Path(, 'Save', '00000000')

def DelPost():
    '''
    delete a local post
    '''
    FileNames =  [f for f in Path(SavePath, 'post').glob('*.txt')]
    print(FileNames)
    files = [json.loads(f.read_text()) for f in FileNames]
    for file in files:
        print(file)
        
if __name__ == '__main__':
    DelPost()