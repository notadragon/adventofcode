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

lineRe = re.compile("^[0-9]+,[0-9]+( -> [0-9]+,[0-9]+)*$")
coordRe = re.compile("([0-9]+),([0-9]+)")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    newpath = []
    for c in x.split(" -> "):
        m2 = coordRe.match(c)
        if not m2:
            print(f"No match for coordinates: {c}")
            continue
        newpath.append( (int(m2.group(1)), int(m2.group(2)), ) )
    data.append(tuple(newpath))

#for d in data:
#    print(f"{d}")

    

def printgrid(grid):
    minx = min(g[0] for g in grid.keys())
    miny = min(g[1] for g in grid.keys())
    maxx = max(g[0] for g in grid.keys())
    maxy = max(g[1] for g in grid.keys())

    numlines = []
    for x in range(minx,maxx+1):
        if x == minx or x == maxx or (x % 10 == 0):
            xs = f"{x}"
            while len(numlines) < len(xs):
                numlines.append([" " * 4])
            for n,c in enumerate(xs):
                numlines[n].append(c)
            for n in range(len(xs),len(numlines)):
                numlines[n].append(" ")
        else:
            for l in numlines:
                l.append(" ")
        
    for l in numlines:
        print("".join(l))
    
    for y in range(miny,maxy+1):
        line = [f"{y:3} "]
        for x in range(minx,maxx+1):
            if (x,y) in grid:
                line.append(grid[ (x,y) ])
            else:
                line.append(".")
        print("".join(line))

sanddeltas = [ (0,1), (-1,1), (1,1) ]
        
def addSand(start, grid, maxy):
    loc = start
    while True:
        nextloc = None
        for sanddelta in sanddeltas:
            candidate = (loc[0] + sanddelta[0], loc[1] + sanddelta[1])
            if candidate in grid:
                continue
            nextloc = candidate
            break
        if nextloc == None:
            grid[loc] = "o"
            return loc
        if nextloc[1] > maxy:
            return None
        loc = nextloc

def makegrid(data):
    grid = {}

    for path in data:
        loc = path[0]
        for nextloc in path[1:]:
            delta = (nextloc[0] - loc[0], nextloc[1] - loc[1])
            if delta[0] != 0:
                delta = ( delta[0] // abs(delta[0]), delta[1] )
            if delta[1] != 0:
                delta = ( delta[0], delta[1] // abs(delta[1]) )

            #print(f"{loc} -> {nextloc} - {delta}")
            grid[loc] = "#"
            while loc != nextloc:
                loc = (loc[0] + delta[0], loc[1] + delta[1])
                grid[loc] = "#"
                
            loc = nextloc

    return grid

if args.p1:
    print("Doing part 1")

    grid = makegrid(data)
    sandorigin = (500,1)
    grid[ sandorigin ] = "*"

    maxy = max(g[1] for g in grid.keys())
    total = 0
    while True:
        sandloc = addSand( sandorigin, grid, maxy )
        if sandloc == None :
            break
        total = total + 1
        if sandloc == sandorigin:
            break
        #printgrid(grid)

    print(f"Total Sand: {total}")
            
if args.p2:
    print("Doing part 2")

    grid = makegrid(data)
    sandorigin = (500,0)
    grid[ sandorigin ] = "*"
    
    maxy = max(g[1] for g in grid.keys())
    floorheight = maxy+2
    maxy = floorheight

    for x in range(500 - floorheight - 1, 500 + floorheight + 1 + 1):
        grid[ (x,floorheight) ] = "#"
    
    total = 0
    if False:
        while True:
            sandloc = addSand( sandorigin, grid, maxy )
            if sandloc == None:
                break
            total = total + 1
            if sandloc == sandorigin:
                break
    else:
        minx = min(g[0] for g in grid.keys())
        maxx = max(g[0] for g in grid.keys())

        grid[sandorigin] = "o"
        total = total + 1

        for y in range(sandorigin[1], maxy+1):
            for x in range(minx,maxx+1):
                loc = (x,y)
                if loc in grid:
                    continue
                issand = False
                for sanddelta in sanddeltas:
                    sourceloc = (loc[0] - sanddelta[0], loc[1] - sanddelta[1])
                    if sourceloc in grid and grid[sourceloc] == "o":
                        issand = True
                        break
                if issand:
                    total = total + 1
                    grid[loc] = "o"
        
    printgrid(grid)

    print(f"Total Sand: {total}")
