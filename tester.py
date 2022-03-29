
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
       teamDict[item.get("region")] = (item.get("tid"), item.get("cid"), item.get("did"))
    teamDict["STJ"] = teamDict["St. John's"]
    teamDict["SDSU"] = teamDict["San Diego State"]
    return teamDict


def createNT(teamDict, regionOrder, seedOrder):
    
    schedule = obj.get("schedule")
    i = 0

    g = 1800
    for game in schedule:
        series = obj.get("playoffSeries")[-1].get("series")[0][i//2]

        region = regionOrder[i//8]
        seed = seedOrder[i%8]
        homeTeam = "Temple"
        if homeTeam in teamDict:
            htid = teamDict[homeTeam][0]
            hcid = teamDict[homeTeam][1]
            hdid = teamDict[homeTeam][2]
            game["homeTid"] = htid
            series['home']['tid'] = htid
            series['home']['cid'] = hcid
            series['home']['did'] = hdid
        else:
            print("Team not found. Please try again.")
      
        i += 1

        region = regionOrder[i//8]
        seed = seedOrder[i%8]
        awayTeam = "San Diego State"
        if awayTeam in teamDict:
            atid = teamDict[awayTeam][0]
            acid = teamDict[awayTeam][1]
            adid = teamDict[awayTeam][2]
            game["awayTid"] = atid
            series['away']['tid'] = atid
            series['away']['cid'] = acid
            series['away']['did'] = adid

            

        else:
            print("Team not found. Please try again.")
            

        i += 1
        game["gid"] = g
        g+=1

def createNIT(teamDict, regionOrder, seedOrder):
    
    schedule = obj.get("schedule")
    i = 0
    g = 1796
    for game in schedule:
        series = obj.get("playoffSeries")[-1].get("series")[1][i//2]
        
        region = regionOrder[i//4]
        seed = seedOrder[i%4]
        homeTeam = input(region + " #" + str(seed) + " seed: ")
        if homeTeam in teamDict:
            htid = teamDict[homeTeam][0]
            hcid = teamDict[homeTeam][1]
            hdid = teamDict[homeTeam][2]
            game["homeTid"] = htid
            series['home']['tid'] = htid
            series['home']['cid'] = hcid
            series['home']['did'] = hdid
        else:
            print("Team not found. Please try again.")
      
        i += 1

        region = regionOrder[i//4]
        seed = seedOrder[i%4]
        awayTeam = input(region + " #" + str(seed) + " seed: ")  
        if awayTeam in teamDict:
            atid = teamDict[awayTeam][0]
            acid = teamDict[awayTeam][1]
            adid = teamDict[awayTeam][2]
            game["awayTid"] = atid
            series['away']['tid'] = atid
            series['away']['cid'] = acid
            series['away']['did'] = adid

            

        else:
            print("Team not found. Please try again.")
            
        i += 1
        game["gid"] = g
        g+=1
        
    


                #elif item.get("tid") == -3 and item.get("retiredYear") == 2038 and item.get("year") == 'Sr.':
                 #   item["tid"] = teamId
                  #  print(item.get("name") + " " +str( item.get("retiredYear")))
            
            
fileName = 'temple.json'
regionOrder = ['Midwest', 'West', 'East', 'South']
NTseedOrder = [1, 8, 4, 5, 3, 6, 2, 7]
NITseedOrder = [1,4,2,3]
obj = getJSON(fileName)
teamDict = getTIDs(obj)
createNT(teamDict, regionOrder, NTseedOrder)
writeJSON(fileName, obj)



    
#HOW TO SET UP NT
#Get post-NT file, make a copy, and put all 32 teams in w GID 1800. Set this aside
#Get post-NT file, make a copy, put in First 4 teams w GID 1796
#Go into new First 4 file, delete all extraneous schedule/playoffseries content
#Sim First 4




