# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import statistics
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
       

    return teamDict


def changeTeamName(obj,tid,newname):
    obj["gameAttributes"][-7]['value'][tid] = newname[:4]
    obj["gameAttributes"][-4]['value'][tid] = newname
    obj["gameAttributes"][-3]['value'][tid] = "Team"
    
    obj["teams"][tid]["region"] = "Team"
    obj["teams"][tid]["name"] = newname
    
def getblocks(obj):
    blockRatings = {}
    tempList = []
    for i in range(0, 30):
        blk = i/10
        for pos in {"PG", "SG", "SF", "PF", "C", "G", "GF", "F", "FC"}:
            for player in obj.get("players"):
                if "stats" in player and player.get("pos") == pos:
                    for season in player.get("stats"):
                        if not season.get("playoffs") and season.get("gp") != 0 and round(season.get("blk")/season.get("gp"),1) == blk:
                    
                            #print(player.get("name") + " " + str(season.get("season")) + " " + str(season.get("blk")))
                    
                            for rating in player.get("ratings"):
                                if rating.get("season") == season.get("season"):
                                       # print(str(rating.get("blk")))
                                        tempList.append(rating.get("blk"))
            if len(tempList) == 0 and blk > 1:
                blockRatings[(pos, blk)] = 100
            else:
                blockRatings[(pos, blk)] = statistics.median(tempList)
            tempList = []
    return(blockRatings)

def getposstatdist(stat,pos,year, obj):
    if(stat == "endu" and (pos == "G" or pos == "SG" or pos == "GF")):
        return getstatdist(stat,year,obj)
    statList = []
    for player in obj.get("players"):
        if "pos" in player:
            if player["pos"] == pos:
                for season in player.get("ratings"):
                    if season.get("season") == year:
                        statList.append(season[stat])
        else:
            if player["ratings"][-1]["pos"] == pos:
                for season in player.get("ratings"):
                    if season.get("season") == year:
                        statList.append(season[stat])
    return(statistics.mean(statList), statistics.stdev(statList))
    
def getstatdist(stat,year, obj):
    statList = []
    for player in obj.get("players"):
            for season in player.get("ratings"):
                if season.get("season") == year:
                    statList.append(season[stat])
    return(statistics.mean(statList), statistics.stdev(statList))

def getsteals(obj):
    stealRatings = {}
    tempList = []
    for i in range(0, 54):
        stl = i/10
        for pos in {"PG", "SG", "SF", "PF", "C", "G", "GF", "F", "FC"}:
            for player in obj.get("players"):
                if "stats" in player and player.get("pos") == pos:
                    for season in player.get("stats"):
                        if not season.get("playoffs") and season.get("gp") != 0 and round(season.get("stl")/season.get("gp"),1) == stl:
                    
                            #print(player.get("name") + " " + str(season.get("season")) + " " + str(season.get("blk")))
                    
                            for rating in player.get("ratings"):
                                if rating.get("season") == season.get("season"):
                                       # print(str(rating.get("stl")))
                                        tempList.append(rating.get("stl"))
            if len(tempList) == 0 and stl > 1:
                stealRatings[(pos, stl)] = 100
            else:
                stealRatings[(pos, stl)] = statistics.median(tempList)
            tempList = []
    return(stealRatings)

def clearplayers(obj, tids):
    for player in obj.get("players"):
        if player["tid"] in tids:
            player["tid"] = -3

def transferplayer(name, year, obj, obj2, obj3, obj4,tid):
    
    for origplayer in obj4.get("players"):
        lastratings = origplayer.get("ratings")[-1]
        if origplayer.get("firstName") in name and name.index(origplayer.get("firstName"))==0 and origplayer.get("lastName") in name and name.index(origplayer.get("lastName"))!=0:
            #print (origplayer.get("firstName") + origplayer.get("lastName"))
            
            lastratings = origplayer.get("ratings")[-1]
            
            pos = lastratings["pos"]
            lastratings["blk"] = (2.5*(lastratings["hgt"])+1.5*(lastratings["jmp"])+0.5*lastratings["diq"])/4.5
            lastratings["stl"] = (50 + lastratings["spd"] + 2*(lastratings["diq"]))/4
            for stat in {"hgt", "ins", "dnk", "ft", "fg", "tp","drb","pss","reb"}:
                    oldstatdist = getstatdist(stat, year, obj)
                    newstatdist = getstatdist(stat, lastratings["season"], obj4)
                    newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                    if newrating > 100:
                        newrating = 100
                    lastratings[stat] = newrating
            for stat in {"stre", "spd", "jmp", "endu"}:
                oldstatdist = getposstatdist(stat,pos, year, obj)
                newstatdist = getposstatdist(stat,pos, lastratings["season"], obj4)
                newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                if newrating > 100:
                        newrating = 100
                lastratings[stat] = newrating
                    
       #     print(name)    
            
       
            age = lastratings["season"] - origplayer["born"]["year"]
            lastratings["season"] = year
            origplayer["born"]["year"] = year-age
            
            origplayer["name"] = name
            origplayer["pos"] = pos
            origplayer["tid"] = tid
            origplayer["contract"]["cre"] = year-1
            
            obj["players"].append(origplayer)
        #    print("DONE")
            return
        
    for origplayer in obj3.get("players"):
        lastratings = origplayer.get("ratings")[-1]
        if  origplayer.get("firstName") in name and name.index(origplayer.get("firstName"))==0 and origplayer.get("lastName") in name and name.index(origplayer.get("lastName"))!=0:
            
            
            if lastratings["season"] > 2044:
                #print(origplayer.get("firstName") + origplayer.get("lastName"))
                
                pos = lastratings["pos"]
                lastratings["blk"] = (2.5*(lastratings["hgt"])+1.5*(lastratings["jmp"])+0.5*lastratings["diq"])/4.5
                lastratings["stl"] = (50 + lastratings["spd"] + 2*(lastratings["diq"]))/4
                for stat in {"hgt", "ins", "dnk", "ft", "fg", "tp","drb","pss","reb"}:
                    oldstatdist = getstatdist(stat, year, obj)
                    newstatdist = getstatdist(stat, lastratings["season"], obj3)
                    newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                    if newrating > 100:
                        newrating = 100
                    lastratings[stat] = newrating
                    
                for stat in {"stre", "spd", "jmp", "endu"}:
                    oldstatdist = getposstatdist(stat,pos, year, obj)
                    newstatdist = getposstatdist(stat,pos, lastratings["season"], obj3)
                    newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                    if newrating > 100:
                        newrating = 100
                    lastratings[stat] = newrating
                        
                #print(name)    
                
                
    
                
                age = lastratings["season"] - origplayer["born"]["year"]
                lastratings["season"] = year
                origplayer["born"]["year"] = year-age
                
                origplayer["name"] = name
                origplayer["pos"] = pos
                origplayer["tid"] = tid
                origplayer["contract"]["cre"] = year-1
                
                obj["players"].append(origplayer)
                #print("DONE")
                return
        
    for origplayer in obj2.get("players"):
        lastratings = origplayer.get("ratings")[-1]
        if origplayer.get("firstName") in name and name.index(origplayer.get("firstName"))==0 and origplayer.get("lastName") in name and name.index(origplayer.get("lastName"))!=0:
            
            
            if lastratings["season"] > 2039:

                #print(origplayer.get("firstName") + origplayer.get("lastName"))
                               
                pos = lastratings["pos"]
                lastratings["blk"] = (2.5*(lastratings["hgt"])+1.5*(lastratings["jmp"])+0.5*lastratings["diq"])/4.5
                lastratings["stl"] = (50 + lastratings["spd"] + 2*(lastratings["diq"]))/4
                for stat in {"hgt", "ins", "dnk", "ft", "fg", "tp","drb","pss","reb"}:
                    oldstatdist = getstatdist(stat, year, obj)
                    newstatdist = getstatdist(stat, lastratings["season"], obj2)
                    newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                    if newrating > 100:
                        newrating = 100
                    lastratings[stat] = newrating
                for stat in {"stre", "spd", "jmp", "endu"}:
                    oldstatdist = getposstatdist(stat,pos, year, obj)
                    newstatdist = getposstatdist(stat,pos, lastratings["season"], obj2)
                    newrating = (((lastratings[stat]-newstatdist[0])/(newstatdist[1]))*oldstatdist[1])+oldstatdist[0]
                    if newrating > 100:
                        newrating = 100
                    lastratings[stat] = newrating
                        
              #  print(name)    
              
                
                age = lastratings["season"] - origplayer["born"]["year"]
                lastratings["season"] = year
                origplayer["born"]["year"] = year-age
                
                origplayer["name"] = name
                origplayer["pos"] = pos
                
                origplayer["contract"]["cre"] = year-1
                origplayer["tid"] = tid
                for season in origplayer.get("ratings")[:-1]:
                    if season.get("season") == 2039:
                        season["season"] = 2015
                obj["players"].append(origplayer)
               # print("DONE")
                return
    for origplayer in obj.get("players"):
        lastratings = origplayer.get("ratings")[-1]
        if origplayer.get("name") == name:
            #print(origplayer.get("name"))
             
            lastratings = origplayer.get("ratings")[-1]

                    
            #print(name)    
            
            
            age = lastratings["season"] - origplayer["born"]["year"]
            lastratings["season"] = year
            origplayer["born"]["year"] = year-age
      
            origplayer["contract"]["cre"] = year-1
            origplayer["tid"] = tid

            return

            
            

            
            
    print(name)       
    return
            
origexport = 'NCBCA Alumni Tourney.json'
preexport = '2044 NCBCA Mid-NT Export.json'
midexport = '2049 NCBCA Pre-NT Export.json'
latestexport = '2050 FIXED NT.json'

teams = ("NCBCA Alumni Tourney Signups.xlsx") 
wb = xlrd.open_workbook(teams) 
#sheet = wb.sheet_by_index(0) 
obj = getJSON(origexport)
obj2 = getJSON(preexport)
obj3 = getJSON(midexport)
obj4 = getJSON(latestexport)
teamDict = getTIDs(obj)


#clearplayers(obj,range(0,35))

#for i in range(0,35):
    
 #   sheet = wb.sheet_by_index(i+2)
    
  #  changeTeamName(obj,i,wb.sheet_names()[i+2])
   # for t in range(2,15):
        #print(sheet.cell_value(t,1))
    #    transferplayer(sheet.cell_value(t,1), 2039, obj, obj2, obj3, obj4,i)
     #   print(wb.sheet_names()[i+2] + str(t-1))

#manualplayers = {"Charles Hendrick", "Henry King", "James McIlwain", "Stephen Downing", "Michael Jameson", "Brandon Fields", "Herman Figueroa", "Ralph Baker", "Raymond Fellows", "Kevin Cochran", "Reed Reyes", "Justin Giovacchini"}
#for name in manualplayers:
 #   transferplayer(name, 2039, obj, obj2, obj3, obj4,0)
#clearplayers(obj, {44})
#for name in {"Matt McNeal", "Anthony Broome", "D'Andre Traore", "Sacha Kanygin", "Brian Wheeler", "Justin Giovacchini", "Tracey Hurtt", "Dakari Vanover", "Wil Penn", "Sean Owens", "Janerio Macellari", "Vance Johnson", "Francis-Cedric Rwahwire", "Phil Harn", "Dardan Djordjic", "B.J. Benton", "Rashad Stricker", "Laytwan Byrd", "Nate Wellington", "Ryan Burrell", "Angel Mackinson", "Dion Freeman", "Gur Buch", "Nicholas Schmitt", "Kevin Langford"}:    
#for name in {"Miguel Jackson", "Mike Newman", "Lorenzo Portis", "Phil Harn", "Dardan Djordjic", "B.J. Benton", "Rashad Stricker", "Laytwan Byrd", "Nate Wellington", "Ryan Burrell", "Angel Mackinson", "Dion Freeman", "Gur Buch", "Nicholas Schmitt", "Kevin Langford"}:    
 #   transferplayer(name, 2039, obj, obj2, obj3, obj4)
tochange = {"won", "lost", "wonHome", "lostHome", "wonAway", "lostAway", "wonDiv", "lostDiv", "wonConf", "lostConf", "confChamp"}
for item in obj.get("teams"):
    for season in item.get("seasons"):
        if season.get("season") == 2039:
            for tc in tochange:
                season[tc] = 0

 
writeJSON(origexport, obj)


    




