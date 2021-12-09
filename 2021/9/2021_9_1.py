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

data = []
lineRe = re.compile("\d+")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append([int(c) for c in x])

def adj(hmap, loc):
    for delta in ( (0,1), (0, -1), (-1, 0), (1,0), ) :
        dloc = ( loc[0] + delta[0], loc[1] + delta[1] )
        if dloc[1] < 0 or dloc[1] >= len(hmap):
            continue
        hrow = hmap[dloc[1]]
        if dloc[0] < 0 or dloc[0] >= len(hrow):
            continue
        c = hrow[dloc[0]]
        yield ( dloc, c)


if args.p1:
    print("Doing part 1")

    hmap = data
    totalRisk = 0
    for y in range(0,len(hmap)):
        hrow = hmap[y]
        for x in range(0,len(hrow)):
            loc = (x, y)
            
            c = hrow[x]

            low = True
            for dloc, dval in adj(hmap,loc):
                if dval <= c:
                    low = False

            if low:
                print(f"LOW: {loc} : {c}")

                risk = 1 + c

                totalRisk = totalRisk + risk

    print(f"Total Risk: {totalRisk}")

def basin(hmap, loc):
    visitted = set()
    tovisit = collections.deque()
    tovisit.append(loc)

    while tovisit:
        vloc = tovisit.popleft()
        if vloc in visitted:
            continue
        visitted.add(vloc)

        c = hmap[vloc[1]][vloc[0]]
        if c == 9:
            continue

        yield vloc

        for aloc,ac in adj(hmap,vloc):
            if aloc in visitted:
                continue
            tovisit.append(aloc)
    
if args.p2:
    print("Doing part 2")

    hmap = data
    basins = {}
    locbasins = {}
    for y in range(0,len(hmap)):
        hrow = hmap[y]
        for x in range(0,len(hrow)):
            loc = (x, y)
            
            c = hrow[x]

            if c == 9:
                continue

            if loc in locbasins:
                continue

            lbasin = list(basin(hmap,loc))

            if lbasin:
                basins[loc] = lbasin
                for l in lbasin:
                    locbasins[l] = lbasin

    if False:
      for floc,basin in basins.items():
        print(f"{basin} : {len(basin)}")

        for y in range(0,len(hmap)):
            hrow = hmap[y]
            drow = []
            for x in range(0,len(hrow)):
                l = (x,y)
                if l in basin:
                    drow.append(str(hrow[x]))
                else:
                    drow.append(" ")

            print("".join(drow))

    basinsizes = [ len(b) for b in basins.values() ]
    basinsizes.sort()

    print(f"BasinSizes: {basinsizes}")

    print(f"Result: {basinsizes[-3]} * {basinsizes[-2]} * {basinsizes[-1]} = {basinsizes[-3]*basinsizes[-2]*basinsizes[-1]}")
