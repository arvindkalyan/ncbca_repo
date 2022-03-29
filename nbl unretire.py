# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 00:41:24 2020

@author: arvin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import itertools
import math
def getJSON(filePath):
    with open(filePath, encoding='utf-8-sig') as f:
        return json.load(f)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def fixretire(json1):
    for player in json1["players"]:
        if(player["tid"] >= 0):
            if player.get("retiredYear") is not None:
                print(player.get("firstName")[0] + player.get("lastName") 
                + str(2049-player.get("born")["year"]))
                player["retiredYear"] = None
            

              
fileName1 = 'nbl2049.json'
edit = getJSON(fileName1)
fixretire(edit)
#writeJSON(fileName1, edit)

