import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

import json

with open('nestedexample2.json', 'r') as jsonin:
    data = json.load(jsonin)


profile = {}

def process_node(node):
    for key, value in node.items():
        if isinstance(value, dict):
            path = "profile['" + "']['".join(meta['level']) + "']"
            # if len(meta['level']) != 0:
            if key not in profile and key != '':
                profile[key] = []
            else:
                previous = meta['level'][:-1]
                print(previous)
                current = eval("profile['" + "']['".join(previous) + "']")
                if key not in current:
                    eval("profile['" + "']['".join(previous) + "']")[key] =

            meta['level'].append(key)

            meta['deep'] += 1
            process_node(value)
            meta['deep'] -= 1
            meta['level'].pop()

        else:
            print("profile['" + "']['".join(meta['level']) + "']")
            eval("profile['" + "']['".join(meta['level']) + "']").append(key)

            # print("profile['" + "']['".join(checked) + "']")






meta = {'level': [], 'deep': 0, 'first': True, 'count' : 0}

process_node(data)
print(profile)
