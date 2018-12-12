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
    grid.append(x)

def ison(grid,loc):
    if loc[1] < 0 or loc[1] >= len(grid):
        return False
    row = grid[loc[1]]
    if loc[0] < 0 or loc[0] >= len(row):
        return False
    return row[loc[0]] == "#"

def neighbors(x,y):
    yield (x-1,y)
    yield (x-1,y-1)
    yield (x,y-1)
    yield (x+1,y-1)
    yield (x+1,y)
    yield (x+1,y+1)
    yield (x,y+1)
    yield (x-1,y+1)
    
def step(grid):
    output = []

    for y in range(0,len(grid)):
        row = grid[y]
        newrow = []
        for x in range(0,len(row)):
            numneighbors = sum([1 for n in neighbors(x,y) if ison(grid,n) ])
            if ison(grid, (x,y) ):
                newrow.append("#" if numneighbors == 2 or numneighbors == 3 else ".")
            else:
                newrow.append("#" if numneighbors == 3 else ".")
        output.append("".join(newrow))
    
    return output
    
#for g in grid:
#    print(g)

#g = grid
#for i in range(0,4):
#    g = step(g)
#    for x in g:
#        print(x)
#    print("")
    
if args.p1:
    print("Doing part 1")

    g = grid
    for i in range(0,100):
        g = step(g)

    total = 0
    for r in g:
        print(r)
    print("Still on: %s" % ( sum( [ sum([ 1 for c in r if c == "#" ]) for r in g ] ), ) )
    
if args.p2:
    print("Doing part 2")

    def stick(g):
        g[0] = "#" + g[0][1:-1] + "#"
        g[-1] = "#" + g[-1][1:-1] + "#"
        return g
    
    g = stick(grid)
    for i in range(0,100):
        g = stick(step(g))

    total = 0
    for r in g:
        print(r)
    print("Still on: %s" % ( sum( [ sum([ 1 for c in r if c == "#" ]) for r in g ] ), ) )
    
