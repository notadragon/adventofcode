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

lineRe = re.compile(".*")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(tuple([ int(c) for c in x]))

data = tuple(data)

print(f"Data: {data}")

def adj(grid,loc):
    for delta in ( (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), ):
        ty = loc[1]+delta[1]
        if ty < 0 or ty >= len(grid):
            continue
        tx = loc[0]+delta[0]
        if tx < 0 or tx >= len(grid[ty]):
            continue
        yield (tx,ty)

def locs(grid):
    for y in range(0,len(grid)):
        for x in range(0,len(grid[y])):
            yield (x,y)

def gat(grid,loc):
    return grid[loc[1]][loc[0]]

def gset(grid,loc,c):
    grid[loc[1]][loc[0]] = c
    return c

def step(grid):
    grid = list([ list([ o for o in r]) for r in grid])

    flashed = set()
    toflash = []

    for loc in locs(grid):
        newc = gset(grid,loc,gat(grid,loc)+1)
        if newc > 9:
            toflash.append(loc)

    while toflash:
        loc = toflash.pop()
        if loc in flashed:
            continue
        flashed.add(loc)
        for aloc in adj(grid,loc):
            newc = gset(grid,aloc,gat(grid,aloc)+1)
            if newc > 9:
                toflash.append(aloc)

    for loc in flashed:
        gset(grid,loc,0)
                
    return (grid,len(flashed))
    
if args.p1:
    print("Doing part 1")

    g = data
    flashes = 0
    for i in range(0,100):
        g,sflashes = step(g)
        flashes = flashes + sflashes

        #print(f"Steps: {i+1}")
        #print(f"Grid:")
        #for r in g:
        #    print("".join([str(c) for c in r]))
        #print(f"Flashes: {flashes}")
        #print("")

    for r in g:
        print("".join([str(c) for c in r]))
        
    print(f"Total flashes: {flashes}")
    
if args.p2:
    print("Doing part 2")

    g = data
    total = sum([len(r) for r in g])
    i = 0
    while True:
        g,sflashes = step(g)
        i = i + 1

        if sflashes == total:
            print(f"All flashed after step {i}")
            break
