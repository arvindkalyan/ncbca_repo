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
       teamDict['Miami'] = 12
       teamDict['UConn'] = 22
       teamDict['UMass'] = 7
       teamDict['Loyola'] = 65
       teamDict['Florida State'] = 65
    return teamDict

def threesyn(num):
    return (5/(1+math.exp(-(3*(num-2)))))
def asyn(num):
    return (1/(1+math.exp(-(15*(num-1.75)))) +
            1/(1+math.exp(-(5*(num-2.75)))))
def bsyn(num):
    return (1/(1+math.exp(-(15*(num-0.75)))) +
            1/(1+math.exp(-(5*(num-1.75)))))

def posyn(num):
    return (1/(1+math.exp(-(15*(num-0.75)))))   
def pssyn(num):
    return 3 / (1 + math.exp(-(15 * (num - 0.75))) + 1 / (1 + math.exp(-(5 * (num - 1.75))) + 1 / (1 + math.exp(-(5 * (num - 2.75))))))
def dpsyn(num):
    return (1/(1+math.exp(-(15*(num-0.75)))))   

def disyn(num):
    return (2/(1+math.exp(-(15*(num-0.75)))))   

def dasyn(num):
    return (1/(1+math.exp(-(5*(num-2)))) +
            1/(1+math.exp(-(5*(num-3.25)))))
    
def rsyn(num):
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
        
def getPlayers(team, teamDict, season):
    name = ''
    nameList = []
    if team in teamDict:
        teamId = teamDict[team]
        for item in obj.get("players"):
            name = item.get("firstName")[0] + ". " + item.get("lastName")
            if (name in open('targets.txt').read()) and (item.get("year") == 'HS'):
            #if item["tid"] == teamId:
            #if (item["tid"] == teamId or (name in open('targets.txt').read()) and (item.get("year") == 'HS')):
                print(item.get("firstName")[0] +  ". " + item.get("lastName"))
                
                #print(item)
                for item2 in item.get("ratings"):
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
                    if name not in nameList:    
                        playerList.append(Player(item.get("firstName")[0] +  ". " + item.get("lastName"), 
                                                three(((0.1*oiq)+tp)/1.1),
                                                aps((stre+spd+jmp+(0.75*hgt))/3.75),
                                                b((drb+spd)/2),
                                                podpr(((2*hgt)+(0.6*stre)+(0.2*spd)+ins+(0.2*oiq))/(2+0.6+0.2+1+0.2)),
                                                aps(((0.4*drb)+pss+(0.5*oiq))/1.9),
                                                aps((stre+spd+jmp+(0.75*hgt))/3.75),
                                                di(((2.5*hgt)+stre+(0.5*spd)+(0.5*jmp)+(2*diq))/(2.5+1+0.5+0.5+2)),
                                                podpr(((0.5*hgt)+(0.5*stre)+(2*spd)+(0.5*jmp)+diq)/(0.5+0.5+2+0.5+1)),
                                                podpr(((2*hgt)+(0.1*stre)+(0.1*jmp)+(2*reb)+(0.5*oiq)+(0.5*diq))/5.2)
                                                ))
                        
                        nameList.append(name)


                    
           



fileName = 'prestige.json'
playerList = []
lineupList = []
obj = getJSON(fileName)
teamDict = getTIDs(obj)
getPlayers("San Diego State", teamDict, 2049)

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
for subset in itertools.combinations(playerList, 1):
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
        
    
        #if item2.name == "David Morton" or item2.name == "William Woodard" or item2.name == "Harvey McNair":
         #   set+=1
    perim = (math.sqrt(1+tp+B+ps)-1)/2
    #print("###")
    
    osyn = ((threesyn(tp) + asyn(a) + bsyn(B) + posyn(po) + pssyn(ps))/17)*(0.5 + 0.5 * perim)
    dsyn = (disyn(Di) + dpsyn(dp) + dasyn(da))/6
    Rsyn = rsyn(r)/6
    #print(str(osyn))
    #print(str(dsyn))
  #  if set == 3:
    lineupList.append((osyn+dsyn+0.75*Rsyn, subset, osyn, dsyn, Rsyn))
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
    
lineupList.sort(key=lambda x: x[4])
for item in lineupList[-10:]:
    for player in item[1]:
        print(player)
    print("O: " + str(item[2]) + " D: " + str(item[3]) + " R: " + str(item[4]) )
    print("----------")
print(len(lineupList))

    




