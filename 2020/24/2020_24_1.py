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

lineRe = re.compile("(w|nw|sw|ne|se|e)+")
dirRe = re.compile("(w|nw|sw|ne|se|e)")
paths = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    paths.append( dirRe.findall(x) )

#for path in paths:
#    print("Path: %s" % (path,))

dirs = { "w" : (-2, 0),
         "nw" : (-1, -2),
         "ne" : (1, -2), 
         "e" : (2, 0),
         "se" : (1, 2),
         "sw" : (-1, 2) }

def pathEnd(loc, path):
    for p in path:
        d = dirs[p]
        loc = (loc[0] + d[0], loc[1] + d[1])
    return loc

if True:
    blackTiles = set()
    for p in paths:
        endpoint = pathEnd( (0,0), p)
        if endpoint in blackTiles:
            blackTiles.remove(endpoint)
        else:
            blackTiles.add(endpoint)

if args.p1:
    print("Doing part 1")

    print("Final Black Tiles: %s" % (len(blackTiles),))

def adjacencies(loc):
    for ddelta in dirs.values():
        yield (loc[0] + ddelta[0], loc[1] + ddelta[1],)
    
def stepTiles(tiles):
    adjTiles = {}

    for t in tiles:
        for adj in adjacencies(t):
            if adj in adjTiles:
                adjTiles[adj] = adjTiles[adj] + 1
            else:
                adjTiles[adj] = 1

    newtiles = set()
    for t,count in adjTiles.items():
        if t in tiles:
            if count > 0 and count <= 2:
                newtiles.add(t)
        else:
            if count == 2:
                newtiles.add(t)

    return newtiles
                
    
if args.p2:
    print("Doing part 2")

    currentTiles = blackTiles
    for i in range(0,100):
        currentTiles = stepTiles(currentTiles)
        print("Day %s: %s" % (i+1,len(currentTiles),))
