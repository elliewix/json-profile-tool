######FAILURE

import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

import json

with open('nestedexample2.json', 'r') as jsonin:
    data = json.load(jsonin)


profile = {}

def process_node(node, parent):
    # meta['level'].append('root')
    iternode = node.items()
    for key, value in iternode:
        print(meta['level'], key, type(value))
        if isinstance(value, dict):
            meta['level'].append(key)

            process_node(value, key)
            meta['len'] = len(value)
            meta['first'] = False
            meta['count'] = 0
            process_node(value, 'root')

            meta['deep'] += 1
        else:
            if parent == key:
                l = 1
            else:
                l = len(node)
            if meta['count'] == l:
                meta['level'].pop()
                meta['deep'] = 1
            # print(l, meta['count'], parent)
            meta['count'] += 1

print(profile)


meta = {'level': [], 'deep': 1, 'first': True, 'count' : 0}

process_node(data, 'root')
