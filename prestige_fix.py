# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json

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
    return teamDict

        

def fixPrestige(json1):
        # Open the file with read only permit

    with open('hype.txt') as f:
        content = f.readlines()
    content = [int(x.strip()) for x in content] 
    
    #for team,prestige in zip(json1.get("teams"),content):
    for team in json1.get("teams"):
        name = team["region"] + " " + team["name"]
        latestseason = team["seasons"][-1]
        print(name + ": current prestige = " + str(100*(latestseason["hype"])))
        #print(season["hype"])
        prestige = input("Press enter to continue, or enter new prestige: ")
        if prestige != "":   
            latestseason["hype"] = int(prestige)/100
    print("All done! Writing to .json now.")


fileName = input("Enter the full name of your .json file: ")
edit = getJSON(fileName)
fixPrestige(edit)
writeJSON(fileName, edit)
print("Ready to go!")

