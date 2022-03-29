# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:19:06 2022

@author: arvin
"""
import json
import itertools
import math


import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from importlib import reload
plt=reload(plt)
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics


attrs = ['hgt', 'stre', 'spd', 'jmp', 'endu', 'ins', 'dnk', 'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb']
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
       teamDict[item.get("abbrev")] = item.get("tid")
       teamDict["FA"] = -1
       teamDict["Draft"] = -2

    return teamDict

def getPlayers(obj, ratings, age, years):
    diff_player = []
    for item in obj.get("players"):
        born = item['born']['year']
        for num, rating in enumerate(item.get("ratings")):
            age_player = rating['season']-born
            if age == age_player and abs(ratings['ovr'] - rating['ovr']) < 3:
                next_five = [rating['ovr']]
                for i in range(num+1, min(num+1+years, len(item.get("ratings")))):
                    next_five.append(item.get("ratings")[i]["ovr"])
                #closeMatch = True
                attrDiff = 0
                for attr in attrs:
                    attrDiff += (ratings[attr]-rating[attr])**2
                    #if abs(rating[attr]-ratings[attr]) > 10:
                       # closeMatch = False
                diff_player.append(((attrDiff)**0.5, item["firstName"] + " " + item["lastName"] + ", " + str(rating['season']), next_five))
    return diff_player
                #if closeMatch:
                    #print(item["firstName"] + " " + item["lastName"] + ", " + str(rating['season']))
        
def graph(diffs, years, top, name, age, season, df):
    
    diffs.sort(key=lambda y: y[0])
    top10 = diffs[1:top+1]
    
    x = range(0, years+1)
    weighted_avgs = []
    maxes = []
    mins = []
    for i in x:
        ovrs = []
        weights = []
        
        for match in top10:
            if i < len(match[2]):
                ovrs.append(match[2][i])
                weights.append((1/(1+match[0])))
        #print(ovrs)
        #print(weights)
        if len(ovrs) != 0:
            weighted_avgs.append(np.average(ovrs, weights=weights))
            maxes.append(max(ovrs))
            mins.append(min(ovrs))
    x = range(0, min(years+1, len(weighted_avgs)))
    fig, ax = plt.subplots()      
    
    
    
    plt.fill_between(x, mins, maxes, color="lightgray",linewidth=0, step="mid")
    
    plt.xticks(range(0, years+1))
    plt.yticks(range(30, 85, 5))
    plt.ylabel('ovr')
    plt.title(name + ", " + str(season))
    
   
    for player in top10:
        print(str(player[0]) + ": " + player[1])
        plt.plot(player[2], alpha=0.7)
    plt.plot(x, weighted_avgs, "o--", color="k")
    plt.grid()
    plt.show()
    #print([name, diffs[0][2][0]] + weighted_avgs + [0]*(11 - len(weighted_avgs)) +  [np.mean(weighted_avgs[2:]), np.median(weighted_avgs[2:])] + maxes+ [0]*(11 - len(weighted_avgs)))
    #print(len([name, diffs[0][2][0]] + weighted_avgs + [0]*(11 - len(weighted_avgs)) +  [np.mean(weighted_avgs[2:]), np.median(weighted_avgs[2:])] + maxes+ [0]*(11 - len(weighted_avgs))))
    #print(len([name, season] + weighted_avgs + [0]*(11 - len(weighted_avgs)) +  maxes+ [0]*(11 - len(weighted_avgs))))
    #print(len(df.columns))
    if df is not None:
        df.loc[len(df)] = [name, age, diffs[0][2][0]] + weighted_avgs + [0]*(years + 1 - len(weighted_avgs)) +  [np.mean(weighted_avgs[1:]), np.median(weighted_avgs[1:])] + maxes+ [0]*(years + 1 - len(weighted_avgs))
    
def showPlayer(name, year=None):
    for player in obj.get("players"):
        name_player = player["firstName"] + " " + player["lastName"]
        if name_player == name:
            season = None
            if year != None:
                for rating in player["ratings"]:
                    if rating["season"] == year:
                        season = rating["season"]
                        age = season - player["born"]["year"]
                        ratings = rating
            else:
                season = player["ratings"][-1]["season"]
                age = season - player["born"]["year"]
                ratings = player["ratings"][-1]
            if season == None:
                print(name + ", " + str(year) + " was not found!")
                return
            diffs = getPlayers(obj, ratings, age, years)
            
            graph(diffs, years, top, name_player, age, season, None)

def showTeam(team, year=None, output=False):
    y = []
    my = []
    for i in range(1, years+1):
        y.append("Year"+str(i))
        my.append("MaxYear"+str(i))
    columns = ['Name', 'Age', 'Ovr', 'Year0'] + y + ['Max', 'Median', 'MaxYear0'] + my
    print(columns)
    df = pd.DataFrame(columns=columns)
    for player in obj.get("players"):
        name_player = player["firstName"] + " " + player["lastName"]
        
        if player["tid"] == teamDict[team]:
            season = None
            if year != None:
                for rating in player["ratings"]:
                    if rating["season"] == year:
                        season = rating["season"]
                        age = season - player["born"]["year"]
                        ratings = rating
            else:
                season = player["ratings"][-1]["season"]
                age = season - player["born"]["year"]
                ratings = player["ratings"][-1]
            if season != None:
                diffs = getPlayers(obj, ratings, age, years)
            
                graph(diffs, years, top, name_player, age, season, df)
    if output:
       df.to_excel('{}{}_projections.xlsx'.format(year, team), encoding='utf-8', index=False)


fileName = 'BBGM_BGMDL_2109_draft_lottery.json'
obj = getJSON(fileName)
teamDict = getTIDs(obj)

years = 20
top = 10

showTeam("Draft", year=2109, output=True)
#showTeam("PHI")
#showPlayer("Steve Huntley")


age = 19
ratings = {'hgt': 59,
           'stre': 45,
           'spd': 58,
           'jmp': 53,
           'endu': 21,
           'ins': 32,
           'dnk': 41, 
           'ft': 40,
           'fg': 46,
           'tp': 50, 
           'oiq': 22,
           'diq': 35,
           'drb': 52,
           'pss': 50, 
           'reb': 49,
           'ovr': 41
        }

#diffs = getPlayers(obj, ratings, age, years)

#graph(diffs, years, top)







