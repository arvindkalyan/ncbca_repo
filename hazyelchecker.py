# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import operator
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
       teamDict[-1] = "DII"
       teamDict[-2] = "Recruit"

    return teamDict

def checkProgRig(post,teamDict):
    season = int(post.get("meta")["phaseText"][0:4])
    riggedList = []
    for item in post.get("players"):
        item2 = item.get("ratings")[-1]
        if item2.get("season") == season:
                name = item.get("firstName") + " " + item.get("lastName")
                hgt2 = item2.get("hgt")
                stre2 = item2.get("stre")
                spd2 = item2.get("spd")
                jmp2 = item2.get("jmp")
                endu2 = item2.get("endu")
                ins2 = item2.get("ins")
                dnk2 = item2.get("dnk")
                ft2 = item2.get("ft")
                fg2 = item2.get("fg")
                tp2 = item2.get("tp")
                oiq2 = item2.get("oiq")
                diq2 = item2.get("diq")
                drb2 = item2.get("drb")
                pss2 = item2.get("pss")
                reb2 = item2.get("reb")
                
                atts2 = [hgt2,stre2,spd2,jmp2,endu2,ins2,dnk2,ft2,fg2,tp2,oiq2,diq2,drb2,pss2,reb2]
                
                
        if (len(item.get("ratings")) > 1):
            item3 = item.get("ratings")[-2]
            if item3.get("season") == season-1:
        
                    hgt = item3.get("hgt")
                    stre = item3.get("stre")
                    spd = item3.get("spd")
                    jmp = item3.get("jmp")
                    endu = item3.get("endu")
                    ins = item3.get("ins")
                    dnk = item3.get("dnk")
                    ft = item3.get("ft")
                    fg = item3.get("fg")
                    tp = item3.get("tp")
                    oiq = item3.get("oiq")
                    diq = item3.get("diq")
                    drb = item3.get("drb")
                    pss = item3.get("pss")
                    reb = item3.get("reb")
                    atts = [hgt,stre,spd,jmp,endu,ins,dnk,ft,fg,tp,oiq,diq,drb,pss,reb]
      
                    diff = list(map(operator.sub, atts2, atts))
                    riggedatts = []
                    if diff[0] > 2:
                        riggedatts.append("hgt: +" + str(diff[0]))        
                    if diff[2] > 2:
                        riggedatts.append("spd: +" + str(diff[2]))
                    if diff[3] > 2: 
                        riggedatts.append("jmp: +" + str(diff[3]))
                    if diff[4] > 19: 
                        riggedatts.append("endu: +" + str(diff[4]))
                    if diff[5] > 13:
                        riggedatts.append("ins: +" + str(diff[5]))
                    if diff[6] > 13: 
                        riggedatts.append("dnk: +" + str(diff[6]))
                    if diff[7] > 13:
                        riggedatts.append("ft: +" + str(diff[7]))
                    if diff[8] > 13:
                        riggedatts.append("fg: +" + str(diff[8]))
                    if diff[9] > 13:
                        riggedatts.append("tp: +" + str(diff[9]))
                    if diff[12] > 5:
                        riggedatts.append("drb: +" + str(diff[12]))
                    if diff[13] > 5:
                        riggedatts.append("pss: +" + str(diff[13]))
                    if diff[14] > 5:
                        riggedatts.append("reb: +" + str(diff[14]))
                    
                    
                    if(len(riggedatts) != 0):
                        riggedList.append((name, teamDict[item.get("tid")], riggedatts))
    riggedList.sort(key = lambda x: (x[1]))
    for i in riggedList:
        print(i)
    print(str(season) + ": " + str(len(riggedList)) + " potentially altered players")
            
def checkProgHistory(post):
    riggedList = []
    for item in post.get("players"):
        for i in range(len(item.get("ratings"))-1,0,-1):
            item2 = item.get("ratings")[i]
            item3 = item.get("ratings")[i-1]
            #if item2.get("season") <= 2051 or item3.get("season") <= 2051:
             #   break
            name = item.get("firstName") + " " + item.get("lastName")
            
            hgt2 = item2.get("hgt")
            stre2 = item2.get("stre")
            spd2 = item2.get("spd")
            jmp2 = item2.get("jmp")
            endu2 = item2.get("endu")
            ins2 = item2.get("ins")
            dnk2 = item2.get("dnk")
            ft2 = item2.get("ft")
            fg2 = item2.get("fg")
            tp2 = item2.get("tp")
            oiq2 = item2.get("oiq")
            diq2 = item2.get("diq")
            drb2 = item2.get("drb")
            pss2 = item2.get("pss")
            reb2 = item2.get("reb")
        
            atts2 = [hgt2,stre2,spd2,jmp2,endu2,ins2,dnk2,ft2,fg2,tp2,oiq2,diq2,drb2,pss2,reb2]

            hgt = item3.get("hgt")
            stre = item3.get("stre")
            spd = item3.get("spd")
            jmp = item3.get("jmp")
            endu = item3.get("endu")
            ins = item3.get("ins")
            dnk = item3.get("dnk")
            ft = item3.get("ft")
            fg = item3.get("fg")
            tp = item3.get("tp")
            oiq = item3.get("oiq")
            diq = item3.get("diq")
            drb = item3.get("drb")
            pss = item3.get("pss")
            reb = item3.get("reb")
            atts = [hgt,stre,spd,jmp,endu,ins,dnk,ft,fg,tp,oiq,diq,drb,pss,reb]
      
            diff = list(map(operator.sub, atts2, atts))
           # print(name + str(diff))
            riggedatts = []
            if diff[0] > 2:
                riggedatts.append("hgt: +" + str(diff[0]))        
            if diff[2] > 2:
                riggedatts.append("spd: +" + str(diff[2]))
            if diff[3] > 2: 
                riggedatts.append("jmp: +" + str(diff[3]))
            if diff[4] > 19: 
                riggedatts.append("endu: +" + str(diff[4]))
            if diff[5] > 13:
                riggedatts.append("ins: +" + str(diff[5]))
            if diff[6] > 13: 
                riggedatts.append("dnk: +" + str(diff[6]))
            if diff[7] > 13:
                riggedatts.append("ft: +" + str(diff[7]))
            if diff[8] > 13:
                riggedatts.append("fg: +" + str(diff[8]))
            if diff[9] > 13:
                riggedatts.append("tp: +" + str(diff[9]))
            if diff[12] > 5:
                riggedatts.append("drb: +" + str(diff[12]))
            if diff[13] > 5:
                riggedatts.append("pss: +" + str(diff[13]))
            if diff[14] > 5:
                riggedatts.append("reb: +" + str(diff[14]))
            
                    
            if(len(riggedatts) != 0):
                riggedList.append((name, item2.get("season"), riggedatts))
    riggedList.sort(key = lambda x: (x[1]))
    for i in riggedList:
        print(i)
    print(str(len(riggedList)) + " potentially altered players")
    
    
def checkPostProgRig(pre, post,teamDict):
    season = int(post.get("meta")["phaseText"][0:4])
    riggedList = []
    currentPlayerNames = {}
    for item in post.get("players"):
        item2 = item.get("ratings")[-1]
        age = season-item["born"].get("year")
        if item2.get("season") == season and age > 18:
    
                name = item.get("firstName") + " " + item.get("lastName")
                city = item.get("city")
                hgt2 = item2.get("hgt")
                stre2 = item2.get("stre")
                spd2 = item2.get("spd")
                jmp2 = item2.get("jmp")
                endu2 = item2.get("endu")
                ins2 = item2.get("ins")
                dnk2 = item2.get("dnk")
                ft2 = item2.get("ft")
                fg2 = item2.get("fg")
                tp2 = item2.get("tp")
                oiq2 = item2.get("oiq")
                diq2 = item2.get("diq")
                drb2 = item2.get("drb")
                pss2 = item2.get("pss")
                reb2 = item2.get("reb")
                
                atts2 = [hgt2,stre2,spd2,jmp2,endu2,ins2,dnk2,ft2,fg2,tp2,oiq2,diq2,drb2,pss2,reb2]
                
                currentPlayerNames[name] = (city,atts2)
    
    for item in pre.get("players"):
        name = item.get("firstName") + " " + item.get("lastName")
        
        if name in currentPlayerNames:
            city = currentPlayerNames[name][0]
            if item.get("city") == city:
                atts2 = currentPlayerNames[name][1]
                item2 = item.get("ratings")[-1]
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
                    atts = [hgt,stre,spd,jmp,endu,ins,dnk,ft,fg,tp,oiq,diq,drb,pss,reb]
                    
                    diff = list(map(operator.sub, atts2, atts))
                    riggedatts = []
                    if diff[0] > 0:
                        riggedatts.append("hgt: +" + str(diff[0]))
                    if diff[1] > 0:
                        riggedatts.append("stre: +" + str(diff[1]))
                    if diff[2] > 0:
                        riggedatts.append("spd: +" + str(diff[2]))
                    if diff[3] > 0: 
                        riggedatts.append("jmp: +" + str(diff[3]))
                    if diff[4] > 0: 
                        riggedatts.append("endu: +" + str(diff[4]))
                    if diff[5] > 0:
                        riggedatts.append("ins: +" + str(diff[5]))
                    if diff[6] > 0: 
                        riggedatts.append("dnk: +" + str(diff[6]))
                    if diff[7] > 0:
                        riggedatts.append("ft: +" + str(diff[7]))
                    if diff[8] > 0:
                        riggedatts.append("fg: +" + str(diff[8]))
                    if diff[9] > 0:
                        riggedatts.append("tp: +" + str(diff[9]))
                    if diff[10] > 0:
                        riggedatts.append("oiq: +" + str(diff[10]))
                    if diff[11] > 0:
                        riggedatts.append("diq: +" + str(diff[11]))
                    if diff[12] > 0:
                        riggedatts.append("drb: +" + str(diff[12]))
                    if diff[13] > 0:
                        riggedatts.append("pss: +" + str(diff[13]))
                    if diff[14] > 0:
                        riggedatts.append("reb: +" + str(diff[14]))
                    
                    
                    if(len(riggedatts) != 0):
                        riggedList.append((name, teamDict[item.get("tid")], riggedatts))
    riggedList.sort(key = lambda x: len(x[2]))
    for i in riggedList:
        print(i)
    print(str(len(riggedList)) + " potentially altered players")
                    

                
    
                    
                    
prog = '2055 NCBCA Returning Talent Export.json'
obj1 = getJSON(prog)                   
           

test = 'purdue.json'
obj2 = getJSON(test)

teamDict = getTIDs(obj1)
print("PROGRESSION")
checkProgRig(obj1, teamDict)
print("------------------------")
print("POST-PROGRESSION")
checkProgHistory(obj1)
#checkPostProgRig(obj1,obj2,teamDict)





