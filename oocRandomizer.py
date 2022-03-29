# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:05:52 2020

@author: lotus
"""
#import xlrd 
import random
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

def getAllTeams(sheet):
    teamList = dict(zip(sheet.col_values(1)[78:178],sheet.col_values(16)[78:178]))
    for i in teamList.keys():
        print(i)
    time.sleep(20)
    print(str(len(teamList)))
    return teamList

def getFreeTeams(week, sheet, teamList):
    freeTeams = teamList.copy()
    takenTeams = sheet.col_values(2*week-1)[3:53] + sheet.col_values(2*week)[3:53]
    time.sleep(5)
    for tm in takenTeams:
        if tm in freeTeams:
            
            freeTeams.pop(tm)
       

    return freeTeams
    
def getAllGames(sheet):
    #for week in range(1,13):
        #for r in range(4,54):
            #for c in range(2*week-1,2*week+1,2):
                #print(sheet.cell(r,c).value, sheet.cell(r,c+1).value)
                #time.sleep(4)
    allgames = []
    emptygames = []
    for num in range(4,54):
        games = sheet.row_values(num)[0:24]
        for game in range(0,len(games),2):
            if (games[game] != ''):
                allgames.append((games[game],games[game+1]))
                #print((games[game],games[game+1]))
            else:
                emptygames.append((num, game+1))
    
        
    return allgames, emptygames
            
            
def getRandomOrder(teamList,challenge, allgames, file):
    teams = list(teamList.keys())
    combined = []
    if(len(challenge) > 0):
        confA = []
        confB = []
        for tm in reversed(teams):
            if teamList[tm] == challenge[0]:
                confA.append(teams.pop(teams.index(tm)))

            elif teamList[tm] == challenge[1]:

                confB.append(teams.pop(teams.index(tm)))
        random.shuffle(confA)
        random.shuffle(confB)
        
        for i in range(0,len(confA)):
            if i%2 == 0:
                combined.append(confA.pop())
                combined.append(confB.pop())
            else:
                combined.append(confB.pop())
                combined.append(confA.pop())
                
    
        print(combined)
        print(len(combined))
        print(teams)
        print(len(teams))
    
    random.shuffle(teams)
    dupeIndices = {}

    for i in range(0,len(teams)-1,2):
        if teamList[teams[i]] == teamList[teams[i+1]] or (teams[i],teams[i+1]) in allgames or (teams[i+1],teams[i]) in allgames:
            dupeIndices[i] = teamList[teams[i]]
            
    for index in dupeIndices:
        conf = dupeIndices[index]
        for i in range(0,len(teams)-1,2):
            if teamList[teams[i]] != conf and teamList[teams[i+1]] != conf:
                temp = teams[i]
                teams[i] = teams[index]
                teams[index] = temp
                break
    teams = teams + combined
    for i in range(0,len(teams)-1,2):
        print(teams[i] + teams[i+1])
        if teamList[teams[i]] == teamList[teams[i+1]]:
            print("SAME CONFERENCE", teamList[teams[i]], teamList[teams[i+1]])  
            file.write("SAME CONFERENCE"+ teams[i]+ teams[i+1])
            file.write("\n")
        if (teams[i],teams[i+1]) in allgames or (teams[i+1],teams[i]) in allgames:
            print("DUPLICATE", teamList[teams[i]], teamList[teams[i+1]])
            file.write("DUPLICATE"+ teams[i]+ teams[i+1])
            file.write("\n")

        allgames.append((teams[i],teams[i+1]))

    
    return teams
        
def populateWeek(sheet, week, teams, emptygames):
    c = 2*week-1
    for r in range(4,54):
        if (r, c) in emptygames:
            emptygames.remove((r,c))
            sheet.update_cell(r,c,teams.pop(0))
            sheet.update_cell(r,c+1,teams.pop(0))
            time.sleep(5)
     
                
        



#loc = "Schedule NCBCA 100.xlsx"
#wb = xlrd.open_workbook(loc) 
#sheet = wb.sheet_by_index(2)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Copy of Schedule NCBCA 100").get_worksheet(2)
#print(sheet.cell(4,1).value)
file = open("ineligiblegames.txt","w") 

allgames, emptygames = getAllGames(sheet)
print(type(allgames))
print(type(emptygames))
teamList = getAllTeams(sheet)
file1 = open("founder2.txt","w") 
for i in range(1,13):
    challenge = []
    if i == 3:
        challenge = ['ACC', 'PCC']
    elif i == 4:
        challenge = ['SEC', 'Big North']
    elif i == 6:
        challenge = ['PCC', 'MWC']
    elif i == 8:
        challenge = ['ACC', 'SEC']
    elif i == 10:
        challenge = ['MWC', 'Big North']
    
    teams = getRandomOrder(getFreeTeams(i,sheet,teamList),challenge, allgames, file)
    populateWeek(sheet, int(i), teams, emptygames)
    
file.close()

