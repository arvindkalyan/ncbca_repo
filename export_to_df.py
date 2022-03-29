# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:32:07 2022

@author: lotus
"""

import json
import pandas as pd  
import numpy as np

def getJSON(filePath):
    with open(filePath, encoding='utf-8-sig') as f:
        return json.load(f)
    
def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("tid")] = item.get("region")
       
       teamDict[-1] = "TID-1" 
       teamDict[-2] = "TID-2" 
       teamDict[-3] = "TID-3"
       teamDict[-4] = "TID-4"
       teamDict[-5] = "TID-5"

    return teamDict

file = getJSON('Updated 2040 Offseason Export v2.json')
teamDict = getTIDs(file)

### PARAMETERS ###
age = 21
season = 2039
cutoff = 87
toFront = ['name', 'pos', 'ovr', 'age', 'team', 'tid']
#################

df = pd.json_normalize(file["players"], record_path=['ratings'], meta=['name', 'tid','pos',['born', 'year']])

df['age'] = df.apply(lambda x: x['season'] - x['born.year'], axis = 1)
df['team'] = df.apply(lambda x: teamDict[x['tid']], axis = 1)

idx = np.where((df['age']>=age) & (df['season'] == season) & (df['ovr'] >= cutoff))
eligible = df.loc[idx].sort_values(by=['ovr'], ascending=False)

for i, col in enumerate(toFront):
    first_column = eligible.pop(col)
    eligible.insert(i, col, first_column)

eligible.to_csv('draft_eligible{}.csv'.format(season), index=False)


