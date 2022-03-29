# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 08:25:00 2018

@author: lotus
"""

import json
import xlrd 

def getJSON(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("region")] = item.get("tid")
    return teamDict 

def assign(name, position, age, ovr, newTeam, teamDict, year):
    year = int(obj.get("meta")["phaseText"][0:4]) 
    if newTeam != '' and newTeam[-1] == " ":
        newTeam = newTeam[:-1]
    
    if newTeam in teamDict:
        teamId = teamDict[newTeam]
        for player in obj.get("players"):
            if(name[0] == player.get("name")[0] and name[3:] in player.get("name")
               and position == player.get("pos") and age == year-player.get("born")["year"]
              and ovr == player.get("ratings")[-1].get("ovr")):
           # if(name[0] == player.get("name")[0] and name[3:] in player.get("name") and age == year-player.get("born")["year"]):
            #    print(player.get("pos"),player.get("ratings")[-1].get("ovr") )
                player["tid"] = teamId
                #print(newTeam)
                print("PLAYER FOUND", name)

                



       
def updateStatesAndAges(name, position, ovr, state)         :
    year = int(obj.get("meta")["phaseText"][0:4]) 
    toDelete = []
    for player in obj.get("players"):

        if(player.get("tid") >= 0):
            toDelete.append(obj["players"].index(player))
        if(name[0] == player.get("name")[0] and name[3:] in player.get("name")
                and position == player.get("pos") and ovr == player.get("ratings")[-1].get("ovr")
                and player.get("tid") == -2):
            player["born"]["year"] = year-18
            player["state"] = state
            print(str(i+1) + name + str(state) + str(year-18))
    print("Deleting now...")
    for index in sorted(toDelete, reverse=True):
        del obj["players"][index]
    print("Deleting done.")


### ENTER 0 FOR ASSIGNER, 1 FOR RECRUITS AND STATES
task = input("Enter 0 for assigner, 1 for recruits and states: ")
### ENTER 0 FOR ASSIGNER, 1 FOR RECRUITS AND STATES 
 
fileName = 'playersonly.json' # put your export here, make sure file name is accurate
loc = ("Recruit States.xlsx") # can either be NZCFL Info or the recruit states sheet

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(task) # pass in 0 for NZCFL Info 1st sheet, 1 for recruit states sheet 2nd page
obj = getJSON(fileName)

if task == 0:
    teamDict = getTIDs(obj)
    for i in range(4,1884):
        print(sheet.cell_value(i, 1), sheet.cell_value(i, 2), 
            sheet.cell_value(i, 3), sheet.cell_value(i,4), sheet.cell_value(i, 17))
        assign(sheet.cell_value(i, 1), sheet.cell_value(i, 2), 
            sheet.cell_value(i, 3), sheet.cell_value(i,4), sheet.cell_value(i, 17), teamDict, 2033)

else:
    reversedstates = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
    states = dict((v,k) for k,v in reversedstates.items())
    for i in range(0,1880): # do range (0,1255) for assigning recruits, (0,1880) for states and ages


        updateStatesAndAges(sheet.cell_value(i, 1), sheet.cell_value(i, 2), 
               sheet.cell_value(i, 4), states.get(sheet.cell_value(i,6),sheet.cell_value(i,6)))
    

print("Writing to .JSON now...")
#writeJSON(fileName, obj) #this takes time! 
    




