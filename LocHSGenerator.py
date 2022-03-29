# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 00:21:39 2020

@author: lotus
"""

import xlrd
import random
from math import cos, asin, sqrt, pi
import pandas as pd  

def pause(i):
    if(i <= 40):
        print("...")
        #time.sleep(1) 
    

def updateExport(name, location, hs):
    pass # to integrate with export- have not worked on this 

def generateLoc(locations,i,name):
    print("#"+str(i) + " " + name)
    pause(i)
    keys = list(locations.keys())
    rand = random.random()
    print("Random location number: " + str(rand))
    pause(i)
    for i in range(0,len(keys)):
        if keys[i] == rand:
            key = keys[i]
            break
        if keys[i] > rand:
            key = keys[i-1]
            break
    print("Hometown: " + locations[key][0][0] + ", " + locations[key][0][1])
    return(locations[key])

def haversine(coords1,coords2):
    lat1 = (coords1[0])*pi/180
    lat2 = (coords2[0])*pi/180
    long1 = (coords1[1])*pi/180
    long2 = (coords2[1])*pi/180
    
    latDiff = lat1-lat2
    longDiff = long1-long2
    
    hav = ((1-cos(latDiff))/2) + ((cos(lat1))*(cos(lat2))*((1-cos(longDiff))/2)) 
    return 7917.5*sqrt(asin(hav))
    

def generateHS(location,t50,t250,t1500Cities,t1500Coords,i,name, cityToCoords):
    pause(i)
    print("#"+str(i) + " " + name + ": " + str(location))
    rng = 1
    
    if i <= 250:
    
        if i <= 30:
            leaveState = random.randint(1,15)
            rng = 15
        elif i <= 90:
            leaveState = random.randint(1,20)
            rng = 20
        elif i <= 150:
            leaveState = random.randint(1,25)
            rng = 25
        else:
            leaveState = random.randint(1,30)
            rng = 30
        print("Leave state for a top-50 school? (Range = 1-" + str(rng) + ", >3 for international, =10 for domestic)")
        pause(i)
        print(str(leaveState))
        pause(i)
        if type(location) == str:
            if len(location.split(", ")[-1]) != 2:
                if (i <= 150 and leaveState > 3) or (i > 150 and leaveState > 5): 
                    leaveState = 10
                else:
                    return
            else:
                city = location.split(", ")[-2]
                state = location.split(", ")[-1]
        else:
            city = location[0][0]
            state = location[0][1]
            coords = location[1]
              
        if leaveState == 10:
            random.shuffle(t50)
            print("High School: " + t50[0])
            return t50[0]
        
        if i <= 30:
            inStateT250 = random.randint(1,5)
            rng = 5
        elif i <= 75:
            inStateT250 = random.randint(1,7)
            rng = 7
        elif i <= 100:
            inStateT250 = random.randint(1,10)
            rng = 10
        elif i <= 150:
            inStateT250 = random.randint(1,15)
            rng = 15
        else:
            inStateT250 = random.randint(1,20)
            rng = 20
        print("Stay in-state and attend a top-250 school? (Range = 1-" + str(rng) + ", =5)")
        pause(i)
        print(inStateT250)
        pause(i)
        
        if inStateT250 == 5:
            eligibleSchools = list(filter(lambda x: x[1] == state, t250))
            if len(eligibleSchools) == 0:
                print("No top-250 HS found in " + state)
            else:
                random.shuffle(eligibleSchools)
                print("High School: " + eligibleSchools[0][0])
                return eligibleSchools[0][0]
    else:
        if type(location) != str:
            city = location[0][0]
            state = location[0][1]
            coords = location[1]
        else:
            city = location.split(", ")[-2]
            state = location.split(", ")[-1]
    print("Player will be staying local!")

    if city in t1500Cities:
        eligibleSchools = t1500Cities[city]
        print(str(len(eligibleSchools)) + " top-1500 schools found in " + city + ".")
        random.shuffle(eligibleSchools)
        pause(i)
        print("High School: " + eligibleSchools[0])
        return eligibleSchools[0]
    else:
        print("0 top-1500 schools found in " + city + ". Choosing closest HS in top-1500:")
        if city + ", " + state in cityToCoords:
            keys = list(t1500Coords.keys())
            keys.sort(key= lambda x: haversine(coords,(x[0],x[1])))
            eligibleSchools = t1500Coords[keys[0]]
            random.shuffle(eligibleSchools)
            pause(i)
            print("High School: " + eligibleSchools[0])
            return eligibleSchools[0]
     
        
    
    print("No high school found!")
    
    return ""



loc = ("NCBCA Recruit Locations Generator.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(1)


loc2 = ("High School Randomizer.xlsx")
wb2 = xlrd.open_workbook(loc2) 
topFifty = wb2.sheet_by_index(4)
topTwoFifty = wb2.sheet_by_index(5)
topFifteenHundred = wb2.sheet_by_index(6)

t50 = []
t250 = []
t1500Cities = {}
t1500Coords = {}

for i in range(1,51):
    t50.append(topFifty.cell_value(i,1))
    
t50 = 7 * t50[0:5] + 4 * t50[5:15] + 2 * t50[15:25] + t50[25:] #WEIGHTS


for i in range(0,449):
    if (topTwoFifty.cell_value(i,1), topTwoFifty.cell_value(i,2)) not in t250:
        t250.append((topTwoFifty.cell_value(i,1), topTwoFifty.cell_value(i,2)))
        
t250 = 5 * t250[0:25] + 3 * t250[25:50] + 2 * t250[50:100] + t250[100:] #WEIGHTS


for i in range(1,1501):
    city = topFifteenHundred.cell_value(i,4)
    HS = topFifteenHundred.cell_value(i,1)
    coords = (topFifteenHundred.cell_value(i,7),topFifteenHundred.cell_value(i,8))
    
    if city not in t1500Cities:
        t1500Cities[city] = [HS]
    else:
        t1500Cities[city].append(HS)
        
    if coords not in t1500Coords:
        t1500Coords[coords] = [HS]
    else:
        t1500Coords[coords].append(HS)

    
locations = {}
cityToCoords = {}
for i in range(1,19360):
    locations[sheet.cell_value(i,5)] = ((sheet.cell_value(i,1),sheet.cell_value(i,0)),((sheet.cell_value(i,6),(sheet.cell_value(i,7)))))
    cityToCoords[(sheet.cell_value(i,1) + ", " + sheet.cell_value(i,0))] = ((sheet.cell_value(i,1),sheet.cell_value(i,0)),((sheet.cell_value(i,6),(sheet.cell_value(i,7)))))


loc3 = ("recruits.xlsx")
wb3 = xlrd.open_workbook(loc3) 
recruits = wb3.sheet_by_index(0)

df = pd.DataFrame(columns=['#','Name','Hometown','High School'])
                           
for i in range(1,511):
    name = recruits.cell_value(i,1)
    location = recruits.cell_value(i,2)
    highschool = recruits.cell_value(i,3)
    #print("-----------------------")
    
    
    if location == "":
        location = generateLoc(locations,i,name)
    else:
        if location in cityToCoords:
            location = cityToCoords[location]
    if highschool == "" and i <= 251:
        highschool = generateHS(location, t50,t250,t1500Cities,t1500Coords,i,name, cityToCoords)
    if type(location) == tuple:
        location = location[0][0] + ", " + location[0][1]
    df.loc[i-1] = [i, name, location, highschool]

        
    
df.to_excel('generatedLocations.xlsx', encoding='utf-8', index=False)

