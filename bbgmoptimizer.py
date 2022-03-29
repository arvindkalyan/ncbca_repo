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
      
    teamDict['FA'] = -1
    teamDict["HS0"] = -2
    teamDict["HS1"] = -4
    teamDict["HS2"] = -5
    teamDict[-2] = "HS0"
    teamDict[-4] = "HS1"
    teamDict[-5] = "HS2"
    teamDict["Draft"] = -2
    return teamDict

def threesyn_calc(num):
    return (5/(1+math.exp(-(3*(num-2)))))
def asyn_calc(num):
    return (1/(1+math.exp(-(15*(num-1.75)))) +
            1/(1+math.exp(-(5*(num-2.75)))))
def bsyn_calc(num):
    return (3/(1+math.exp(-(15*(num-0.75)))) +
            1/(1+math.exp(-(5*(num-1.75)))))

def posyn_calc(num):
    return (1/(1+math.exp(-(15*(num-0.75)))))   
def pssyn_calc(num):
    return 3 / (1 + math.exp(-(15 * (num - 0.75)))) + 1 / (1 + math.exp(-(5 * (num - 1.75)))) + 1 / (1 + math.exp(-(5 * (num - 2.75))))
def dpsyn_calc(num):
    return (1/(1+math.exp(-(15*(num-0.75)))))   

def disyn_calc(num):
    return (2/(1+math.exp(-(15*(num-0.75)))))   

def dasyn_calc(num):
    return (1/(1+math.exp(-(5*(num-2)))) +
            1/(1+math.exp(-(5*(num-3.25)))))
    
def rsyn_calc(num):
    return (1/(1+math.exp(-(15*(num-0.75)))) +
            1/(1+math.exp(-(5*(num-1.75)))))

def three(num):
    return (1/(1+math.exp(-(15*(num/100 - 0.59)))))
def aps(num):
    return (1/(1+math.exp(-(15*(num/100 - 0.63)))))
def b(num):
    return (1/(1+math.exp(-(15*(num/100 - 0.68)))))
def podpr(num):
    return (1/(1+math.exp(-(15*(num/100 - 0.61)))))
def di(num):
    return (1/(1+math.exp(-(15*(num/100 - 0.57)))))
    
def perimsyn(num):
    if num < 0:
        return 0
    elif num > 2:
        return 2
    else:
        return num

class Player(object):
    name = ""
    tp = 0
    A=0
    B=0
    Po=0
    Ps=0
    da=0
    Di=0
    dp=0
    R=0
    
    
    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, tp, A, B, Po, Ps, da, Di, dp, R):
        self.name = name
        self.tp = tp
        self.A = A
        self.B = B
        self.Po = Po
        self.Ps = Ps
        self.da = da
        self.Di = Di
        self.dp = dp
        self.R = R
        
    def __str__(self):
        return self.name
        
def getPlayers(team, team2, teamDict, season):
    if "phaseText" in obj.get("meta"):
        season = int(obj.get("meta")["phaseText"][0:4])
    if team and team2 in teamDict:
        teamId = teamDict[team]
        teamId2 = teamDict[team2]
    
            
        for item in obj.get("players"):
            ovr = item.get("ratings")[-1].get("ovr")
            age = season-item["born"]["year"]
            #if item["tid"] == teamId or (ovr > 60 and ovr < 70 and age > 26 and item["tid"] == teamId2):
            #if item.get("firstName") + " " + item.get("lastName") in names or item["tid"] == teamId:
            #if item.get("firstName") + " " + item.get("lastName") in names:
            #if item["tid"] == teamId or item["tid"] == teamId2:
            #if item["tid"] == teamId:
            if item["tid"] > 0:
                print(item.get("firstName")[0] +  ". " + item.get("lastName") + str(item["value"]))
                
                #print(item)
                item2 = item.get("ratings")[-1]
                if item2.get("season") == season:
                        
                    hgt = item2.get("hgt")
                    stre = item2.get("stre")
                    spd = item2.get("spd")
                    jmp = item2.get("jmp")
                    ins = item2.get("ins")
                    tp = item2.get("tp")
                    oiq = item2.get("oiq")
                    diq = item2.get("diq")
                    drb = item2.get("drb")
                    pss = item2.get("pss")
                    reb = item2.get("reb")
                    
                    
                    '''print("3 " + str(synergy((tp + 0.2 * (hgt-25))/1.1)))
                    print("A " + str(synergy((stre + spd + jmp + (hgt-25))/3.5)))
                    print("B " + str(synergy((drb + spd)/2)))
                    print("Di " + str(synergy((4 * (hgt-25) + stre + 0.5 * spd + 0.5 * jmp + blk)/5)))
                    print("Dp " + str(synergy(((hgt-25) + stre + 2 * spd + 0.5 * jmp + stl)/5)))
                    print("Po " + str(synergy((2*(hgt-25) + 0.6 * stre + 0.2 * spd + ins)/2.8)))
                    print("Ps " + str(synergy((0.4 * drb + pss)*1.4)))
                    print("R " + str(synergy((3 * (hgt-25) + 0.1 * stre + 0.1 * jmp + 0.7 * reb)/2.4)))'''
                    
                    playerList.append(Player(item.get("firstName") +  " " + item.get("lastName") + " " + str(item2["ovr"]), 
                                            three(((0.1*oiq)+tp)/1.1),
                                            aps((stre+spd+jmp+(0.75*hgt))/3.75),
                                            b((drb+spd)/2),
                                            podpr(((hgt)+(0.6*stre)+(0.2*spd)+ins+(0.4*oiq))/(1+0.6+0.2+1+0.4)),
                                            aps(((0.4*drb)+pss+(0.5*oiq))/1.9),
                                            aps((stre+spd+jmp+(0.75*hgt))/3.75),
                                            di(((2.5*hgt)+stre+(0.5*spd)+(0.5*jmp)+(2*diq))/(2.5+1+0.5+0.5+2)),
                                            podpr(((0.5*hgt)+(0.5*stre)+(2*spd)+(0.5*jmp)+diq)/(0.5+0.5+2+0.5+1)),
                                            podpr(((2*hgt)+(0.1*stre)+(0.1*jmp)+(2*reb)+(0.5*oiq)+(0.5*diq))/5.2)
                                            ))
                        
                    
           


fileName = 'BBGM_BGMDL_2110_draft_lottery.json'
names = []
playerList = []
lineupList = []
obj = getJSON(fileName)
teamDict = getTIDs(obj)
getPlayers("Philadelphia", "Draft", teamDict, 2110)
print("P----------------------------------")
i = 1
tp = 0
a = 0
B = 0
po = 0
ps = 0
perim = 0
da = 0
Di = 0
dp = 0
r = 0
osyn = 0
dsyn = 0
Rsyn = 0
set = 0
f = open("throwaway.txt", "w")

for subset in itertools.combinations(playerList, 1):
    tp = 0
    a = 0
    B = 0
    po = 0
    ps = 0
    da = 0
    Di = 0
    dp = 0
    r = 0
    osyn = 0
    dsyn = 0
    Rsyn= 0
    perim = 0
    set = 0
    for item2 in subset:
        #print(item2)
        tp += item2.tp
        a += item2.A
        B += item2.B
        po += item2.Po
        ps += item2.Ps
        da += item2.da
        Di += item2.Di
        dp += item2.dp
        r += item2.R
        print(tp, a, B, po, ps, da, Di, dp, r)
    
        #if item2.name == "David Morton" or item2.name == "William Woodard" or item2.name == "Harvey McNair":
         #   set+=1
    perim = perimsyn((math.sqrt(1+tp+B+ps)-1)/2)
    #print("###")
    
    tpsyn = threesyn_calc(tp)
    asyn = asyn_calc(a)
    bsyn = bsyn_calc(B)
    posyn = posyn_calc(po)
    pssyn = pssyn_calc(ps)
    disyn = disyn_calc(Di)
    dpsyn = dpsyn_calc(dp)
    dasyn = dasyn_calc(da)
    rsyn = rsyn_calc(r)
    
    osyn = ((tpsyn + asyn + bsyn +  posyn + pssyn)/17)*(0.5 + 0.5 * perim)
    dsyn = (disyn + dpsyn + dasyn)/6
    Rsyn = rsyn/4
    #print(str(osyn))
    #print(str(dsyn))
  #  if set == 3:
    lineupList.append((osyn+dsyn+Rsyn, subset, osyn, dsyn, Rsyn, osyn * dsyn))
    
    
lineupList.sort(key=lambda x: x[3])
for item in lineupList[-25:]:
    for player in item[1]:
        print(player)
        f.write(str(player) + "\n")

    print("O: " + str(round(item[2], 3)) + " D: " + str(round(item[3], 2)) + " R: " + str(round(item[4],2)))
    f.write("O: " + str(round(item[2],2)) + " D: " + str(round(item[3],2)) + " R: " + str(round(item[4],2)) + "\n")
    print("----------")
    f.write("----------"+ "\n")
f.close()





