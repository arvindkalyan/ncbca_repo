# -*- coding: utf-8 -*-
import json
import xlrd 
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
       teamDict['St Louis'] = 96
       teamDict['Umass'] = 7
       teamDict['SDSU'] = 75
       teamDict['South Florida'] = 92
       teamDict['Ohio St'] = 20
       teamDict['St. Johns'] = 84
       teamDict["St. John's"] = 84
       teamDict[''] = -99
       teamDict['Closed'] = -99
       teamDict['No Offers'] = -99
       teamDict['Closed'] = -99
       teamDict['Was Not Cut'] = -99
       teamDict['N/A'] = -99


    teamDict['Arizona St'] = int(teamDict["Arizona State"])
    teamDict['Mississippi St'] = int(teamDict["Mississippi State"])
    teamDict["California-Irvine"]= int(teamDict['UC Irvine'] )
    teamDict['Cal'] = int(teamDict["California"])
    teamDict['NC State'] = int(teamDict["North Carolina State"])
    return teamDict


def assign(obj, name, ovr, newTeam, teamDict):
    if " (PWO)" in newTeam:
        newTeam = newTeam[:-6]
    season = int(obj.get("meta")["phaseText"][0:4])
    timesFound = 0
    if newTeam in teamDict:
        teamId = teamDict[newTeam]
        for player in obj.get("players"):
            fullname = player.get("firstName") + " " + player.get("lastName")
            ratings = player.get("ratings")[-1]            
            #print(ratings.get("year"))
            if name.find(fullname) == 0 and ratings.get("season") == season and ratings.get("ovr") == ovr:
               # print("FOUND")
                timesFound += 1
                if teamId != -99:
                    player["tid"] = teamId
        
    if timesFound == 0 or timesFound > 1:
        print(name, str(timesFound))             
        
  
            
fileName = 'mid-recruitingV3.json'
loc = ("2057 NCBCA Votes.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
obj = getJSON(fileName)
teamDict = getTIDs(obj)
for i in range(0,709):
    if sheet.cell_value(i, 2) != '':   
        assign(obj,sheet.cell_value(i, 2), sheet.cell_value(i, 13),
           sheet.cell_value(i, 7), teamDict)
  

writeJSON(fileName, obj)


    




