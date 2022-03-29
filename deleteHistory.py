# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:16:35 2020

@author: arvin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import itertools
import copy
def getJSON(filePath):
    with open(filePath, encoding='utf-8-sig') as f:
        return json.load(f)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("tid")] = item.get("region")
    return teamDict

        
def deleteHistory(json1):
    print(type(json1.get("players")))
    toDelete = []
    for player in json1.get("players"):
        if player["ratings"][-1].get("season") < 2024:
            toDelete.append(json1["players"].index(player))
    print(toDelete)
    for index in sorted(toDelete, reverse=True):
        del json1["players"][index]


#        for rate in player["ratings"][:-1]:
 #           del rate
        
  #      if len(player["stats"]) > 0:
   #         for rate in player["stats"][:-1]:    
    #            del rate
            
        

                
fileName = 'UCBA DII II.json'
main = getJSON(fileName)

deleteHistory(main)
writeJSON(fileName, main)
    

    

