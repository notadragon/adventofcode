#!/usr/bin/env pypy3

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("Player (\d+) starting position: (\d+)")
players = {}

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    players[int(m.group(1))] = int(m.group(2))

print(f"Players: {players}")

def deterministicDie():
    while True:
        for i in range(1,101):
            yield i

def steppos(pos, roll):
    pos = pos + roll
    pos = ((pos - 1) % 10) + 1
    return pos

def runGame(playerMap, dice):
    players = [ [ pid, pos, 0] for pid,pos in playerMap.items() ]
    players.sort()

    print(f"Players: {players}")

    numrolls = 0
    done = False
    while not done:

        for pdata in players:
            rolls = (next(dice), next(dice), next(dice),)
            numrolls = numrolls + 3
            pos = steppos(pdata[1],sum(rolls))
            pdata[1] = pos
            pdata[2] = pdata[2] + pos

            if pdata[2] >= 1000:
                #print(f"Player {pdata[0]} rolls {rolls[0]}+{rolls[1]}+{rolls[2]} and moves to space {pdata[1]} for a final score of {pdata[2]}")
                done = True
                break
            else:
                #print(f"Player {pdata[0]} rolls {rolls[0]}+{rolls[1]}+{rolls[2]} and moves to space {pdata[1]} for a total score of {pdata[2]}")
                pass

    print(f"Rolls: {numrolls}")

    loserScore = min(pdata[2] for pdata in players)
    print(f"Loser: {loserScore}")
    print(f"GameVal: {numrolls * loserScore}")
    

if args.p1:
    print("Doing part 1")

    runGame(players, deterministicDie())

diracCache = {}

def genDiracCounts():
    output = {}
    for r1 in range(1,4):
        for r2 in range(1,4):
            for r3 in range(1,4):
                total = r1+r2+r3
                output[total] = output.get(total,0) + 1
    return output

diracCounts = genDiracCounts()

def diracResults( gamestate ):
    if gamestate in diracCache:
        return diracCache[gamestate]
    
    turn, p1pos, p2pos, p1score, p2score  = gamestate

    tpos = gamestate[1+turn]
    tscore = gamestate[3+turn]

    output = [0, 0]
    
    for roll,count in diracCounts.items():
        pos = steppos(tpos, roll)
        score = tscore + pos

        if score >= 21:
            output[turn] = output[turn] + count
            continue

        if turn == 0:
            nextturn = ( 1, pos, p2pos, score, p2score )
        else:
            nextturn = ( 0, p1pos, pos, p1score, score )

        nextResults = diracResults(nextturn)

        output[0] = output[0] + count * nextResults[0]
        output[1] = output[1] + count * nextResults[1]
                

    diracCache[gamestate] = output
    return output
    

def diracGame(playerMap):
    players = [ [ pid, pos, 0] for pid,pos in playerMap.items() ]
    players.sort()

    firststate = ( 0, playerMap[1], playerMap[2], 0, 0)

    results = diracResults(firststate)

    print(f"Dirac Results: {results}")
    if results[0] > results[1]:
        print(f"Player 1 wins more: {results[0]}")
    elif results[1] > results[0]:
        print(f"Player 2 wins more: {results[2]}")
    else:
        print(f"TIE! : {results[0]}")
        
    

    
    
if args.p2:
    print("Doing part 2")

    diracGame(players)
