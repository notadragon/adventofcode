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

lineRe = re.compile("^([0-9]+),([0-9]+),([0-9]+)$")

data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    data.append( (int(m.group(1)), int(m.group(2)), int(m.group(3)), ) )

cubes = frozenset(data)

deltas = ( ( 1,  0,  0),
           (-1,  0,  0),
           ( 0,  1,  0),
           ( 0, -1,  0),
           ( 0,  0,  1),
           ( 0,  0, -1), )
           

if args.p1:
    print("Doing part 1")

    exposedsides = 0
    for c in cubes:
        for delta in deltas:
            adj = (c[0] + delta[0], c[1] + delta[1], c[2] + delta[2],)
            if not adj in cubes:
                exposedsides = exposedsides + 1
    print(f"Exposed Sides: {exposedsides}")

    
if args.p2:
    print("Doing part 2")

    minx = min(c[0] for c in cubes) -1
    maxx = max(c[0] for c in cubes) +1 
    miny = min(c[1] for c in cubes) -1
    maxy = max(c[1] for c in cubes) +1
    minz = min(c[2] for c in cubes) -1
    maxz = max(c[2] for c in cubes) +1

    print(f"Ranges: ({minx}-{maxx},{miny}-{maxy},{minz}-{maxz})")

    sides = set()
    for c in cubes:
        for delta in deltas:
            adj = (c[0] + delta[0], c[1] + delta[1], c[2] + delta[2],)
            if not adj in cubes:
                sides.add( (c,adj) )
    allsides = frozenset(sides)

    fillstart = (minx, miny, minz)
    tocheck = collections.deque([ fillstart ])
    visited = set([fillstart])

    insides = sides.copy()
    
    while tocheck:
        loc = tocheck.popleft()

        for delta in deltas:
            adj = (loc[0] + delta[0], loc[1] + delta[1], loc[2] + delta[2],)
            if adj[0] < minx or adj[0] > maxx:
                continue
            if adj[1] < miny or adj[1] > maxy:
                continue
            if adj[2] < minz or adj[2] > maxz:
                continue
            
            if adj in cubes:
                insides.remove( (adj,loc) )
            else:
                
                if not adj in visited:
                    visited.add(adj)
                    tocheck.append(adj)

    print(f"Sides: {len(sides)}")
    print(f"Insides: {len(insides)}")
    print(f"Outsides: {len(sides)-len(insides)}")
                
            
