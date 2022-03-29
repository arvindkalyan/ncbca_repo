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

        
def transferPlayers(json1, json2,playerList):
    season = int(json1.get("meta")["phaseText"][0:4]) 
    teamDict = getTIDs(json1)
    atts1 = ["stre", "spd", "jmp", "endu", 
              "ins", "dnk", "fg", "tp","ft",
              "oiq", "diq", "drb", "pss", "reb"]
    print(len(json2["players"]))
   
    pids = {}
    for player in json2.get("players"):
        pids[player["pid"]] = player.get("firstName") + " " + player.get("lastName")
    pid = (max(list(pids.keys()))) + 1
    for player in json1.get("players"):
        #if player.get("firstName") + " " + player.get("lastName") in playerList:
        if any(player.get("firstName") + " " + player.get("lastName") in name for name in playerList):
            school = teamDict[player["statsTids"][-1]]
            player["tid"] = -2
            player["watch"] = "true"
            ratings = player["ratings"][-1]
            player["college"] = school
            
            for year in player["stats"]:
                year["tid"] = -10
            
            for att in atts1:
               # print(att + str(ratings[att]))
                if att == "ft" or att == 'endu':
                    
                    ratings[att] = 0.81 * ratings[att]
                elif att == 'oiq':
                    ratings[att] = 0.81 * ratings[att]
                else:
                    ratings[att] = 0.76 * ratings[att]
                #print(att + str(ratings[att]))
            player["pid"] = pid
            pid += 1
            if player["pid"] in pids:
                print(pids[player["pid"]])
            player2 = copy.deepcopy(player)
            json2["players"].append(player2)
            #print(type(copy.deepcopy(player)))
            player["tid"] = -3
        else:
            if player["tid"] == -3 and player["retiredYear"] == season and (player["year"] == 'Jr.' or player["year"] == 'So.' or player["year"] == 'Fr.'):

                player["tid"] = player["statsTids"][-1]
        
    print(len(json2["players"]))
               

                
fileName1 = '2053 JUCO.json'
fileName2 = '2053 Post-NT JUCOs.json'
juco = getJSON(fileName1)
main = getJSON(fileName2)

with open("jucos.txt") as f: 
    playerList = f.readlines()
print(playerList)
transferPlayers(juco, main,playerList)
#writeJSON(fileName1, juco)
writeJSON(fileName2, main)
    

    

