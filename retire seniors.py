# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import random
def getJSON(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("tid")] = 45
    return teamDict 

def retire(obj, obj2):
    toretire = {}
    for player in obj.get("players"):
        #ratings = player.get("ratings")[-1]

        toretire[(player.get("name"),player.get("pos"),player.get("city"))] = player.get("tid")
    
    print("First export done.")  
    
    for player2 in obj2.get("players"):
        #ratings = player.get("ratings")[-1]
        if (player2.get("name"),player2.get("pos"),player2.get("city")) in toretire:
            player2["tid"] = toretire[(player2.get("name"),player2.get("pos"),player2.get("city"))]
    print("Second export done.")  
    
def update(teamDict):
    print(teamDict)
    for key in list(teamDict.keys()):
        if teamDict[key] < 1:
            teamDict.pop(key)
            
def updateTeam(teamDict, team):
    
    teamDict[team] -= 1
    if teamDict[team] < 1:
        teamDict.pop(team)
            

def fillteams(obj, teamDict):
    season = int(obj.get("meta")["phaseText"][0:4])
    for player in obj.get("players"):
        if player.get("tid") in teamDict:
            teamDict[player.get("tid")] -= 1
    update(teamDict)
    
    for player in obj.get("players"):
        if (player.get("tid") == -1 and player.get("ratings")[-1].get("ovr")<55) or (player.get("tid") == -2 and player.get("ratings")[-1].get("ovr")< 34) or (player.get("tid") == -4 and player.get("ratings")[-1].get("ovr")< 34):
            if season - player["born"]["year"] < 18:
                player["born"]["year"] = season-18
            if len(list(teamDict)) > 0:
                team = random.choice(list(teamDict))
                player["tid"] = team
                updateTeam(teamDict,team)
        


        
    

fileName = '2033 NZCFL Pre Progression.json' # put your export here, make sure file name is accurate

obj = getJSON(fileName)

teamDict = getTIDs(obj)
fillteams(obj, teamDict)
print(teamDict)

print(sum(teamDict.values()))
#retire(obj, obj2)
#print("Writing to JSON.")
writeJSON(fileName, obj) #this takes time! 






