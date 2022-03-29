# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import itertools
import math
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
       teamDict[item.get("tid")] = item.get("region")
    return teamDict

def getNTHist(teamDict):
    years = []
    seed1 = []
    team1 = []
    score1 = []
    seed2 = []
    team2 = []
    score2 = []
    winner = []
    loser = []
    for year in obj.get("playoffSeries"):
        season = year.get("season")
        for nt in year.get("series"):
            for game in nt:
                years.append(season)
                seed1.append(game.get("home").get("seed"))
                team1.append(teamDict[game.get("home").get("tid")])
                score1.append(game.get("home").get("pts2"))
                seed2.append(game.get("away").get("seed"))
                team2.append(teamDict[game.get("away").get("tid")])
                score2.append(game.get("away").get("pts2"))
                if(game.get("home").get("won") == 1):
                    winner.append(teamDict[game.get("home").get("tid")])
                    loser.append(teamDict[game.get("away").get("tid")])
                else:
                    winner.append(teamDict[game.get("away").get("tid")])
                    loser.append(teamDict[game.get("home").get("tid")])
    data = {'year':years, 'seed1':seed1, 'team1':team1, 'score1': score1, 
            'seed2':seed2, 'team2':team2, 'score2': score2, 'winner':winner, 'loser':loser} 
    return pd.DataFrame(data)

def getCTHist(teamDict):
    years = []
    seed1 = []
    team1 = []
    score1 = []
    seed2 = []
    team2 = []
    score2 = []
    winner = []
    loser = []
    for year in obj.get("playoffSeries2"):
        season = year.get("season")
        for nt in year.get("series"):
            for game in nt:
                years.append(season)
                seed1.append(game.get("home").get("seed"))
                team1.append(teamDict[game.get("home").get("tid")])
                score1.append(game.get("home").get("pts2"))
                seed2.append(game.get("away").get("seed"))
                team2.append(teamDict[game.get("away").get("tid")])
                score2.append(game.get("away").get("pts2"))
                if(game.get("home").get("won") == 1):
                    winner.append(teamDict[game.get("home").get("tid")])
                    loser.append(teamDict[game.get("away").get("tid")])
                else:
                    winner.append(teamDict[game.get("away").get("tid")])
                    loser.append(teamDict[game.get("home").get("tid")])
    data2 = {'year':years, 'seed1':seed1, 'team1':team1, 'score1': score1, 
            'seed2':seed2, 'team2':team2, 'score2': score2, 'winner':winner, 'loser':loser} 
    return pd.DataFrame(data2)

def getRecords(teamDict):
    years = []
    teams = []
    wins = []
    losses = []
    cwins = []
    closses = []
    for team in obj.get("teams"):
        tid = team.get("tid")
        for season in team.get("seasons"):
            years.append(season.get("season"))
            teams.append(teamDict.get(tid))
            wins.append(season.get("won"))
            losses.append(season.get("lost"))
            cwins.append(season.get("wonConf"))
            closses.append(season.get("lostConf"))
    data3 = {'year':years, 'team':teams, 'wins':wins, 'losses': losses, 
            'cwins':cwins, 'closses':closses} 
    return pd.DataFrame(data3)
        


fileName = 'NCBCA 2049 Post-NT.json'
obj = getJSON(fileName)
teamDict = getTIDs(obj)
print(teamDict)
#df = getNTHist(teamDict)
#df2 = getCTHist(teamDict)
df3 = getRecords(teamDict)
df3.groupby('year')
print(df3.head())
#df3.to_csv('standingshistory', encoding='utf-8', index=False)

