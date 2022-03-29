# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:15:09 2021

@author: arvin
"""

import json
import numpy as np
import pandas as pd  


threshold = 20

def getJSON(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)
        

def getClosest(export1, export2, age, ovr, stre, spd, jmp, endu, ins, dnk, ft, fg, tp, oiq, diq, drb, pss, reb, hgt):
    ovrs = []
    for player in export1["players"]:
        prev = 0
        matched = False
        for year in player["ratings"]:
            if matched and (prev != 0 and year["ovr"]-prev >= -5):
                ovrs.append(year["ovr"])
                prev = year["ovr"]
            else:
                p_age = year["season"] - player["born"]["year"]
                if(abs(year["ovr"]-ovr) <= 1 and
                   abs(year["stre"]-stre) <= threshold and
                   abs(year["spd"]-spd) <= threshold and
                   abs(year["jmp"]-jmp) <= threshold and
                   abs(year["endu"]-endu) <= threshold and
                   abs(year["ins"]-ins) <= threshold and
                   abs(year["dnk"]-dnk) <= threshold and
                   abs(year["ft"]-ft) <= threshold and
                   abs(year["fg"]-fg) <= threshold and
                   abs(year["tp"]-tp) <= threshold and
                   abs(year["oiq"]-oiq) <= threshold and
                   abs(year["diq"]-diq) <= threshold and
                   abs(year["drb"]-drb) <= threshold and
                   abs(year["pss"]-pss) <= threshold and
                   abs(year["reb"]-reb) <= threshold and
                   abs(year["hgt"]-hgt) <= threshold and
                   p_age == age):
                    matched = True
                   # print(str(year["season"]) + " " + str(age) + " " + player["firstName"] + " " + player["lastName"])
    for player in export2["players"]:
        matched = False
        for year in player["ratings"]:
            if matched:
                ovrs.append(year["ovr"])
            else:
                p_age = year["season"] - player["born"]["year"]
                if(abs(year["ovr"]-ovr) <= 1 and
                   abs(year["stre"]-stre) <= threshold and
                   abs(year["spd"]-spd) <= threshold and
                   abs(year["jmp"]-jmp) <= threshold and
                   abs(year["endu"]-endu) <= threshold and
                   abs(year["ins"]-ins) <= threshold and
                   abs(year["dnk"]-dnk) <= threshold and
                   abs(year["ft"]-ft) <= threshold and
                   abs(year["fg"]-fg) <= threshold and
                   abs(year["tp"]-tp) <= threshold and
                   abs(year["oiq"]-oiq) <= threshold and
                   abs(year["diq"]-diq) <= threshold and
                   abs(year["drb"]-drb) <= threshold and
                   abs(year["pss"]-pss) <= threshold and
                   abs(year["reb"]-reb) <= threshold and
                   abs(year["hgt"]-hgt) <= threshold and
                   p_age == age):
                    matched = True
                 #   print(str(year["season"]) + " " + str(age) + " " + player["firstName"] + " " + player["lastName"])
   # if(len(ovrs) is not 0):
      #  print(ovrs)
      #  print(np.median(ovrs))
    if(age == 18 or age == 19):
        median = np.nanpercentile(ovrs, 75)
    else:
        median = np.nanpercentile(ovrs, 50)
   # print(ovrs)
    if(len(ovrs) <= 3):
        median = getClosest2(export1, export2, age, ovr, stre, spd, jmp, endu, ins, dnk, ft, fg, tp, oiq, diq, drb, pss, reb, hgt)
    return  median

def getClosest2(export1, export2, age, ovr, stre, spd, jmp, endu, ins, dnk, ft, fg, tp, oiq, diq, drb, pss, reb, hgt):
    ovrs = []
    for player in export1["players"]:
        prev = 0
        matched = False
        for year in player["ratings"]:
            if matched and (prev != 0 and year["ovr"]-prev >= -5):
                ovrs.append()
                prev = year["ovr"]
            else:
                p_age = year["season"] - player["born"]["year"]
                if(abs(year["ovr"]-ovr) == 0 and
                   p_age == age):
                    matched = True
                   # print(str(year["season"]) + " " + str(age) + " " + player["firstName"] + " " + player["lastName"])
    for player in export2["players"]:
        matched = False
        for year in player["ratings"]:
            if matched:
                ovrs.append(year["ovr"])
            else:
                p_age = year["season"] - player["born"]["year"]
                if(abs(year["ovr"]-ovr) == 0 and
                   p_age == age):
                    matched = True
                 #   print(str(year["season"]) + " " + str(age) + " " + player["firstName"] + " " + player["lastName"])
   # if(len(ovrs) is not 0):
      #  print(ovrs)
      #  print(np.median(ovrs))

    median = np.nanpercentile(ovrs, 50)
    #print(ovrs)
    return median
                


fileName = '2056 Offseason w_ JUCOS.json'
obj = getJSON(fileName)

fileName2 = 'NCBCA 2049 Post-NT (1).json'
obj2 = getJSON(fileName2)

df = pd.DataFrame(columns=['Name','Ovr','Median'])

i = 0
for p in obj["players"]:
    ratings = p["ratings"][-1]
    if(p["tid"] == -2 or (p["retiredYear"] == 2056 and ratings["ovr"] > 65 and ratings["ovr"] < 74)):
        name = p["firstName"] + " " + p["lastName"]
        age = 2056 - p["born"]["year"]
        median = getClosest(obj, obj2, age, ratings["ovr"], ratings["stre"], ratings["spd"], ratings["jmp"], ratings["endu"], ratings["ins"], ratings["dnk"], ratings["ft"], ratings["fg"], ratings["tp"], ratings["oiq"], ratings["diq"], ratings["drb"], ratings["pss"], ratings["reb"], ratings["hgt"])
        df.loc[i] = [name, ratings["ovr"], median]
        i+=1
        print(str(i) + name)
df.to_excel('testRanks.xlsx', encoding='utf-8', index=False)

#getClosest(obj, obj2, 18, 68, 44, 54, 52, 58, 49, 52, 67, 65, 68, 74, 70, 70, 54, 50, 54)


