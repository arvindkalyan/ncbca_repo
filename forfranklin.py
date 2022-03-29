# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import xlrd 
import copy
def getJSON(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("region")] = item.get("tid")
       teamDict['Miami'] = 12
       teamDict['UConn'] = 22
       teamDict['UMass'] = 7
       teamDict['Loyola'] = 65
       teamDict['Florida State'] = 10
       teamDict['Penn St'] = 21
       teamDict['Saint Louis'] = 96
       teamDict['Umass'] = 7
       teamDict['SDSU'] = 75
       teamDict['South Florida'] = 92
       teamDict['Ohio St'] = 20
       teamDict['St. Johns'] = 84
       teamDict["St. John's"] = 84

    return teamDict


def removeIneligible(obj,obj2,f):
    season = int(obj2.get("meta")["phaseText"][0:4])
    ineligibleList = []
    eligibleList = []
    for player in obj2.get("players"):
        ratings = player.get("ratings")[-1]
        age = season - player["born"]["year"]
        tid = player.get("tid")
        if age < 22 and ratings.get("season") == season and ratings.get("ovr") < 70 and tid == -3:
            #print(player.get("firstName")+player.get("lastName"))
            ineligibleList.append((player.get("firstName")+player.get("lastName"),ratings.get("pos")))
        if ratings.get("season") == season and ratings.get("ovr") >= 70 and tid >= 0: 
            #print(player.get("firstName")+player.get("lastName"))
            eligibleList.append((player.get("firstName")+player.get("lastName"),ratings.get("pos")))
            print(player.get("firstName")+player.get("lastName"))
            obj["players"].append(player)
            

    print("----------------")
    for player in obj.get("players"):
        ratings = player.get("ratings")[-1]
        if (player.get("firstName")+player.get("lastName"),ratings.get("pos")) in ineligibleList:
            print(player.get("firstName")+player.get("lastName"))

    for player in obj.get("players"):
        ratings = player.get("ratings")[-1]
        if (player.get("firstName")+player.get("lastName"),ratings.get("pos")) in ineligibleList:
            print(player.get("firstName")+player.get("lastName"))
            obj["players"].pop(obj["players"].index(player))

    for player in obj.get("players"):
        ratings = player.get("ratings")[-1]
        if (player.get("firstName")+player.get("lastName"),ratings.get("pos")) in ineligibleList:
            print(player.get("firstName")+player.get("lastName"))
            obj["players"].remove(player)

    print("DRAFT CLASS")
    for player in obj.get("players"):
        f.write(player.get("firstName")+ " " + player.get("lastName")+"\n")
            #if player.get("tid") in [0,40]:
            

                #elif item.get("tid") == -3 and item.get("retiredYear") == 2038 and item.get("year") == 'Sr.':
                 #   item["tid"] = teamId
                  #  print(item.get("name") + " " +str( item.get("retiredYear")))
            
            
draftclass = '2052class.json'
export = '2052post.json'
obj = getJSON(draftclass)
obj2 = getJSON(export)
f = open("class.txt", "w")
f.truncate(0)
removeIneligible(obj,obj2,f)    
f.close()
writeJSON(draftclass, obj)


    




