# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:33:02 2020

@author: arvin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics

import json
import itertools
import math
def getJSON(filePath):
    with open(filePath, encoding='utf-8-sig') as f:
        return json.load(f)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)


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
        
def getPlayers(obj):
    i = 0
    for item in obj.get("players"):
        if( item.get("draft").get("year") > 2040
           and item.get("draft").get("year") < 2051 and item.get("ratings")[-1].get("ovr") <= 70 and
         (item.get("ratings")[-1].get("ovr")-item.get("ratings")[0].get("ovr") <= 9)):
            print(item.get("firstName") + " " + item.get("lastName"))
            #print(item.get("ratings")[0].get('stre'))
            playerList.append((item.get("firstName") + " " + item.get("lastName"), 
             item.get("ratings")[0].get('stre'),
             item.get("ratings")[0].get('spd'),
             item.get("ratings")[0].get('jmp'),
             item.get("ratings")[0].get('endu'),
             item.get("ratings")[0].get('ins'),
             item.get("ratings")[0].get('dnk'),
             item.get("ratings")[0].get('ft'),
             item.get("ratings")[0].get('fg'),
             item.get("ratings")[0].get('tp'),
             item.get("ratings")[0].get('oiq'),
             item.get("ratings")[0].get('diq'),
             item.get("ratings")[0].get('drb'),
             item.get("ratings")[0].get('pss')
             ,item.get("ratings")[0].get('reb'),
             item.get("ratings")[0].get('hgt'),
             item.get("value"))) 
            
            #print(i)
            i += 1
        if(item.get("born").get("year") == 2031 and item.get("tid") == -2 
           and item.get("ratings")[0].get("ovr") < 55):
            print(item.get("firstName") + " " + item.get("lastName"))
            recruitList.append((item.get("firstName") + " " + item.get("lastName"), 
             item.get("ratings")[0].get('stre'),
             item.get("ratings")[0].get('spd'),
             item.get("ratings")[0].get('jmp'),
             item.get("ratings")[0].get('endu'),
             item.get("ratings")[0].get('ins'),
             item.get("ratings")[0].get('dnk'),
             item.get("ratings")[0].get('ft'),
             item.get("ratings")[0].get('fg'),
             item.get("ratings")[0].get('tp'),
             item.get("ratings")[0].get('oiq'),
             item.get("ratings")[0].get('diq'),
             item.get("ratings")[0].get('drb'),
             item.get("ratings")[0].get('pss')
             ,item.get("ratings")[0].get('reb'),
             item.get("ratings")[0].get('hgt'),
             item.get("value"))) 
           
          

fileName = 'temple.json'
playerList = []
recruitList = []
obj = getJSON(fileName)
getPlayers(obj)
#print(playerList)
df = pd.DataFrame(playerList, 
                     columns = ['name' , 'stre', 'spd' , 'jmp', 'endu', 'ins', 'dnk',
                                'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb', 'hgt'
                                , 'value']) 

X = df[['stre', 'spd' , 'jmp', 'endu', 'ins', 'dnk',
                                'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb', 'hgt']]
Y = df['value'].values

df2 = pd.DataFrame(recruitList, 
                     columns = ['name' , 'stre', 'spd' , 'jmp', 'endu', 'ins', 'dnk',
                                'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb', 'hgt'
                                , 'value'])

X2 = df2[['stre', 'spd' , 'jmp', 'endu', 'ins', 'dnk',
                                'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb', 'hgt']]

regressor = LinearRegression()  
regressor.fit(X, Y)
#Y2 = regressor.predict(X2)
print(Y.shape)
coeff_df = pd.DataFrame(regressor.coef_, X.columns, columns=['Coefficient'])  
print(coeff_df)

#df3 = pd.DataFrame({'Predicted': Y2})
#df3.insert(1, "Name", df2['name'])
#df3.to_csv('test', encoding='utf-8', index=False)
#print(df3)
#print(Y2.shape)


