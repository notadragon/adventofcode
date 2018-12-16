#!/usr/bin/env pypy

import argparse, re

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

lineRe = re.compile(".*")
grid = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(list(x))

def show(state):
    grid,units = state
    for y in range(0,len(grid)):
        print("%s %s" % ("".join(grid[y]), "".join([ "%s(%s)" % (u[2],u[4],) for u in units if u[0] == y ]), ))

dirs = ( (0,0), (-1,0), (0,-1), (0,1), (1,0), )

def enemy(u):
    if u[2] == "E":
        return "G"
    else:
        return "E"

def step(state):
    grid,units = state

    nummoves = 0
    numattacks = 0
    
    locations = {}
    for u in units:
        locations[ (u[0],u[1]) ] = u

    completed = True

    killedone = True
    
    for u in units:
        if (u[0],u[1]) not in locations:
            continue
        else:
            u = locations[ (u[0],u[1],) ]
        
        distance = 0

        # y, x, startdir
        distancelocs = [ (u[0], u[1], 0) ]
        
        foundlocs = set( [ (u[0],u[1]) ] )

        e = enemy(u)

        if killedone:
            if sum([1 for other in locations.values() if other[2] == e]) == 0:
                completed = False
                break
        
        movedir = None
        while True:
            for p in distancelocs:
                for di in range(1,len(dirs)):
                    d = dirs[di]
                    if grid[p[0]+d[0]][p[1]+d[1]] == e:
                        # minimal distance, reading order first path
                        movedir = p[2]
                        break
                if movedir != None:
                    break
            if movedir != None:
                break
            
            newdistancelocs = []
            for p in distancelocs:
                for di in range(1,len(dirs)):
                    d = dirs[di]
                    newloc = (p[0]+d[0],p[1]+d[1])
                    if newloc in foundlocs:
                        continue
                    if grid[newloc[0]][newloc[1]] != ".":
                        continue
                    if p[2] == 0:
                        newp = (newloc[0],newloc[1],di)
                    else:
                        newp = (newloc[0],newloc[1],p[2])
                    newdistancelocs.append(newp)

            if not newdistancelocs:
                movedir = 0
                break

            distancelocs = []
            for p in newdistancelocs:
                pl = p[0:2]
                if pl in foundlocs:
                    continue
                else:
                    foundlocs.add(pl)
                    distancelocs.append(p)
            
            distance = distance + 1
            distancelocs.sort()

        if movedir != 0:
            movedelta = dirs[movedir]

            grid[u[0]][u[1]] = "."
            del locations[(u[0],u[1])]

            u = [u[0]+movedelta[0],u[1]+movedelta[1],] + u[2:]
            grid[u[0]][u[1]] = u[2]
            locations[(u[0],u[1])] = u

            nummoves += 1

        attackloc = None
        targethp = None
        for di in range(1,len(dirs)):
            d = dirs[di]
            td = (u[0]+d[0],u[1]+d[1],)
            if grid[td[0]][td[1]] == e:
                tdhp = locations[td][4]
                if targethp == None or targethp > tdhp:
                    targethp = tdhp
                    attackloc = td
        if attackloc:
            numattacks += 1
            tu = locations[attackloc]
            #print( "%s attacks %s (distance: %s)" % (u,tu,(tu[0]-u[0],tu[1]-u[1],)))
            tu[4] -= u[3]
            if tu[4] <= 0:
                #KILL!
                killedone = True
                del locations[attackloc]
                grid[attackloc[0]][attackloc[1]] = "."
            
    units = list(locations.values())
    units.sort()

    return ((grid,units),nummoves+numattacks,completed,)

def outcome(s):
    completed = 0
    while s:
        nexts,numactions,rounddone = step(s)
        s = nexts
        if rounddone:
            completed = completed + 1
        else:
            break
    totalhp = sum([u[4] for u in s[1]])
    return s,completed,totalhp

if args.p1:
    print("Doing part 1")

    g = []
    
    units = []
    for y in range(0,len(grid)):
        row =grid[y]
        r = []
        for x in range(0,len(row)):
            c = row[x]
            if c == "E" or c == "G":
                units.append( [y,x,c,3,200] )
            r.append(c)
        g.append(r)

    s = (g,units)
    show(s)
    s,completed,totalhp = outcome(s)
    print ("After %s rounds" % (completed,))
    show(s)
    print("Complete Rounds: %s" % (completed,))
    totalhp = sum([u[4] for u in s[1]])
    print("Total hp: %s" % (totalhp,))
    print("Outcome: %s" % ((completed)*totalhp,))
    
            
if args.p2:
    print("Doing part 2")

    elfattack = 1
    while True:
        g = []

        numelves = 0
        
        units = []
        for y in range(0,len(grid)):
            row =grid[y]
            r = []
            for x in range(0,len(row)):
                c = row[x]
                if c == "E":
                    units.append( [y,x,c,elfattack,200] )
                    numelves = numelves+1
                elif c == "G":
                    units.append( [y,x,c,3,200] )
                r.append(c)
            g.append(r)
                
        s = (g,units)
        s,completed,totalhp = outcome(s)

        if len(s[1]) == numelves and s[1][0][2] == "E":
            print("No deaths with attack power: %s" % (elfattack,))

            show(s)
            print("Combat ends after %s full rounds" % (completed,))
            print("Total hp: %s" % (totalhp,))
            print("Outcome: %s" % ((completed)*totalhp,))

            break
        else:
            elfattack = elfattack+1
