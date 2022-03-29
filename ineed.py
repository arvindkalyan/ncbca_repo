# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:38:57 2020

@author: arvin
"""
import json

def getJSON(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)
        
fileName = 'CFB_Association_2_2035_preseason.json' # put your export here, make sure file name is accurate

obj = getJSON(fileName)
    
writeJSON(fileName, obj) #this takes time! 
    