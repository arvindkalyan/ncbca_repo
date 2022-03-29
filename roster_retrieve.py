# -*- coding: utf-8 -*-
import urllib.request
import json
import pandas as pd  
import statistics

#import dataframe_image as dfi

def getJSON_OBS(filePath):    
    with open(filePath, encoding='utf-8-sig') as fp:
        return json.load(fp)

def getJSON(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        return data

def writeJSON(filePath, obj):
    with open(filePath, 'r+',encoding='utf-8') as fp:
        json.dump(obj, fp, indent=4)

def getTIDs(obj):
    teamDict = {}
    for item in obj.get("teams"):
       teamDict[item.get("region")] = item.get("tid")
       teamDict[item.get("tid")] = item.get("region")
    teamDict["HS0"] = -2
    teamDict["HS1"] = -4
    teamDict["HS2"] = -5
    teamDict[-2] = "HS0"
    teamDict[-4] = "HS1"
    teamDict[-5] = "HS2"
    teamDict["Draft"] = -2
    return teamDict


def search(obj, team, teamDict):
    cols = ["#", "Name", "Injury", "Pos", "Yr", "Ovr", "GP", "Min", "Pts", "Reb", "Ast", "PER", "PT"]
    pt_dict = dict([(0, "--"), (0.75, "-"), (1, " "), (1.25, "+"), (1.75, "++")])
    roster_df = pd.DataFrame(columns = cols)
    
    i = 0
    for player in obj.get("players"):
        if player["tid"] == teamDict[team]:
            stats = player["stats"][-1]
            ratings = player["ratings"][-1]
            if stats["gp"] == 0:
                roster_df.loc[i] = (player['rosterOrder'], player["firstName"] + " " + player["lastName"], " ", ratings["pos"], player["year"], ratings["ovr"], 0, 0, 0,  0, 0, 0, pt_dict[player["ptModifier"]])
            else:
                if player["injury"]["gamesRemaining"] != 0:
                    roster_df.loc[i] = (player['rosterOrder'], player["firstName"] + " " + player["lastName"], player["injury"]["gamesRemaining"], ratings["pos"], player["year"], ratings["ovr"], stats["gp"], stats["min"]/stats["gp"], stats["pts"]/stats["gp"],  (stats["orb"]+stats["drb"])/stats["gp"], stats["ast"]/stats["gp"], stats["per"], pt_dict[player["ptModifier"]])
                else:
                    roster_df.loc[i] = (player['rosterOrder'], player["firstName"] + " " + player["lastName"], " ", ratings["pos"], player["year"], ratings["ovr"], stats["gp"], stats["min"]/stats["gp"], stats["pts"]/stats["gp"],  (stats["orb"]+stats["drb"])/stats["gp"], stats["ast"]/stats["gp"], stats["per"], pt_dict[player["ptModifier"]])
            i+=1
    roster_df.set_index("#", inplace = True)

    return (roster_df.sort_values(by=['#']).round(1))


def getGames(obj, team, teamDict):
    log = ""
    tid = teamDict[team]
    for game in obj["games"]:
        if game["won"]["tid"] != tid and game["lost"]["tid"] != tid:
            continue
        if game["won"]["tid"] == tid:
            if game["teams"][0]["tid"] == tid:
                log += "Game " + str(game["gid"]//50 + 1) + ": W, " +str(game["won"]["pts"]) + "-" + str(game["lost"]["pts"]) + " vs. " + teamDict[game["lost"]["tid"]] + " (" + getRecord(obj,game["lost"]["tid"]) +  ")"
            else:
                log += "Game " + str(game["gid"]//50+ 1) + ": W, " +str(game["won"]["pts"]) + "-" + str(game["lost"]["pts"]) + " @ " + teamDict[game["lost"]["tid"]]  + " (" + getRecord(obj,game["lost"]["tid"]) +  ")"
        else:
            if game["teams"][0]["tid"] == tid:
                log += "Game " + str(game["gid"]//50 + 1) + ": L, " +str(game["lost"]["pts"]) + "-" + str(game["won"]["pts"]) + " vs. " + teamDict[game["won"]["tid"]]+ " (" + getRecord(obj,game["won"]["tid"]) +  ")"
            else:
                log += "Game " + str(game["gid"]//50+ 1 ) + ": L, " + str(game["lost"]["pts"]) + "-" + str(game["won"]["pts"]) + " @ " + teamDict[game["won"]["tid"]] + " (" + getRecord(obj,game["won"]["tid"]) +  ")"
        if game["overtimes"] > 1:
            log += " (" + str(game["overtimes"]) + "OT)"
        if game["overtimes"] == 1:
            log += " (OT)"
        log += "\n"
    print(log)
    
            



#df = search(obj, "Miami (FL)", teamDict)

#print(df.to_string())
#rev_teamDict = {v: k for k, v in teamDict.items()}

#getGames(obj, "Oklahoma", teamDict)
def getRecord(current_export, team):
    rec = ""
    rec += str(current_export["teams"][team]["seasons"][-1]["won"])
    rec += "-"
    rec += str(current_export["teams"][team]["seasons"][-1]["lost"])
    return rec

def getSchedule(obj, team, teamDict):    
    log = ""
    tid = teamDict[team]
    for game in obj["schedule"]:
        if game['homeTid'] == tid:
            log += "Game " + str(game["gid"]//50+ 1) + ": v " + teamDict[game["awayTid"]] + " (" + getRecord(obj,game["awayTid"]) +  ")"
            log += '\n'
        elif game['awayTid'] == tid:
            log += "Game " + str(game["gid"]//50+ 1) + ": @ " + teamDict[game["homeTid"]] + " (" + getRecord(obj,game["homeTid"]) +  ")"
            log += '\n'
    print(log)

#getGames(obj, "Xavier", teamDict)
#getSchedule(obj, "Xavier", teamDict)
def someFunc():
    cols = ["name", "team", "gp", "min", "fg", "fgA", "fgAtRim", "fgAtRimA", "fgLowPost", "fgLowPostA", "fgMidRange", "fgMidRangeA", "tp", "tpa", "ft", "fta", "pm", "orb", "drb", "reb", "ast", "tov", "stl", "blk", "pf", "pts", "per", "ewa", "drtg", "ortg", "dws", "ows", "ws"]
    stats_df = pd.DataFrame(columns = cols)
    i = 0
    for player in obj["players"]:
        if len(player["stats"]) != 0:
            stats = player["stats"][-1]
            if player["tid"] >= 0:
                gp = stats["gp"]
                if gp != 0:
                    if stats["fgaAtRim"] == 0:
                        fgAtRim = 0
                    else:
                        fgAtRim = stats["fgAtRim"]/stats["fgaAtRim"]
                    if stats["fgaLowPost"] == 0:
                        fgLowPost = 0
                    else:
                        fgLowPost = stats["fgLowPost"]/stats["fgaLowPost"]
                    if stats["fgaMidRange"] == 0:
                        fgMidRange = 0
                    else:
                        fgMidRange = stats["fgMidRange"]/stats["fgaMidRange"]
                    if stats["fga"] == 0:
                        fg = 0
                    else:
                        fg = stats["fg"]/stats["fga"]
                    if stats["tpa"] == 0:
                        tp = 0
                    else:
                        tp = stats["tp"]/stats["tpa"]
                    if stats["fta"] == 0:
                        ft = 0
                    else:
                        ft = stats["ft"]/stats["fta"]
                        
                    stats_df.loc[i] = (player["firstName"] + " " + player["lastName"], teamDict[player["tid"]], stats["gp"], stats["min"]/gp, fg, stats["fga"]/gp, fgAtRim, stats["fgaAtRim"]/gp, fgLowPost, stats["fgaLowPost"]/gp, fgMidRange, stats["fgaMidRange"]/gp, tp, stats["tpa"]/gp, ft, stats["fta"]/gp, stats["pm"]/gp, stats["orb"]/gp, stats["drb"]/gp, (stats["orb"] + stats["drb"])/gp, stats["ast"]/gp, stats["tov"]/gp, stats["stl"]/gp, stats["blk"]/gp, stats["pf"]/gp, stats["pts"]/gp, stats["per"], stats["ewa"], stats["drtg"], stats["ortg"], stats["dws"], stats["ows"], stats["dws"] + stats["ows"])
                else:
                    stats_df.loc[i] = (player["firstName"] + " " + player["lastName"], teamDict[player["tid"]], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0,0,0)
                i+=1
        stats_df = stats_df.round(1)


       
def getLeaders(stats_df, stat, num):
    stats_df = stats_df.loc[stats_df["min"] > 7]
    if stat == "tp" or stat == "ft":
        stats_df = stats_df[stats_df[stat+"a"] > 1]
        leaders = stats_df[["name", "team", stat, stat+"a"]]
        leaders[stat] = leaders[stat].map('{:.3f}'.format)
    elif stat == "fg":
        stats_df = stats_df[stats_df["fgA"] > 3.6]
        leaders = stats_df[["name", "team", stat, stat+"A"]]
        leaders[stat] = leaders[stat].map('{:.3f}'.format)
    elif stat == "fgAtRim" or stat == "fgLowPost" or stat == "fgMidRange":
        stats_df = stats_df[stats_df["fgA"] > 2]
        leaders = stats_df[["name", "team", stat, stat+"A"]]
        leaders[stat] = leaders[stat].map('{:.3f}'.format)
    else:
        leaders = stats_df[["name", "team", stat]]
        
    return leaders.sort_values(by = stat, ascending = False).head(num)

#print(getLeaders(stats_df, "ft", 10).to_string(index=False))
    
def getProfile(obj, player_name, teamDict, year = None):
    profile = ""
    year_dict = dict([(19, "Fr."), (20, "So."), (21, "Jr."), (22, "Sr.")])
    stats_year = year
    i = 0
    cols = ["name", "ovr", "age", "grade", "tall", "weight", "pos", "year", "team", "ppg", "apg", "rpg", "spg", "bpg", "fgp", "tpp", "ftp", "ts", "fga", "tpa", "fta", "per", "ewa", "ortg", "drtg","hgt", "str", "spd", "jmp", "end", "ins", "dnk", "ft", "fg", "tp", "oiq", "diq", "drb", "pss", "reb", "badges", "location", "hs"]
    player_df = pd.DataFrame(columns = cols)

    for player in obj["players"]:
        name = player["firstName"] + " " + player["lastName"]
        if name.lower() == player_name.lower():
            if year == None:
                stats_year = player["ratings"][-1]["season"]
            buffer = []
            for i in range(0, len(player["ratings"]) - len(player["stats"])):
                buffer += [None]
            for stats, ratings in zip(buffer + player["stats"], player["ratings"]):
                if ratings["season"] == stats_year:
                    age = ratings["season"] - player["born"]["year"]
                    if age < 19:
                        grade = "HS"
                    elif age > 22:
                        grade = "LS"
                    else:
                        grade = year_dict[age]
                    badges = ""
                    for badge in ratings["skills"]:
                        badges += badge + " "
                    if stats == None:
                        gp = 0
                        team = "HS/JUCO"
                    else:
                        gp = stats["gp"]
                        team = teamDict[stats["tid"]]
                    if gp != 0:
                        if stats["fga"] == 0:
                            fg = 0
                        else:
                            fg = stats["fg"]/stats["fga"]
                        if stats["tpa"] == 0:
                            tp = 0
                        else:
                            tp = stats["tp"]/stats["tpa"]
                        if stats["fta"] == 0:
                            ft = 0
                        else:
                            ft = stats["ft"]/stats["fta"]

                        player_df.loc[i] = (player["firstName"] + " " + player["lastName"], ratings["ovr"],age, grade, player["hgt"], player["weight"], ratings["pos"], stats_year, team, round(stats["pts"]/gp,1), round(stats["ast"]/gp,1), round((stats["orb"]+stats["drb"])/gp,1), round(stats["stl"]/gp,1), round(stats["blk"]/gp,1), round(100*fg,1) ,round(100*tp,1), round(100*ft,1), round(100*stats["pts"]/(2 * (stats["fga"] + 0.44 * stats["fta"])),1), round(stats["fga"]/gp,1), round(stats["tpa"]/gp,1), round(stats["fta"]/gp,1), round(stats["per"],1), round(stats["ewa"],1), round(stats["ortg"],1), round(stats["drtg"],1), ratings["hgt"], ratings["stre"], ratings["spd"], ratings["jmp"], ratings["endu"], ratings["ins"], ratings["dnk"], ratings["ft"], ratings["fg"], ratings["tp"], ratings["oiq"], ratings["diq"], ratings["drb"], ratings["pss"], ratings["reb"], badges, player["city"] + ", " + player["state"], player["college"])
                    else:
                        player_df.loc[i] = (player["firstName"] + " " + player["lastName"], ratings["ovr"], age, grade, player["hgt"], player["weight"], ratings["pos"], stats_year, team, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0,0, 0, 0, 0, 0, ratings["hgt"], ratings["stre"], ratings["spd"], ratings["jmp"], ratings["endu"], ratings["ins"], ratings["dnk"], ratings["ft"], ratings["fg"], ratings["tp"], ratings["oiq"], ratings["diq"], ratings["drb"], ratings["pss"], ratings["reb"], badges, player["city"] + ", " + player["state"], player["college"])
                    i += 1
    if player_df.shape[0] == 0 and year == None:
        profile = "Who? No player found!"
    if player_df.shape[0] == 0 and year != None:
        profile = "No player found that year!"
    if player_df.shape[0] > 1 and year == None:
        profile = "Multiple players found. Specify a year."
    if player_df.shape[0] > 1 and year != None:
        profile  = "Multiple players found in same year."

    if profile == "":
        player_df = player_df.to_dict('r')[0]
        profile = "```\n{} | {} OVR | {} | {} | {}\n{} | {}\n \n{} STATS:\n{} PPG | {} APG | {} RPG | {} SPG | {} BPG\n{} FG% | {} 3P% | {} FT% | {} TS%\n{} FGA | {} 3PA | {} FTA\n{} PER | {} EWA | {} ORTG | {} DRTG\n \n{} RATINGS: \n{} OVR | {}'{}\" | {} LB | {}\nPHYSICAL: {} HGT | {} STR | {} SPD | {} JMP | {} ENDU\nSHOOTING: {} INS | {} DNK | {} FT | {} FG | {} 3P\nSKILL: {} OIQ | {} DIQ | {} DRB | {} PSS | {} REB\n```".format(player_df["name"], player_df["ovr"], player_df["grade"], player_df["pos"], player_df["team"], player_df["location"], player_df["hs"], player_df["year"], player_df["ppg"], player_df["apg"], player_df["rpg"], player_df["spg"], player_df["bpg"], player_df["fgp"], player_df["tpp"], player_df["ftp"], player_df["ts"],player_df["fga"], player_df["tpa"], player_df["fta"], player_df["per"], player_df["ewa"], player_df["ortg"], player_df["drtg"], player_df["year"], player_df["ovr"], player_df["tall"]//12, player_df["tall"]%12, player_df["weight"], player_df["badges"], player_df["hgt"], player_df["str"], player_df["spd"], player_df["jmp"], player_df["end"], player_df["ins"], player_df["dnk"], player_df["ft"], player_df["fg"], player_df["tp"], player_df["oiq"], player_df["diq"], player_df["drb"], player_df["pss"], player_df["reb"])

    return player_df, profile

def createMessage(player_df, year):
    if player_df.shape[0] == 0 and year == None:
        profile = "Who? No player found!"
    if player_df.shape[0] == 0 and year != None:
        profile = "No player found that year!"
    if player_df.shape[0] > 1 and year == None:
        profile = "Multiple players found. Specify a year."
    if player_df.shape[0] > 1 and year != None:
        profile  = "Multiple players found in same year."
    if profile == "":
        player_df = player_df.to_dict('r')[0]
        profile = "```\n{} | {} OVR | {} | {} | {}\n{} | {}\n \n{} STATS:\n{} PPG | {} APG | {} RPG | {} SPG | {} BPG\n{} FG% | {} 3P% | {} FT% | {} TS%\n{} FGA | {} 3PA | {} FTA\n{} PER | {} EWA | {} ORTG | {} DRTG\n \n{} RATINGS: \n{} OVR | {}'{}\" | {} LB | {}\nPHYSICAL: {} HGT | {} STR | {} SPD | {} JMP | {} ENDU\nSHOOTING: {} INS | {} DNK | {} FT | {} FG | {} 3P\nSKILL: {} OIQ | {} DIQ | {} DRB | {} PSS | {} REB\n```".format(player_df["name"], player_df["ovr"], player_df["age"], player_df["pos"], player_df["team"], player_df["location"], player_df["hs"], player_df["year"], player_df["ppg"], player_df["apg"], player_df["rpg"], player_df["spg"], player_df["bpg"], player_df["fgp"], player_df["tpp"], player_df["ftp"], player_df["ts"],player_df["fga"], player_df["tpa"], player_df["fta"], player_df["per"], player_df["ewa"], player_df["ortg"], player_df["drtg"], player_df["year"], player_df["ovr"], player_df["tall"]//12, player_df["tall"]%12, player["weight"], player_df["badges"], player_df["hgt"], player_df["str"], player_df["spd"], player_df["jmp"], player_df["end"], player_df["ins"], player_df["dnk"], player_df["ft"], player_df["fg"], player_df["tp"], player_df["oiq"], player_df["diq"], player_df["drb"], player_df["pss"], player_df["reb"])
    return profile
    
import random     

def bound(low, high, value):
    if value < low:
        return low
    if value > high: 
        return high
    return value

shootingFormula = (0, (-3, 13))

def iqFormula(age):
    if age <= 21:
        base = 4
    else:
        base = 3
    return (base, (-3, 7 + 5 * (24 - age)))

def ratingFormula(rtg, age):
    val, lim = 0, (-99,99)
    if rtg == 'spd' or rtg == 'jmp':
        val = 0
        lim = (-12, 2)
    if rtg == 'end':
        val = random.uniform(0, 9)
        lim = (-11, 19)
    if rtg == 'dnk' or rtg == 'ins' or rtg == 'ft' or rtg == 'fg' or rtg == 'tp':
        val, lim = shootingFormula
    if rtg == 'oiq' or rtg == 'diq':
        val, lim = iqFormula(age)
    if rtg == 'drb' or rtg == 'pss' or rtg == 'reb':
        val, lim = iqFormula(age)
        lim = (-2, 5)
    return val, lim

def calcBaseChange(age):
    if age <= 19:
        val = 7
    elif age <= 20:
        val = 5
    elif age <= 21:
        val = 3
    else:
        val = 1   
    if age <= 23:
        val += bound(-4, 20, random.gauss(0,5))
    elif age <= 25:
        val += bound(-4, 10, random.gauss(0,5))
    else:
        val += bound(-2, 4, random.gauss(0,3))
    return val
        
def getOvr(value):
    if value >= 68.:
        return round(value+8.)
    elif value >= 50.:
        return round(value+ (4. + ((value - 50.) * (4. / 18.))))
    elif value >= 42.:
        return round(value+ (-5. + (value -42.) * (10. / 8.)))
    elif value >= 31.:
        return round(value+ (-5. - (42.-value) * (5. / 11.) ))
    else:
        return round(value -10.)
    

def progress(player_df):
    oldOvr = getOvr(((5 *player_df['hgt'] + 1 *player_df['str'] + 4 *player_df['spd'] + 2 *player_df['jmp'] + 1 *player_df['end'] + 1 *player_df['ins'] + 2 *player_df['dnk'] + 1 *player_df['ft'] + 1 *player_df['fg'] + 3 *player_df['tp'] + 7 *player_df['oiq'] + 3 *player_df['diq'] + 3 *player_df['drb'] + 3 *player_df['pss'] + 1 * player_df['reb']) / 38.))
    age = player_df["age"]
    baseChange = calcBaseChange(age)
    rtgs = ['hgt', 'str', 'spd', 'jmp', 'end', 'dnk', 'ins', 'ft', 'fg', 'tp', 'oiq', 'diq', 'drb', 'pss', 'reb']
    new_ratings = {}
    for rtg in rtgs:
        #print(rtg)
        old_rtg = player_df[rtg]
        new_ratings[rtg] = old_rtg
        if rtg == 'hgt':
            hgtRand = random.random()
            if hgtRand > 0.99 and age <= 20:
                new_ratings[rtg] += 1
            if hgtRand > 0.999:
                new_ratings[rtg] += 1
        else:
            ageModifier, limits = ratingFormula(rtg, age)
            new_ratings[rtg] = int(bound(0, 100, old_rtg + bound(limits[0], limits[1], (baseChange + ageModifier) * random.uniform(0.4, 1.4))))
        #print((old_rtg, new_ratings[rtg], new_ratings[rtg] - old_rtg))
    newOvr = getOvr(((5 *new_ratings['hgt'] + 1 *new_ratings['str'] + 4 *new_ratings['spd'] + 2 *new_ratings['jmp'] + 1 *new_ratings['end'] + 1 *new_ratings['ins'] + 2 *new_ratings['dnk'] + 1 *new_ratings['ft'] + 1 *new_ratings['fg'] + 3 *new_ratings['tp'] + 7 *new_ratings['oiq'] + 3 *new_ratings['diq'] + 3 *new_ratings['drb'] + 3 *new_ratings['pss'] + 1 * new_ratings['reb']) / 38.))        
    new_ratings['age'] = age+1
    new_ratings['ovr'] = newOvr
    new_ratings['oldovr'] = oldOvr
    #print((oldOvr, newOvr, newOvr-oldOvr))
    return new_ratings
    

def avgProg(obj, teamDict, team, names = []):
    tid = teamDict[team]
    i = 0
    cols = ["name", "ovr", "oldovr", "age", "pos","hgt", "str", "spd", "jmp", "end", "ins", "dnk", "ft", "fg", "tp", "oiq", "diq", "drb", "pss", "reb"]
    player_df = pd.DataFrame(columns = cols)
    prog_cols = ["name", "ovr", "ovr_med", "ovr_std", "ovr_max", "oldovr", "age", "pos","hgt", "str", "spd", "jmp", "end", "ins", "dnk", "ft", "fg", "tp", "oiq", "diq", "drb", "pss", "reb"]
    progs_df = pd.DataFrame(columns = prog_cols)
    for player in obj["players"]:
        name = player["firstName"] + " " + player["lastName"]
        if name.lower() in names or player["tid"] == tid:
            ratings = player["ratings"][-1]
            age = ratings["season"] - player["born"]["year"]
            player_df.loc[i] = (player["firstName"] + " " + player["lastName"], ratings["ovr"],ratings["ovr"], age, ratings["pos"], ratings["hgt"], ratings["stre"], ratings["spd"], ratings["jmp"], ratings["endu"], ratings["ins"], ratings["dnk"], ratings["ft"], ratings["fg"], ratings["tp"], ratings["oiq"], ratings["diq"], ratings["drb"], ratings["pss"], ratings["reb"])
            i+=1
    
    for i in list(player_df.index):
        progs = dict((rtg,[]) for rtg in cols[5:])
        progs["name"] = player_df.iloc[i]["name"]
        progs["ovr"] = []
        progs["age"] = []
        progs["pos"] = player_df.iloc[i]["pos"]
        
        progs_df.loc[i, "name"] = player_df.iloc[i]["name"]
        progs_df.loc[i, "pos"] = player_df.iloc[i]["pos"]
        progs_df.loc[i, "oldovr"] = player_df.iloc[i]["oldovr"]
        progs_df = progs_df.sort_values(by=['oldovr'], ascending = False)
        iterations = 100
        for it in range(iterations):
            p = progress(player_df.iloc[i])
            for key, value in p.items():
                if key != "name" and key != "pos" and key != "oldovr":
                    progs[key].append(value)
        for key, value in progs.items():
                if key != "name" and key != "pos" and key != "oldovr":
                    progs[key] = statistics.mean(value)
                    progs_df.loc[i, key] = statistics.mean(value)
                if key == "ovr":
                    progs_df.loc[i, "ovr_std"] = statistics.stdev(value)
                    progs_df.loc[i, "ovr_med"] = statistics.median(value)
                    progs_df.loc[i, "ovr_max"] = max(value)
            
    return progs_df.reset_index(drop=True)

    
                

       
fileName = 'BBGM_BGMDL_2110_draft.json'
obj = getJSON_OBS(fileName)
teamDict = getTIDs(obj) 
    
p = avgProg(obj, teamDict, "Draft")

p.to_excel('DRAFT_2110.xlsx', encoding='utf-8', index=True)

#progress(getProfile(obj, "george hooper", teamDict)[0])






