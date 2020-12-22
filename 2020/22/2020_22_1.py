#!/usr/bin/env pypy

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

lineRe = re.compile("(?:Player (\d+))|(\d+)")
players = {}
currentPlayer = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        pid = int(m.group(1))
        currentPlayer = []
        players[pid] = currentPlayer
    else:
        currentPlayer.append(int(m.group(2)))

def combat(pdata, v):
    plays = []
    for i in range(0,2):
        if v: print("Player %s's deck: %s" % (i+1,", ".join([str(x) for x in pdata[i]]),))

        idata = pdata[i]
        p = idata[0]
        del idata[0]
        plays.append(p)

    for i in range(0,2):
        if v: print("Player %s plays: %s" % (i+1,plays[i],))

    if plays[0] > plays[1]:
        winner = 0
    else:
        winner = 1

    if v: print("Player %s wins the round!" % (winner+1,))
    pdata[winner].extend( (plays[winner], plays[1-winner],) )

    return winner

def score(idata, v):
    total = 0
    for m in range(len(idata),0,-1):
        ndx = len(idata) - m
        if v:
            print("%s %2s * %2s" % ("+" if m < len(idata) else " ",idata[ndx],m,))
        total = total + (idata[ndx] * m)
    if v:
        print("= %s" % (total,))
    return total
    
for pid,data in players.items():
    print("%s -> %s" % (pid,data,))

if args.p1:
    print("Doing part 1")

    v = False
    pdata = [ players[1][:], players[2][:], ]
    rnum = 0
    cache = set()
    while pdata[0] and pdata[1]:
        cached = (tuple(pdata[0]),tuple(pdata[1]))
        if cached in cache:
            print("Recursion!")
            break
        cache.add(cached)
        rnum = rnum + 1
        if v:
            print("")
            print("Round %s" % (rnum,))
        winner = combat(pdata,v)

    s = score(pdata[winner], v)
    print("Final Score: %s" % (s,))

def rcombat(pdata, rnum, mygnum, nextgnum, v):
    if v:
        print("")
        print("-- Round %s (Game %s) --" % (rnum,mygnum,))
    plays = []
    for i in range(0,2):
        if v: print("Player %s's deck: %s" % (i+1,", ".join([str(x) for x in pdata[i]]),))

        idata = pdata[i]
        p = idata[0]
        del idata[0]
        plays.append(p)

    for i in range(0,2):
        if v: print("Player %s plays: %s" % (i+1,plays[i],))

    if plays[0] <= len(pdata[0]) and plays[1] <= len(pdata[1]):
        rpdata = []
        for i in range(0,2):
            rpdata.append( pdata[i][:plays[i]] )

        if v:
            print("Playing a sub-game to determine the winner...")
            print("")

        subgnum = nextgnum
        winner,nextgnum = rcombatgame(rpdata, subgnum, v)

        if v:
            print("")
            print("...anyway, back to game %s." % (mygnum,))
    else:
        if plays[0] > plays[1]:
            winner = 0
        else:
            winner = 1

    if v: print("Player %s wins round %s of game %s!" % (winner+1,rnum,mygnum,))
    pdata[winner].extend( (plays[winner], plays[1-winner],) )

    return winner, nextgnum

def rcombatgame(pdata, gnum, v):
    if v:
        print("=== Game %s ===" % (gnum,))

    cache = set()
    if pdata[0]:
        winner = 0
    else:
        winner = 1

    nextgnum = gnum + 1
    rnum = 0
    while pdata[0] and pdata[1]:
        cached = (tuple(pdata[0]),tuple(pdata[1]))
        if cached in cache:
            return (0,gnum)
        cache.add(cached)

        rnum = rnum + 1
        winner,nextgnum = rcombat(pdata,rnum,gnum,nextgnum,v)

    if v: print("The winner of game %s is player %s!" % (gnum,winner+1,))
        
    return (winner,nextgnum)
    
if args.p2:
    print("Doing part 2")

    v = False
    pdata = [ players[1][:], players[2][:], ]
    rnum = 0
    while pdata[0] and pdata[1]:
        rnum = rnum + 1
        if v:
            print("")
            print("Round %s" % (rnum,))
        winner,gnum = rcombatgame(pdata,1,v)

    s = score(pdata[winner], v)
    print("Final Score: %s" % (s,))
