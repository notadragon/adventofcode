#!/usr/bin/env pypy

import argparse, re, itertools

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lineRe = re.compile("([0-9]+), ([0-9]+)")

pairs = []
ids = [ chr(i) for i in range(ord('a'),ord('z')+1) + range(ord('A'),ord('Z')+1) ]

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    pairs.append( (int(m.group(1)), int(m.group(2)), ) )

minx = min([x[0] for x in pairs])
miny = min([x[1] for x in pairs])
maxx = max([x[0] for x in pairs])
maxy = max([x[1] for x in pairs])

#print("Pairs (%s): %s" % (len(pairs),pairs,))
print("Ranges: %s-%s x %s-%s" % (minx,maxx,miny,maxy,))

def generateSquare( center, radius ):
    for d in range(0, radius*2+1):
        yield ( center[0] + radius, center[1] - radius + d,)
    for d in range(1, radius*2+1):
        yield ( center[0] + radius - d, center[1] + radius,)
    for d in range(1, radius*2+1):
        yield ( center[0] - radius, center[1] + radius - d,)
    for d in range(1, radius*2):
        yield ( center[0] - radius + d, center[1] - radius,)

def generateDiamond( center, radius ):
    for d in range(0,radius+1):
        yield( center[0] + radius - d, center[1] + d ,)
    for d in range(1,radius+1):
        yield( center[0] - d, center[1] + radius - d ,)
    for d in range(1,radius+1):
        yield( center[0] - radius + d, center[1] - d ,)
    for d in range(1,radius):
        yield( center[0] + d, center[1] - radius + d ,)
        
if args.p1:
    print("Doing part 1")

    ps = { pid : loc for pid,loc in zip(ids,pairs) }
    print("Ps:%s" % (ps,))

    grid = [ [ ["?",-1] for x in range(minx-1,maxx+2) ] for y in range(miny-1,maxy+2) ]
    for i in itertools.count():
        added = 0

        for pid,loc in ps.items():

            for d in generateDiamond( loc, i):
                if not(d[0] >= minx-1 and d[0] <= maxx+1 and d[1] >= miny-1 and d[1] <= maxy+1):
                    continue
                griddata = grid[d[1]-miny+1][d[0]-minx+1]
                if griddata[0] == "?":
                    griddata[0]  = pid
                    griddata[1] = i
                    added += 1
                elif griddata[1] == i:
                    griddata[0] = "."
                    
        if added == 0:
            break

    #for g in grid:
    #    print("".join( [l[0] for l in g] ))

    totals = { x:0 for x in ps.keys() }

    for g in grid:
        for x in g:
            if x[0] != ".":
                totals[x[0]] += 1
    for x in grid[0] + grid[-1] + [ g[0] for g in grid ] + [ g[-1] for g in grid ]:
        if x[0] != ".":
            totals[x[0]] = -1
    print("Totals: %s" % (totals,))

    print("Largest Area: %s" % ( max(totals.values()),))
            
if args.p2:
    print("Doing part 2")

    ydists = { y : sum( [ abs( p[1] - y ) for p in pairs ] ) for y in range(miny-1,maxy+2) }
    xdists = { x : sum( [ abs( p[0] - x ) for p in pairs ] ) for x in range(minx-1,maxx+2) }

    while xdists[minx-1] < 10000:
        xdists[minx-2] = xdists[minx-1] + len(pairs)
        minx -= 1
    while xdists[maxx+1] < 10000:
        xdists[maxx+2] = xdists[maxx+1] + len(pairs)
        maxx += 1
    while ydists[miny-1] < 10000:
        ydists[miny-2] = ydists[miny-1] + len(pairs)
        miny -= 1
    while ydists[maxy+1] < 10000:
        ydists[maxy+2] = ydists[maxy+1] + len(pairs)
        maxy += 1
    print("NewRanges: %s-%s x %s-%s" % (minx,maxx,miny,maxy,))

    total = sum( [ 1 for (x,y) in itertools.product( range(minx-1,maxx+2), range(miny-1,maxy+2) ) if xdists[x] + ydists[y] < 10000 ] )
    print("Total: %s" % (total,))
