#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 16:09:20 2018

@author: him

It creates index.json file in the same directory
"""

import json
import os
import sys
import errno

### write your prefix here
#prefix = '/home/him/Documents/distributed_systems/Notes/highlighted_notes'
prefix = '/home/him/test_fetch'

def create_index(root_path):
    """
    Creates the index file in heirarchical tree structure of the input path directory.
    Parameters: path whose directory structure needs to be created.
    Returns: Dictionary of heirarchical tree.
    """
    directory_structure = {
            'file_name' : os.path.basename(root_path),
            'path' : root_path,
            'version_node' : 'NONE',
            'version_number' : 0,
            }
    try:
        directory_structure[os.path.basename(root_path)] = [create_index(os.path.join(root_path, subfiles)) for subfiles in os.listdir(root_path)]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        pass
    return directory_structure

with open('index.json','w') as Ijson:
    json.dump(create_index(os.path.join(prefix,'data')),Ijson)

