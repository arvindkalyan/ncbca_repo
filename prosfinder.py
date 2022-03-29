
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import xlrd
import pandas as pd 
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

def getAwards(section):
    allawards = []
    awardList = {}
    for awards in section:
        award = awards.get("type")
        year = awards.get("season")
        if award in awardList:
            awardList[award].append(year)
        else:
            awardList[award] = [year]
    for key in awardList.keys():
        years = "(" + ','.join(map(str, awardList[key]))  + ")"
        num = len(awardList[key])
        final = str(num) + "x " + key + years
        allawards.append(final)
    return ', '.join(allawards)

def getSalaries(section):
    total = 0
    for item in section:
        total += item["amount"]
    return total*1000

def getCareerStats(section):
    pts = 0
    trb = 0
    ast = 0
    stl = 0
    blk = 0
    per = 0
    ewa = 0 
    for year in section:
        if not year["playoffs"]:
            pts += year["pts"]
            trb += year["orb"] + year["drb"]
            ast += year["ast"]
            stl += year["stl"]
            blk += year["blk"]
            ewa += year["ewa"]
    return [pts, trb, ast, stl, blk, per, ewa]
            
def getMaxOvr(section):
    ovrs = {}
    for year in section[1:]:

        ovrs[year["ovr"]] = year["season"]
    if len(ovrs) == 0:
        return section[0].get("season")
    maxovr = max(ovrs.keys())
    return ovrs[maxovr] 

def getMaxRTGs(section, season):
    for year in section:
        if year["season"] == season:
            return [year["ovr"], year["hgt"], year["stre"],  year["spd"], year["jmp"], year["endu"], year["ins"], year["dnk"], year["ft"],year["fg"],year["tp"],year["oiq"],year["diq"],year["drb"],year["pss"],year["reb"]]
    return ['','','','','','','','','','','','','','','',''] 
    
def getMaxStats(section, season):
    for year in section:
        if year["season"] == season and year["playoffs"] == False and year["gp"] != 0:
            return [year["pts"]/year["gp"], (year["orb"] + year["drb"])/year["gp"], year["ast"]/year["gp"], year["stl"]/year["gp"], year["blk"]/year["gp"], year["per"], year["ewa"]]
    return [0,0,0,0,0,0,0]


def findpros(obj, teamDict, playerList):
    cols = ['Name', 'Draft Position','Draft Round','Pick Number', 'Draft Year','Earnings','Career Pts','Rebounds','Assists', 'Steals','Blocks','PER','EWA','Peak Year','PPG','RPG','APG','SPG','BPG','PER','EWA','Peak Ovr','hgt','stre','spd','jmp','endu','ins','dnk','ft','fg','tp','oiq','diq','drb','pss','reb','Accomplishments']
    df = pd.DataFrame(columns = cols)
    index = 0
    for player in obj["players"]:

        shortname = player.get("firstName")[0] + ". " + player.get("lastName")
        longname = player.get("firstName") + " " + player.get("lastName")
        name = ''
        if shortname in playerList or longname in playerList:
            if shortname in playerList:
                name = shortname
            if longname in playerList:
                name = longname
            
            if playerList[name] == player.get("college") or (playerList[name] == 'Massachusetts' and player.get("college") == 'UMass'):
                draftyear = player["draft"]["year"]
                rd = str(player["draft"]["round"])
                pk = str(player["draft"]["pick"])
                draftpos = str(player["draft"]["round"])+"."+str(player["draft"]["pick"])
                if draftpos == '0.0':
                    draftpos = 'UDFA'
                earnings = getSalaries(player["salaries"])
                awards = getAwards(player["awards"])
                careerstats = getCareerStats(player["stats"])
                szn = getMaxOvr(player["ratings"])
                maxstats = getMaxStats(player["stats"], szn)
                maxrtgs = getMaxRTGs(player["ratings"], szn)
                print(longname)
                print(szn)
                print(maxstats)
                print(maxrtgs)
                print(careerstats)
                print(draftyear, draftpos)
                print(earnings)
                print(awards)
                print("----------------------------")
              
                df.loc[index] = [longname, draftpos, rd, pk, draftyear, earnings] + careerstats + [szn] + maxstats + maxrtgs + [awards]
                index += 1
    
    print(df.head(10))
    return df
        
        
            

              
fileName = '2052 NBL Pre Playoffs.json'
obj = getJSON(fileName)

loc = ("ethan.xlsx") 

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
obj = getJSON(fileName)
num = 1
playerList = {}
teamDict = getTIDs(obj)
for i in range(0,7):
    team = sheet.cell_value(i,0)

    for j in range(2,int(sheet.cell_value(i,1))+2):
        name = sheet.cell_value(i,j)
        if " (L)" in name:
            name = name[:-4]
        if "(L)" in name:
            name = name[:-3]
        if " +" in name:
            name = name[:-2]
        playerList[name] = team

allpros = findpros(obj, teamDict, playerList)

allpros.to_excel('ethanpros.xlsx', encoding='utf-8', index=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    

