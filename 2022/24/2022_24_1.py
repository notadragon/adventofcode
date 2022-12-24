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

lineRe = re.compile("^[\.<>v^#]+$")
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

deltas = { "" : (0,0),
           "^" : (0,-1),
           ">" : (1,0),
           "v" : (0,1),
           "<" : (-1,0),
           }
    
class Basin:
    def __init__(self, grid):
        self.minx = 0
        self.maxx = max(len(g)-1 for g in grid)
        self.miny = 0
        self.maxy = len(grid)-1

        # half-open range of positions for blizzards
        self.hrange = (self.minx+1, self.maxx)
        self.vrange = (self.miny+1, self.maxy)

        # row -> minute 0 column
        self.rblizzards = {}
        self.lblizzards = {}

        # column -> minute 0 row
        self.ublizzards = {}
        self.dblizzards = {}

        self.endpoints = [ None, None ]

        def addblizzard(bmap, index, startpos):
            if index in bmap:
                bmap[index] = bmap[index].union([startpos])
            else:
                bmap[index] = frozenset((startpos,))
                
        for y in range(0,len(grid)):
            for x in range(0,len(grid[y])):
                c = grid[y][x]
                if c == "#":
                    pass
                elif c == "^":
                    addblizzard(self.ublizzards, x, y)
                elif c == "v":
                    addblizzard(self.dblizzards, x, y)
                elif c == ">":
                    addblizzard(self.rblizzards, y, x)
                elif c == "<":
                    addblizzard(self.lblizzards, y, x)
                elif y == 0:
                    self.endpoints[0] = (x,y)
                elif y == len(grid)-1:
                    self.endpoints[1] = (x,y)


    def getblizzards( self, loc, minute ):
        def hasblizzard(bmap, mdir, r, index, pos):
            if not index in bmap:
                return False
            m0pos = pos - (mdir * minute)
            m0pos = (( m0pos - r[0]) % (r[1]-r[0])) + r[0]
            return m0pos in bmap[index]
            
        blizzards = []
        if loc[0] >= self.hrange[0] and loc[0] < self.hrange[1]:
            if hasblizzard(self.ublizzards, -1, self.vrange, loc[0], loc[1]):
                blizzards.append("^")
            if hasblizzard(self.dblizzards, 1, self.vrange, loc[0], loc[1]):
                blizzards.append("v")
        if loc[1] >= self.vrange[0] and loc[1] < self.vrange[1]:
            if hasblizzard(self.rblizzards, 1, self.hrange, loc[1], loc[0]):
                blizzards.append(">")
            if hasblizzard(self.lblizzards, -1, self.hrange, loc[1], loc[0]):
                blizzards.append("<")
        return blizzards

    def isedge(self, loc):
        return loc[0] == self.minx or loc[0] == self.maxx or loc[1] == self.miny or loc[1] == self.maxy
    
    def iswall(self, loc):
        return self.isedge(loc) and not loc in self.endpoints

    def isinside(self, loc):
        if loc[0] < self.minx or loc[0] > self.maxx or loc[1] < self.miny or loc[1] > self.maxy:
            return False
        return not self.iswall(loc)
    

    def showMinute(self, minute):
        for y in range(self.miny, self.maxy+1):
            line = []
            
            for x in range(self.minx, self.maxx+1):
                if self.iswall( (x,y) ):
                    line.append("#")
                elif (x,y) in self.endpoints:
                    line.append(".")
                else:
                    bzs = self.getblizzards( (x,y), minute)
                    if 0 == len(bzs):
                        line.append(".")
                    elif 1 == len(bzs):
                        line.append(bzs[0])
                    else:
                        line.append(f"{len(bzs)}")
            print("".join(line))
                    

    def shortestpath(self, start, end, startminute = 0):
        minute = startminute
        mlocs = set( (start,) )

        while not end in mlocs:
            newmlocs = set()

            for loc in mlocs:
                for delta in deltas.values():
                    tloc = (loc[0] + delta[0], loc[1] + delta[1])
                    if not self.isinside(tloc):
                        continue
                    if tloc in newmlocs:
                        continue
                    if self.getblizzards(tloc, minute+1):
                        continue
                    newmlocs.add(tloc)
                    
            mlocs = newmlocs
            minute = minute + 1

            #print(f"Minute: {minute} Locs: {len(mlocs)}")

        return minute
        
basin = Basin(grid)
            
print(f"Endpoints: {basin.endpoints}")

#for i in range(0,10):
#    print(f"Minute: {i}")
#    basin.showMinute(i)

if args.p1:
    print("Doing part 1")

    shortesttime = basin.shortestpath( basin.endpoints[0], basin.endpoints[1])
    print(f"Shortest path {basin.endpoints[0]} -> {basin.endpoints[1]}: {shortesttime}")
    
if args.p2:
    print("Doing part 2")

    shortesttime = basin.shortestpath( basin.endpoints[0], basin.endpoints[1], 0)
    print(f"Shortest path {basin.endpoints[0]} -> {basin.endpoints[1]}: {shortesttime}")
    
    shortesttime = basin.shortestpath( basin.endpoints[1], basin.endpoints[0], shortesttime)
    print(f"Shortest path {basin.endpoints[1]} -> {basin.endpoints[0]}: {shortesttime}")

    shortesttime = basin.shortestpath( basin.endpoints[0], basin.endpoints[1], shortesttime)
    print(f"Shortest path {basin.endpoints[0]} -> {basin.endpoints[1]}: {shortesttime}")
