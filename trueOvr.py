# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import itertools
import math
import statistics
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
       teamDict["FA"] = -1
       teamDict["Recruit"] = -2
       teamDict["idk"] = -3

    return teamDict

def getTrueOvrs(team, teamDict, season):
    cols = ["Name","Age","Team","Pos","Ovr","trueOvr","Diff","pce","usg","drb","pss","to",
                            "rim","ins","mid","three","reb","stl","blk","foul","draw","rockets","def","int","perim","end","ath"]
    df = pd.DataFrame(columns = cols)
    index = 0
    season = int(obj.get("meta")["phaseText"][0:4])
    playerList = []
    addNames = ["Terrance Dantzler","Nate Proffitt","J.R. Garcia", "Jeff Northern", "David Roberts"]
    if team in teamDict:
        teamId = teamDict[team]
        for item in obj.get("players"):
            ovr = item.get("ratings")[-1].get("ovr")
            age = season-item["born"]["year"]
            #if (ovr < 55) or (item.get("firstName") in addNames):         
            if item["tid"] == teamId or item.get("firstName")+ " " + item.get("lastName") in addNames:
                tm = dict(map(reversed, teamDict.items()))[item["tid"]]
                if len(item.get("firstName")) > 0:
                    name = item.get("firstName")[0] +  ". " + item.get("lastName")
                else: 
                    name=item.get("firstName")+ " " + item.get("lastName") 
                print(name + str(ovr))  
                item2 = item.get("ratings")[-1]
                pos = item2.get("pos")
                if item2.get("season") == season:

                    hgt = item2.get("hgt")
                    stre = item2.get("stre")
                    spd = item2.get("spd")
                    jmp = item2.get("jmp")
                    endu = item2.get("endu")
                    ins = item2.get("ins")
                    dnk = item2.get("dnk")
                    ft = item2.get("ft")
                    fg = item2.get("fg")
                    tp = item2.get("tp")
                    oiq = item2.get("oiq")
                    diq = item2.get("diq")
                    drb = item2.get("drb")
                    pss = item2.get("pss")
                    reb = item2.get("reb")
                    
                    pace = (spd+jmp+dnk+tp+drb+pss)/6
                    usage = ((1.5*ins)+dnk+fg+tp+(spd*0.5)+(hgt*0.5)+(drb*0.5)+(oiq*0.5))/6.5
                    dribbling = (drb+spd)/2
                    passing =((0.4*drb)+pss+(0.5*oiq))/1.9
                    turnovers =((50*0.5)+ins+pss+(-1*oiq))/1.5
                    rim =((0.75*hgt)+(0.2*spd)+(0.6*jmp)+(0.4*dnk)+(0.2*oiq))/(0.75+0.2+0.6+0.4+0.2)
                    low = ((2*hgt)+(0.6*stre)+(0.2*spd)+ins+(0.2*oiq))/(2+0.6+0.2+1+0.2)
                    mid =((0.5*oiq)+fg)/1.5
                    three =((0.1*oiq)+tp)/1.1
                    rebounding =((2*hgt)+(0.1*stre)+(0.1*jmp)+(2*reb)+(0.5*oiq)+(0.5*diq))/5.2
                    stealing =(50+spd+(2*diq))/4
                    blocking =((2.5*hgt)+(1.5*jmp)+(0.5*diq))/4.5
                    fouling =((3*50)+hgt+(-1*diq)+(-1*spd))/2
                    drawing = (hgt+spd+drb+dnk+oiq)/5
                    defense=(hgt+stre+spd+(0.5*jmp)+(2*diq))/5.5
                    interior =((2.5*hgt)+stre+(0.5*spd)+(0.5*jmp)+(2*diq))/(2.5+1+0.5+0.5+2)
                    perimeter =((0.5*hgt)+(0.5*stre)+(2*spd)+(0.5*jmp)+diq)/(0.5+0.5+2+0.5+1)
                    endurance = (50+endu)/2
                    athleticism =(stre+spd+jmp+(0.75*hgt))/(3.75)
                    rockets = defense + three + drawing
                    attributes = [pace, usage, dribbling, passing, turnovers, rim, low, mid, three, rebounding, stealing, blocking,
                                  fouling, drawing, rockets, defense, interior, perimeter, endurance, athleticism]
                    
                    trueOvr =((hgt*5)+(stre*1)+(spd*4)+(jmp*2)+(endu*1)+(ins*1)+(dnk*2)+(ft*1)+(fg*1)+(tp*3)+(oiq*7)+(diq*3)+(drb*3)+(pss*3)+(reb*1))/38
                    diff = trueOvr - ovr
                    df.loc[index] = [name, age, tm, pos, ovr, trueOvr, diff] + attributes
                    index += 1
                    playerList.append(
                            ((name + " " + str(age)+ " " + pos),
                             trueOvr,
                             ovr,
                             diff,attributes
                             ))
    
    return df, playerList
                    
                    
                    
           


fileName = '2054p.json'
obj = getJSON(fileName)
teamDict = getTIDs(obj)
info = getTrueOvrs("FA", teamDict, 2054)
players = info[1]
spread = info[0]
print(len(players))
players.sort(key=lambda x: x[3])
for player in players:
    print(player[:-1])

spread.to_excel('dii.xlsx', encoding='utf-8', index=False)






