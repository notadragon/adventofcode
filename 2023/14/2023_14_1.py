#!/usr/bin/env python3

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

lineRe = re.compile("^[\.O#]+$")

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
    
grid = tuple(grid)
    
#for r in grid:
#    print(r)

deltas = {
    "n" : (0, -1),
    "e" : (1, 0),
    "w" : (-1, 0),
    "s" : (0, 1)
    }

class Grid:
    def __init__(self, m):
        self.minx = 0
        self.maxx = max( len(r)-1 for r in m )
        self.miny = 0
        self.maxy = len(m)-1

        self.grid = {
            (x,y) : m[y][x] for y in range(0,len(m)) for x in range(0,len(m[y]))
        }

    def show(self):
        for y in range(self.miny, self.maxy+1):
            l = []
            for x in range(self.minx, self.maxx+1):
                l.append(self.grid[ (x,y) ])
            print("".join(l))

    def tilt(self, movedir):
        moved = False
        newgrid = {}

        for y in range(self.miny, self.maxy+1):
            for x in range(self.minx, self.maxx+1):
                v = self.grid[ (x,y) ]
                if v == "#":
                    newgrid[ (x,y) ] = "#"

        delta = deltas[movedir]
        if movedir == "n" or movedir == "w":
            for y in range(self.miny, self.maxy+1):
                for x in range(self.minx, self.maxx+1):
                    v = self.grid[ (x,y) ]
                    if v == "O":
                        toloc = ( x + delta[0], y + delta[1] )
                        if toloc in self.grid and toloc not in newgrid:
                            newgrid[ toloc ] = "O"
                            moved = True
                        else:
                            newgrid[ (x,y) ] = "O"
        elif movedir == "s" or movedir == "e":
            for y in range(self.maxy, self.miny-1, -1):
                for x in range(self.maxx, self.minx - 1, -1):
                    v = self.grid[ (x,y) ]
                    if v == "O":
                        toloc = ( x + delta[0], y + delta[1] )
                        if toloc in self.grid and toloc not in newgrid:
                            newgrid[ toloc ] = "O"
                            moved = True
                        else:
                            newgrid[ (x,y) ] = "O"
                            

        for y in range(self.miny, self.maxy+1):
            for x in range(self.minx, self.maxx+1):
                if (x,y) not in newgrid:
                    newgrid[ (x,y) ] = "."
            
        self.grid = newgrid
        return moved

    def load(self):
        total = 0
        for loc, v in self.grid.items():
            if v == "O":
                load = self.maxy - loc[1] + 1
                total = total + load
        return total

    def torocks(self):
        output = []
        for y in range(self.miny, self.maxy+1):
            for x in range(self.minx, self.maxx+1):
                if self.grid[ (x,y) ] == "O":
                    output.append( (x,y) )
        return tuple(output)

    def togrid(self):
        output = []
        for y in range(self.miny, self.maxy+1):
            l = []
            for x in range(self.minx, self.maxx+1):
                l.append(self.grid[ (x,y) ])
            output.append(tuple(l))
        return tuple(output)
    
if args.p1:
    print("Doing part 1")

    g = Grid(grid)
    g.show()

    
    while g.tilt("n"):
        pass

    print("")
    g.show()

    print(f"Load: {g.load()}")

if args.p2:
    print("Doing part 2")

    def cycle(grid):
        while g.tilt("n"):
            pass
        while g.tilt("w"):
            pass
        while g.tilt("s"):
            pass
        while g.tilt("e"):
            pass

    g = Grid(grid)
    g.show()

    rocklocs = { g.togrid() : 0 }
    repeats = None
    step = 0
    while True:
        cycle(g)
        step = step + 1
        
        r = g.togrid()

        if r in rocklocs:
            repeats = (rocklocs[ r ], step )
            break
        else:
            rocklocs[r] = step

    print(f"Repeat Cycles: {repeats}")

    cyclelen = repeats[1] - repeats[0]
    
    mod = (1000000000 - repeats[0]) % cyclelen
    c = repeats[0] + mod

    print(f"  1000000000 % {cyclelen} == {mod}")
    
    for gr,s in rocklocs.items():
        if s == c:
            lastgrid = gr
            break

    gr = Grid(gr);
    gr.show()
    print(f"Final Load: {gr.load()}")
            
    
