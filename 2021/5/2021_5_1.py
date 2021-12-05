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

lineRe = re.compile("(\d+),(\d+) -> (\d+),(\d+).*")
paths = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    paths.append( ( (int(m.group(1)),int(m.group(2))), (int(m.group(3)),int(m.group(4))), ) )

#for p in paths:
#    print(f"{p}")

if args.p1:
    print("Doing part 1")

    covered = {}
    maprange = ( (0,0), (0,0) )
    
    for p in paths:
        if p[0][0] != p[1][0] and p[0][1] != p[1][1]:
            continue

        #print(f"Line: {p}")

        minx = min(p[0][0], p[1][0])
        miny = min(p[0][1], p[1][1])
        maxx = max(p[0][0], p[1][0])
        maxy = max(p[0][1], p[1][1])

        maprange = ( ( min(maprange[0][0], minx), min(maprange[0][1],miny)),
                     ( max(maprange[1][0], maxx), max(maprange[1][1],maxy)), )
                     
        
        for x in range(minx,maxx+1):
            for y in range(miny,maxy+1):
                loc = (x,y)
                if loc in covered:
                    covered[loc] = covered[loc] + 1
                else:
                    covered[loc] = 1

    #print(f"MapRange: {maprange}")
    #for y in range(maprange[0][1], maprange[1][1]+1):
    #    row = []
    #    for x in range(maprange[0][0], maprange[1][0]+1):
    #        loc = (x,y)
    #        if loc in covered:
    #            row.append(f"{covered[loc]}")
    #        else:
    #            row.append(".")
    #    print("".join(row))

    overlaps = len([ loc for loc,count in covered.items() if count > 1])
    print(f"Overlaps: {overlaps}")
                
if args.p2:
    print("Doing part 2")

    covered = {}
    maprange = ( (0,0), (0,0) )
    
    for p in paths:

        delta = ( p[1][0] - p[0][0], p[1][1] - p[0][1],)

        deltasize = abs(delta[0])
        if deltasize == 0:
            deltasize = abs(delta[1])
        if deltasize != 0:
            delta = (delta[0] / deltasize, delta[1] / deltasize)
        
        maprange = ( ( min(maprange[0][0], p[0][0], p[1][0]), min(maprange[0][1],p[0][1],p[1][1])),
                     ( max(maprange[0][0], p[0][0], p[1][0]), max(maprange[0][1],p[0][1],p[1][1])), )

        #print(f"Line: {p}  Delta: {delta}")

        loc = p[0]
        for i in range(0,deltasize+1):
            if loc in covered:
                covered[loc] = covered[loc] + 1
            else:
                covered[loc] = 1
            loc = ( loc[0] + delta[0], loc[1] + delta[1],)
                
            
    #print(f"MapRange: {maprange}")
    #for y in range(maprange[0][1], maprange[1][1]+1):
    #    row = []
    #    for x in range(maprange[0][0], maprange[1][0]+1):
    #        loc = (x,y)
    #        if loc in covered:
    #            row.append(f"{covered[loc]}")
    #        else:
    #            row.append(".")
    #    print("".join(row))

    overlaps = len([ loc for loc,count in covered.items() if count > 1])
    print(f"Overlaps: {overlaps}")
