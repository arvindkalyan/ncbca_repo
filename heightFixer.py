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

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("tid")] = item.get("region")
    return teamDict

        
def fixHeights(json1, json2):
    i = 1
    j = 1
    oldRatings = {}
    for player in json1.get("players"):
        ratings = player.get("ratings")[-1]
        if player["tid"] == -4 or player["tid"] == -5:
            oldRatings[(player.get("firstName"), player.get("lastName"), player.get("city"), player.get("tid"))] = (ratings.get("hgt"),ratings.get("ovr"))
    for player in json2.get("players"):
        ratings = player.get("ratings")[-1]
        if player["tid"] == -2:
            if (player.get("firstName"), player.get("lastName"), player.get("city"), -4) not in oldRatings:
                print((player.get("firstName"), player.get("lastName"), player.get("city"), player.get("tid")))
            else:
                newratings = oldRatings[(player.get("firstName"), player.get("lastName"), player.get("city"), -4)]
                ratings["hgt"] = newratings[0]
                ratings["ovr"] = newratings[1]
        if player["tid"] == -4:
            if (player.get("firstName"), player.get("lastName"), player.get("city"), -5) not in oldRatings:
                print((player.get("firstName"), player.get("lastName"), player.get("city"), player.get("tid")))
            else:
                newratings = oldRatings[(player.get("firstName"), player.get("lastName"), player.get("city"), -5)]
                ratings["hgt"] = newratings[0]
                ratings["ovr"] = newratings[1]
                
               

                
fileName1 = '2050 NCBCA Post-NT Draft Size Increased CT and NT Restored.json'
fileName2 = '2051 with JUCOS.json'
old = getJSON(fileName1)
new = getJSON(fileName2)


#print(playerList)
#fixHeights(old, new)
#writeJSON(fileName2, new)


    

    

