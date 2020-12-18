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
    grid.append(x)


if args.p1:
    def getDeltas():
        for t in itertools.product( range(-1,2), range(-1,2), range(-1,2) ):
            if t[0] != 0 or t[1] != 0 or t[2] != 0:
                yield t
    
    def getAdj(t):
        for d in getDeltas():
            yield ( d[0] + t[0], d[1] + t[1], d[2] + t[2])
    
    def printGrid(grid):
        corners = None
        for a in grid:
            if not corners:
                corners = [ a, a ]
            else:
                corners[0] = tuple( min(corners[0][i], a[i]) for i in range(0,3) )
                corners[1] = tuple( max(corners[1][i], a[i]) for i in range(0,3) )
    
        for z in range(corners[0][2], corners[1][2]+1):
            print("z=%s" % (z,))
            for y in range(corners[0][1], corners[1][1]+1):
                outrow = []
                for x in range(corners[0][0], corners[1][0]+1):
                    if (x,y,z) in grid:
                        outrow.append("#")
                    else:
                        outrow.append(".")
                print("".join(outrow))
            print("")
    
    def step(active):
    
        if not active:
            return active
    
        corners = None
        for a in active:
            if not corners:
                corners = [ a, a ]
            else:
                corners[0] = tuple( min(corners[0][i], a[i]) for i in range(0,3) )
                corners[1] = tuple( max(corners[1][i], a[i]) for i in range(0,3) )
    
        newactive = set()
        for x in range(corners[0][0] - 1, corners[1][0]+2):
            for y in range(corners[0][1] - 1, corners[1][1]+2):
                for z in range(corners[0][2] - 1, corners[1][2]+2):
                    numNeighbors = len( [ t for t in getAdj( (x,y,z) ) if t in active ] )
                    
                    #print("%s: %s" % ( (x,y,z), numNeighbors, ) )
    
                    if (x,y,z) in active:
                        if numNeighbors == 2 or numNeighbors == 3:
                            newactive.add( (x,y,z) )
                    else:
                        if numNeighbors == 3:
                            newactive.add( (x,y,z) )
    
        #printGrid(newactive)
    
        return newactive
    
    print("Doing part 1")

    active = set()
    for y in range(0,len(grid)):
        for x in range(0,len(grid[y])):
            if grid[y][x] == "#":
                active.add( (x,y,0) )

    print("Step: %s  active: %s" % (0,len(active)) )
    for i in range(0,6):
        active = step(active)
        print("Step: %s  active: %s" % (i+1,len(active)) )
        
if args.p2:
    def getDeltas():
        for t in itertools.product( range(-1,2), range(-1,2), range(-1,2), range(-1,2) ):
            if t[0] != 0 or t[1] != 0 or t[2] != 0 or t[3] != 0:
                yield t
    
    def getAdj(t):
        for d in getDeltas():
            yield ( d[0] + t[0], d[1] + t[1], d[2] + t[2], d[3] + t[3])
    
    def printGrid(grid):
        corners = None
        for a in grid:
            if not corners:
                corners = [ a, a ]
            else:
                corners[0] = tuple( min(corners[0][i], a[i]) for i in range(0,4) )
                corners[1] = tuple( max(corners[1][i], a[i]) for i in range(0,4) )
    
        for z in range(corners[0][2], corners[1][2]+1):
            for w in range(corners[0][3], corners[1][3]+1):
                print("z=%s, w=%s" % (z,w,))
                for y in range(corners[0][1], corners[1][1]+1):
                    outrow = []
                    for x in range(corners[0][0], corners[1][0]+1):
                        if (x,y,z) in grid:
                            outrow.append("#")
                        else:
                            outrow.append(".")
                    print("".join(outrow))
                print("")
    
    def step(active):
    
        if not active:
            return active
    
        corners = None
        for a in active:
            if not corners:
                corners = [ a, a ]
            else:
                corners[0] = tuple( min(corners[0][i], a[i]) for i in range(0,4) )
                corners[1] = tuple( max(corners[1][i], a[i]) for i in range(0,4) )
    
        newactive = set()
        for x in range(corners[0][0] - 1, corners[1][0]+2):
            for y in range(corners[0][1] - 1, corners[1][1]+2):
                for z in range(corners[0][2] - 1, corners[1][2]+2):
                    for w in range(corners[0][3] - 1, corners[1][3]+2):
                    
                        numNeighbors = len( [ t for t in getAdj( (x,y,z,w) ) if t in active ] )
                    
                        #print("%s: %s" % ( (x,y,z,w), numNeighbors, ) )
    
                        if (x,y,z,w) in active:
                            if numNeighbors == 2 or numNeighbors == 3:
                                newactive.add( (x,y,z,w) )
                        else:
                            if numNeighbors == 3:
                                newactive.add( (x,y,z,w) )
    
        #printGrid(newactive)
    
        return newactive
    

    print("Doing part 2")

    active = set()
    for y in range(0,len(grid)):
        for x in range(0,len(grid[y])):
            if grid[y][x] == "#":
                active.add( (x,y,0,0) )

    print("Step: %s  active: %s" % (0,len(active)) )
    for i in range(0,6):
        active = step(active)
        print("Step: %s  active: %s" % (i+1,len(active)) )
