# -*- coding: utf-8 -*-
import urllib.request
import json
import pandas as pd  
import math
import numpy as np
import sys
import random     

#import dataframe_image as dfi

def getJSON_OBS(filePath):  
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def getJSON(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        return data

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("region")] = item.get("tid")
       teamDict[item.get("tid")] = item.get("region")
    teamDict["HS0"] = -2
    teamDict["HS1"] = -4
    teamDict["HS2"] = -5
    teamDict[-2] = "HS0"
    teamDict[-4] = "HS1"
    teamDict[-5] = "HS2"
    teamDict["Draft"] = -2
    teamDict["All"] = -100
    return teamDict
    
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
def perimsyn(num):
    if num < 0:
        return 0
    elif num > 2:
        return 2
    else:
        return num

def bound(low, high, value):
    if value < low:
        return low
    if value > high: 
        return high
    return value

def shootingFormula(age):
    if age <= 27:
        i = 0
    elif age <= 29:
        i = 0.5
    elif age <= 31:
        i = 1.5
    else:
        i = 2
    return (i, (-3, 13))

def iqFormula(age):
    if age <= 21:
        base = 4
    elif age <= 23:
        base = 0.5
    elif age <= 27:
        base = 0
    elif age <= 29:
        base = 0.5
    elif age <= 31:
        base = 1.5
    else:
        base = 2
    if age >= 24:
        return (base, (-3, 9))
    else:
        return (base, (-3, 7 + 5 * (24 - age)))

def ratingFormula(rtg, age):
    val, lim = 0, (-99,99)
    if rtg == 'spd':
        if age <= 27:
            val = 0
        elif age <= 30:
            val = -2
        elif age <= 35: 
            val = -3
        elif age <= 40:
            val = -4
        else:
            val = -8
        lim = (-12, 2)
    if rtg == 'jmp':
        if age <= 26:
            val = 0
        elif age <= 30:
            val = -3
        elif age <= 35: 
            val = -4
        elif age <= 40:
            val = -5
        else:
            val = -10
        lim = (-12, 2)
    if rtg == 'end':
        if age <= 26:
            val = random.uniform(0, 9)
        elif age <= 30:
            val = 0
        elif age <= 35: 
            val = -2
        elif age <= 40:
            val = -4
        else:
            val = -8
        lim = (-11, 19)
    if rtg == 'dnk':
        if age <= 27:
            val = 0
        else:
            val = 0.5
        lim = (-12, 2)
    if rtg == 'ins' or rtg == 'ft' or rtg == 'fg' or rtg == 'tp':
        val, lim = shootingFormula(age)
    if rtg == 'oiq' or rtg == 'diq':
        val, lim = iqFormula(age)
    if rtg == 'drb' or rtg == 'pss' or rtg == 'reb':
        val, lim = shootingFormula(age)
        lim = (-2, 5)
    return val, lim

def calcBaseChange(age):
    if age <= 21:
        val = 2
    elif age <= 25:
        val = 1
    elif age <= 27:
        val = 0
    elif age <= 29:
        val = -1
    elif age <= 31:
        val = -2
    elif age <= 34:
        val = -3
    elif age <= 40:
        val = -4
    elif age <= 43:
        val = -5
    else:
        val = -6  
    if age <= 23:
        val += bound(-4, 20, random.gauss(0,5))
    elif age <= 25:
        val += bound(-4, 10, random.gauss(0,5))
    else:
        val += bound(-2, 4, random.gauss(0,3))
    return val
        
def getOvr(value, true = False):
    if true:
        return value
    if value >= 68.:
        return round(value+8.)
    elif value >= 50.:
        return round(value+ (4. + ((value - 50.) * (4. / 18.))))
    elif value >= 42.:
        return round(value+ (-5. + (value -42.) * (10. / 8.)))
    elif value >= 31.:
        return round(value+ (-5. - (42.-value) * (5. / 11.) ))
    else:
        return round(value -10.)
    

def progress(player_df):
    oldOvr = getOvr((0.159 * (player_df['hgt'] - 47.5) +
		0.0777 * (player_df['str'] - 50.2) +
		0.123 * (player_df['spd'] - 50.8) +
		0.051 * (player_df['jmp'] - 48.7) +
		0.0632 * (player_df['end'] - 39.9) +
		0.0126 * (player_df['ins'] - 42.4) +
		0.0286 * (player_df['dnk'] - 49.5) +
		0.0202 * (player_df['ft'] - 47.0) +
		0.0726 * (player_df['tp']- 47.1) +
		0.133 * (player_df['oiq'] - 46.8) +
		0.159 * (player_df['diq'] - 46.7) +
		0.059 * (player_df['drb'] - 54.8) +
		0.062 * (player_df['pss'] - 51.3) +
		0.01 * (player_df['fg']- 47.0) +
		0.01 * (player_df['reb'] - 51.4) +
		48.5), true = False)
    age = player_df["age"]
    baseChange = calcBaseChange(age)
    rtgs = ['hgt', 'str', 'spd', 'jmp', 'end', 'dnk', 'ins', 'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb']
    new_ratings = {}
    for rtg in rtgs:
        #print(rtg)
        old_rtg = player_df[rtg]
        new_ratings[rtg] = old_rtg
        if rtg == 'hgt':
            hgtRand = random.random()
            if hgtRand > 0.99 and age <= 20:
                new_ratings[rtg] += 1
            if hgtRand > 0.999:
                new_ratings[rtg] += 1
        else:
            ageModifier, limits = ratingFormula(rtg, age)
            new_ratings[rtg] = int(bound(0, 100, old_rtg + bound(limits[0], limits[1], (baseChange + ageModifier) * random.uniform(0.4, 1.4))))
        #print((old_rtg, new_ratings[rtg], new_ratings[rtg] - old_rtg))
    newOvr = getOvr((0.159 * (new_ratings['hgt'] - 47.5) +
		0.0777 * (new_ratings['str'] - 50.2) +
		0.123 * (new_ratings['spd'] - 50.8) +
		0.051 * (new_ratings['jmp'] - 48.7) +
		0.0632 * (new_ratings['end'] - 39.9) +
		0.0126 * (new_ratings['ins'] - 42.4) +
		0.0286 * (new_ratings['dnk'] - 49.5) +
		0.0202 * (new_ratings['ft'] - 47.0) +
		0.0726 * (new_ratings['tp']- 47.1) +
		0.133 * (new_ratings['oiq'] - 46.8) +
		0.159 * (new_ratings['diq'] - 46.7) +
		0.059 * (new_ratings['drb'] - 54.8) +
		0.062 * (new_ratings['pss'] - 51.3) +
		0.01 * (new_ratings['fg']- 47.0) +
		0.01 * (new_ratings['reb'] - 51.4) +
		48.5), true = False)
    
    tp = three(((0.1*new_ratings['oiq'])+new_ratings['tp'])/1.1)
    a = aps((new_ratings['str']+new_ratings['spd']+new_ratings['jmp']+(0.75*new_ratings['hgt']))/3.75)
    B = b((new_ratings['drb']+new_ratings['spd'])/2)
    po = podpr(((new_ratings['hgt'])+(0.6*new_ratings['str'])+(0.2*new_ratings['spd'])+new_ratings['ins']+(0.4*new_ratings['oiq']))/(1+0.6+0.2+1+0.4))
    ps = aps(((0.4*new_ratings['drb'])+new_ratings['pss']+(0.5*new_ratings['oiq']))/1.9)
    da = aps((new_ratings['str']+new_ratings['spd']+new_ratings['jmp']+(0.75*new_ratings['hgt']))/3.75)
    Di = di(((2.5*new_ratings['hgt'])+new_ratings['str']+(0.5*new_ratings['spd'])+(0.5*new_ratings['jmp'])+(2*new_ratings['diq']))/(2.5+1+0.5+0.5+2))
    dp = podpr(((0.5*new_ratings['hgt'])+(0.5*new_ratings['str'])+(2*new_ratings['spd'])+(0.5*new_ratings['jmp'])+new_ratings['diq'])/(0.5+0.5+2+0.5+1))
    r = podpr(((2*new_ratings['hgt'])+(0.1*new_ratings['str'])+(0.1*new_ratings['jmp'])+(2*new_ratings['reb'])+(0.5*new_ratings['oiq'])+(0.5*new_ratings['diq']))/5.2)
    
    tpsyn = threesyn_calc(tp)
    asyn = asyn_calc(a)
    bsyn = bsyn_calc(B)
    posyn = posyn_calc(po)
    pssyn = pssyn_calc(ps)
    disyn = disyn_calc(Di)
    dpsyn = dpsyn_calc(dp)
    dasyn = dasyn_calc(da)
    rsyn = rsyn_calc(r)
    
    perim = bound(0, 2, (math.sqrt(1+tp+B+ps)-1)/2)
    
    osyn = ((tpsyn + asyn + bsyn +  posyn + pssyn)/17)*(0.5 + 0.5 * perim)
    dsyn = (disyn + dpsyn + dasyn)/6
    Rsyn = rsyn/4
    
    new_ratings['age'] = age+1
    new_ratings['ovr'] = newOvr
    new_ratings['oldovr'] = oldOvr
    new_ratings['osyn'] = osyn
    new_ratings['dsyn'] = dsyn
    new_ratings['rsyn'] = Rsyn
    #print((oldOvr, newOvr, newOvr-oldOvr))
    return new_ratings
    

def avgProg(obj, teamDict, team, season, names = []):
    tid = teamDict[team]
    i = 0
    cols = ["name", "ovr", "oldovr", "age", "pos","hgt", "str", "spd", "jmp", "end", "ins", "dnk", "ft", "fg", "tp", "oiq", "diq", "drb", "pss", "reb"]
    player_df = pd.DataFrame(columns = cols)
    prog_cols = ["name", "age", "pos", "oldovr", "oldtrueovr"]
    for i in range(19, 45):
        prog_cols.append(str(i)+"ovr")

    prog_cols.append("prime_avg")
    prog_cols.append("max")
    prog_cols.append("max_age")        
    for i in range(19, 45):
        prog_cols.append("75_"+str(i)+"ovr")
    
    prog_cols.append("75_prime_avg")
    for i in range(19, 45):
        prog_cols.append(str(i)+"osyn")
    prog_cols.append("prime_osyn")
    
    for i in range(19, 45):
        prog_cols.append(str(i)+"dsyn")
    prog_cols.append("prime_dsyn")
    
    for i in range(19, 45):
        prog_cols.append(str(i)+"rsyn")
    prog_cols.append("prime_rsyn")
    
    for i in range(19, 45):
        prog_cols.append("75_"+str(i)+"osyn")
    prog_cols.append("75_prime_osyn")
    
    for i in range(19, 45):
        prog_cols.append("75_"+str(i)+"dsyn")
    prog_cols.append("75_prime_dsyn")
    
    for i in range(19, 45):
        prog_cols.append("75_"+str(i)+"rsyn")
    prog_cols.append("75_prime_rsyn")
    
    progs_df = pd.DataFrame(columns = prog_cols)
    for player in obj["players"]:
        name = player["firstName"] + " " + player["lastName"]
        if name.lower() in names or (team == "All" and player["tid"]> 0) or (team != "Draft" and player["tid"] == tid) or (team == "Draft" and player["draft"]["year"] == season):
            ratings = player["ratings"][-1]
            age = ratings["season"] - player["born"]["year"]
            player_df.loc[i] = (player["firstName"] + " " + player["lastName"], ratings["ovr"],ratings["ovr"], age, ratings["pos"], ratings["hgt"], ratings["stre"], ratings["spd"], ratings["jmp"], ratings["endu"], ratings["ins"], ratings["dnk"], ratings["ft"], ratings["fg"], ratings["tp"], ratings["oiq"], ratings["diq"], ratings["drb"], ratings["pss"], ratings["reb"])
            i+=1
    for i in range(player_df.shape[0]):
        
        progs = dict((age,{"ovr": [], "osyn": [], "dsyn": [], "rsyn": []}) for age in range(19, 45))
        #print(i)
        #print(player_df.iloc[i])
        progs_df.loc[i, "name"] = player_df.iloc[i]["name"]
        progs_df.loc[i, "age"] = player_df.iloc[i]["age"]
        progs_df.loc[i, "pos"] = player_df.iloc[i]["pos"]
        progs_df.loc[i, "oldtrueovr"] = player_df.iloc[i]["oldovr"]
        progs_df = progs_df.sort_values(by=['oldovr'], ascending = False)
        sys.stdout.write('\r'+"Simulating {} of {}".format(i+1, player_df.shape[0]))
        iterations = 100
        #print(player_df.iloc[i]["name"])
        for it in range(iterations):
            p = player_df.iloc[i]
            p = progress(p)
            progs_df.loc[i, "oldovr"] = p["oldovr"]
            #print(p)
            while p['age'] != 44:
                p = progress(p)
                progs[p['age']]['ovr'].append(p['ovr'])
                progs[p['age']]['osyn'].append(p['osyn'])
                progs[p['age']]['dsyn'].append(p['dsyn'])
                progs[p['age']]['rsyn'].append(p['rsyn'])
        top = [-1, -1]
        for age, progs in progs.items():
            for stat, rtgs in progs.items():
                #print(stat)
                #print(rtgs)
                if type(rtgs) != str:
                    if len(rtgs) == 0:
                        progs_df.loc[i, str(age)+stat] = np.nan
                    else:
                        progs_df.loc[i, str(age)+stat] = np.percentile(rtgs, 50)
                        progs_df.loc[i, "75_"+str(age)+stat] = np.percentile(rtgs, 75)
                        if stat == "ovr" and max(rtgs) > top[0]:
                            top = [max(rtgs), age]
            progs_df.loc[i, "max"] = top[0]
            progs_df.loc[i, "max_age"]= top[1]
            sys.stdout.flush()
    sys.stdout.flush()
        
    progs_df["prime_avg"] = progs_df[[str(i)+"ovr" for i in range(24, 31)]].mean(axis = 1)
    
    progs_df["prime_osyn"] = progs_df[[str(i)+"osyn" for i in range(24, 31)]].mean(axis = 1)
    progs_df["prime_dsyn"] = progs_df[[str(i)+"dsyn" for i in range(24, 31)]].mean(axis = 1)
    progs_df["prime_rsyn"] = progs_df[[str(i)+"rsyn" for i in range(24, 31)]].mean(axis = 1)
    
    progs_df["75_prime_avg"] = progs_df[["75_"+str(i)+"ovr" for i in range(24, 31)]].mean(axis = 1)
    
    progs_df["75_prime_osyn"] = progs_df[["75_"+str(i)+"osyn" for i in range(24, 31)]].mean(axis = 1)
    progs_df["75_prime_dsyn"] = progs_df[["75_"+str(i)+"dsyn" for i in range(24, 31)]].mean(axis = 1)
    progs_df["75_prime_rsyn"] = progs_df[["75_"+str(i)+"rsyn" for i in range(24, 31)]].mean(axis = 1)
    return progs_df.reset_index(drop=True)

    
season = 2113     
team = "Draft"  
fileName = 'BBGM_BGMDL_2113_draft.json'
obj = getJSON_OBS(fileName)
teamDict = getTIDs(obj) 

for i in obj["players"]:
    if i["lastName"] == "Medlock" and i["tid"] == -2:
        print(i)
    
p = avgProg(obj, teamDict, team, season)

print(p)
p.to_excel('{}{}.xlsx'.format(season, team), encoding='utf-8', index=True)



#progress(getProfile(obj, "george hooper", teamDict)[0])






