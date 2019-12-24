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

lineRe = re.compile("[\.#]+")

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

for g in grid:
    print(g)

directions = {
    "^" : (0,-1),
    ">" : (1,0),
    "<" : (-1,0),
    "v" : (0,1),
}

def getcontents(grid,x,y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return "."
    else:
        return grid[y][x]

def step(grid):
    output = []
    w = len(grid[0])
    h = len(grid)

    for i in range(0,h):
        output.append([])
    for x,y in itertools.product(range(0,w),range(0,h)):
        adjacents = 0
        current = getcontents(grid,x,y)
        for heading in directions.values():
            hv = getcontents(grid, x + heading[0], y + heading[1])
            if hv == "#":
                adjacents = adjacents + 1
        if current == "#":
            if adjacents != 1:
                current = "."
        else:
            if adjacents == 1 or adjacents == 2:
                current = "#"
        output[y].append(current)

    return tuple([ "".join(g) for g in output ])

def biodiversity(gr):
    w = len(gr[0])
    h = len(gr)

    bd = 1
    total = 0
    n = 1
    for y in range(0,h):
        for x in range(0,w):
            current = getcontents(gr,x,y)
            if current == "#":
                total = total + bd
            n = n + 1
            bd *= 2
        
    return total

if args.p1:
    print("Doing part 1")

    startgrid = tuple(grid)

    past = set()

    gr = grid
    while True:
        gr = step(gr)

        if gr in past:
            print("DUPLICATE")
            break

        past.add(gr)

    for g in gr:
        print(g)

    print biodiversity(gr)

def countbugs(gr):
    output = 0
    for g in gr:
        for c in g:
            if c == "#":
                output = output + 1
    return output
    
def getrcontents(grid,x,y,z):
    if z < 0 or z >= len(grid) or y < 0 or y >= len(grid[z]) or x < 0 or x >= len(grid[z][y]):
        return "."
    else:
        return grid[z][y][x]

def radjacents(x,y,z):
    for heading in directions.values():
        yield (x + heading[0], y + heading[1], z)

    if x == 0:
        yield (1,2,z+1)
    if x == 4:
        yield (3,2,z+1)
    if y == 0:
        yield (2,1,z+1)
    if y == 4:
        yield (2,3,z+1)

    if x == 1 and y == 2:
        for i in range(0,5):
            yield (0, i, z-1)
    elif x == 2 and y == 1:
        for i in range(0,5):
            yield (i, 0, z-1)
    elif x == 3 and y == 2:
        for i in range(0,5):
            yield (4, i, z-1)
    elif x == 2 and y == 3:
        for i in range(0,5):
            yield (i, 4, z-1)
        
def rstep(grs):
    w = len(grs[0][0])
    h = len(grs[0])
    
    output = []
    for z in range(-1,len(grs)+1):
        zg = []

        for i in range(0,h):
            zg.append([])
        for y in range(0,h):
            for x in range(0,w):
                if x == 2 and y == 2:
                    zg[y].append(".")
                    continue
                adjacents = 0
                current = getrcontents(grs,x,y,z)

                for l in radjacents(x,y,z):
                    hv = getrcontents(grs, l[0], l[1], l[2])
                    if hv == "#":
                        #print( " %s : #" % (l,))
                        adjacents = adjacents + 1
                if current == "#":
                    if adjacents != 1:
                        current = "."
                else:
                    if adjacents == 1 or adjacents == 2:
                        current = "#"
                #print("%s adj:%s" % ( (x,y,z,), adjacents,) )
                zg[y].append(current)

        output.append(tuple(["".join(g) for g in zg]))

    while output and countbugs(output[0]) == 0:
        output = output[1:]
    while output and countbugs(output[-1]) == 0:
        output = output[:-1]
    return tuple(output)
        
if args.p2:
    print("Doing part 2")

    for g in grid:
        print(g)
    print("")
    
    grs = ( tuple(grid), )

    if args.input == "input":
        for i in range(0,200):
            grs = rstep(grs)
    else:
        for i in range(0,10):
            grs = rstep(grs)

    output = 0
    for gr in grs:
        for g in gr:
            output += sum([1 if c == "#" else 0 for c in g])

    #for gr in grs:
    #    print("")
    #    for g in gr:
    #        print(g)
    print("Bugs: %s" % (output,))
