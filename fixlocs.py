# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:19:26 2020

@author: arvin
"""
import json
import xlrd 
import copy

def getJSON(filePath):
    with open(filePath, encoding='utf-8-sig') as f:
        return json.load(f)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)


def fixLocs(name, pos, ovr, hometown, hs, obj):

    for item in obj.get("players"):
        fullname = item.get("firstName")[0] + ". " + item.get("lastName")

        ratings = item.get("ratings")[0]
        position = ratings.get("pos")
        overall = ratings.get("ovr") 

        if (fullname in name and pos == position and ovr == overall and item.get("tid") == -5):
            city = hometown.split(", ")[0]
            state = hometown.split(", ")[1]
            if " (IR)" in state:
                state = state.split(" (IR)")[0]
            item["city"] = city
            item["state"] = state
            item["college"] = hs
            return
    print(name)
        

fileName = 'prerecruiting.json'
loc = ("recruit location.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
obj = getJSON(fileName)


for i in range(1,511):
        
        fixLocs(sheet.cell_value(i, 1), sheet.cell_value(i, 2),
           sheet.cell_value(i, 3),sheet.cell_value(i, 18),sheet.cell_value(i, 19),obj)

writeJSON(fileName, obj)