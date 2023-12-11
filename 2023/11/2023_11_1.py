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

lineRe = re.compile("^[\.#]+$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

galaxies = {}
for y in range(0,len(data)):
    for x in range(0,len(data[y])):
        v = data[y][x]
        if v == "#":
            galaxies[ (x,y) ] = v

#print(f"Galaxies: {galaxies}")


if args.p1:
    print("Doing part 1")

    minx = min( l[0] for l in galaxies.keys() )
    maxx = max( l[0] for l in galaxies.keys() )
    miny = min( l[1] for l in galaxies.keys() )
    maxy = max( l[1] for l in galaxies.keys() )

    galaxycolumns = list( set( l[0] for l in galaxies ) )
    galaxycolumns.sort()
    galaxyrows = list( set( l[1] for l in galaxies ) )
    galaxycolumns.sort()

    expandedcolumns = (maxx - minx + 1) - len(galaxycolumns)
    expandedrows = (maxy - miny + 1) - len(galaxyrows)

    def adjust( loc ):
        c = len( tuple( x for x in galaxycolumns if x < loc[0] ) )
        r = len( tuple(y for y in galaxyrows if y < loc[1] ) )

        return loc[0] * 2 - c, loc[1] * 2 - r

    adjustedgalaxies = { loc : adjust(loc)  for loc in galaxies.keys() }

    poses = list(galaxies.keys())
    total = 0
    for i in range(0,len(poses)-1):
        for j in range(i+1, len(poses)):
            l1 = poses[i]
            l2 = poses[j]

            l1adj = adjustedgalaxies[l1]
            l2adj = adjustedgalaxies[l2]

            dist = abs( l1adj[0] - l2adj[0]) + abs(l1adj[1] - l2adj[1] )

            #print(f"{l1} -> {l2} ({l1adj} -> {l2adj}) : {dist}")
            total = total + dist

    
    print(f"Total: {total}")
    
    
if args.p2:
    print("Doing part 2")

    minx = min( l[0] for l in galaxies.keys() )
    maxx = max( l[0] for l in galaxies.keys() )
    miny = min( l[1] for l in galaxies.keys() )
    maxy = max( l[1] for l in galaxies.keys() )

    galaxycolumns = list( set( l[0] for l in galaxies ) )
    galaxycolumns.sort()
    galaxyrows = list( set( l[1] for l in galaxies ) )
    galaxycolumns.sort()

    expandedcolumns = (maxx - minx + 1) - len(galaxycolumns)
    expandedrows = (maxy - miny + 1) - len(galaxyrows)

    m = 1000000
    def adjust( loc ):
        c = len( tuple( x for x in galaxycolumns if x < loc[0] ) )
        r = len( tuple(y for y in galaxyrows if y < loc[1] ) )

        return loc[0] * m - (m-1) * c, loc[1] * m - (m-1) * r

    adjustedgalaxies = { loc : adjust(loc)  for loc in galaxies.keys() }

    poses = list(galaxies.keys())
    total = 0
    for i in range(0,len(poses)-1):
        for j in range(i+1, len(poses)):
            l1 = poses[i]
            l2 = poses[j]

            l1adj = adjustedgalaxies[l1]
            l2adj = adjustedgalaxies[l2]

            dist = abs( l1adj[0] - l2adj[0]) + abs(l1adj[1] - l2adj[1] )

            #print(f"{l1} -> {l2} ({l1adj} -> {l2adj}) : {dist}")
            total = total + dist

    
    print(f"Total: {total}")
