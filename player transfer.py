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
       teamDict[item.get("region")] = item.get("tid")
    return teamDict

        
def transferPlayers(json1, json2, teams):
    playerList = []
    for item in json1.get("players"):    
        if(item["tid"] in teams or item["tid"] == -3 
                                or item["tid"] == -2 
                                or item["tid"] == -4 
                                or item["tid"] == -5):
            #print(str(item["tid"]) + item["lastName"])
            item["tid"] = -3
    for dii in json1.get("players"):
        if(dii["tid"] == -3):
            dii["tid"] = -3
            #print(dii["firstName"] + dii["lastName"])
            json1["players"].remove(dii)
    for item2 in json2.get("players"):
        if(item2["tid"] in teams or item2["retiredYear"] == 2049 or item2["tid"] == -2 or item2["tid"] == -4):
            #print(item2["firstName"] + item2["lastName"])
            if(item2["tid"] == 26):
                item2["tid"] = 79
            elif(item2["tid"] == 50):
                item2["tid"] = 26
            elif(item2["tid"] == 79):
                item2["tid"] = 50
            playerList.append(item2)
            json1["players"].append(item2)
    return playerList
            
           
def recruitkiller(json1):
    for item in json1.get("players"):
        if (item["tid"] == -2 and (item["firstName"][0] + ". " + item["lastName"] not in open('2049.txt').read())):
            for ratings in item.get("ratings"):
                for rating in ratings:
                    if (type(ratings.get(rating)) == int and
                            ratings.get(rating) > 1 and ratings.get(rating) < 100):
                        ratings[rating] = 0
                        #print(ratings.get(rating))
            #print(item["firstName"]+item["lastName"])
            item["tid"] = -3

def fixPrestige(json1):
    prestiges = [83, 53, 45 , 39 , 65 , 84 , 53 , 79 , 34 , 94 , 24 , 16 , 54 , 50 , 33, 78, 23 ,61,72,20,47,36,83,75,12,85,79,43,71,28,89,49,54,32,55,40,22,54,25,31,59,42,87,21,85,15,14,84,61,31,38,35,46,50,49,37,75,26,52,59,47,56,58,83,50,48,47,75,48,54,19,33,15,88,79,26,72,73,38,33,38,38,24,30,32,21,30,31,18,32,31,28,30,19,32,28,7,12 ,20 ,18]
    for team in json1.get("teams"):
        tid = team.get("tid")
        for season in team["seasons"]:
            #print(season["hype"])
            season["hype"] = prestiges[tid]/100

def fixJUCOYears(json1):
    for item in json1.get("players"):
        if(item["tid"] in range(80,100)):
            item["born"]["year"]=item["born"]["year"]-1

def transferRatings(json1, json2, recruits):
    origlist = {}
    i = 0
    f = open("buffs.txt", "w")
    for origplayer in json2.get("players"):
        name = origplayer.get("firstName")[0] + ". " + origplayer.get("lastName")
        fullname = origplayer.get("firstName") + " " + origplayer.get("lastName")
        if(origplayer["tid"] == -2 and name in open(recruits).read()):
            origlist[fullname] = origplayer
            
            

    for newplayer in json1.get("players"):
        name = newplayer.get("firstName")[0] + ". " + newplayer.get("lastName")
        fullname = newplayer.get("firstName") + " " + newplayer.get("lastName")
        if(newplayer["tid"] == -1 and name in open(recruits).read() 
            and fullname in origlist):
            player = origlist[fullname]
            newplayer["ratings"][0] = player["ratings"][0]
                
            print(name +str(newplayer.get("ratings")[0]['ovr']))
            i = i+1
            f.write(name +str(newplayer.get("ratings")[0]['ovr']))
            f.write("\n")
    print(str(i))
    f.close()
    
def fixrecruityears(json1):
    for player in json1.get("players"):
        name = player.get("firstName")[0] + ". " + player.get("lastName")
        if player["tid"] == -4 and player["born"].get("year") == 2033:
            player["tid"] = -5
        if name in open('4950.txt').read():
            if player["tid"] == -2 and player["born"].get("year") == 2032:
                player["tid"] = -4
            if player["tid"] == -1 and player["born"].get("year") == 2031:
                player["tid"] = -2
            
    
def importDII(json1, json2, json3):
    pids = []
    i = 0
    for player in json1.get("players"):
        if player["tid"] == -1:
            pids.append(player["pid"])
    for player2 in json2.get("players"):
        if player2["pid"] in pids:
            json3["players"].append(player2)
            i = i+1
    print(str(i))
            
                
teams = range(0,80)
fileName1 = '2049s.json'
fileName2 = '2049r.json'
fileName3 = 'actuallyupdated.json'
read = getJSON(fileName1)
readconv = getJSON(fileName2)
edit = getJSON(fileName3)
#fixrecruityears(edit)
importDII(read, readconv, edit)
writeJSON(fileName3, edit)

