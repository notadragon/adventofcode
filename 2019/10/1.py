#!/usr/bin/env python3

import argparse, re, itertools, collections, math, functools

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

lineRe = re.compile("[#\.]*")

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

for x in grid:
    print(x)

cols = len(grid[0])
rows = len(grid)

def visible(grid,a,b):
    dist = ( b[0] - a[0], b[1] - a[1])

    if dist[0] == 0:
        delta = (0,1 if dist[1] > 0 else -1)
        steps = abs(dist[1])
    elif dist[1] == 0:
        delta = (1 if dist[0] > 0 else -1,0)
        steps = abs(dist[0])
    else:
        steps = math.gcd(abs(dist[0]), abs(dist[1]))
        delta = ( dist[0]//steps, dist[1]//steps, )

    #print("%s -> %s (%s * %s(" % (a,b,steps,delta,))
    for i in range(1,steps):
        c = (a[0] + i*delta[0], a[1] + i*delta[1])
        #print("  c: %s" % (c,))
        if grid[c[1]][c[0]] == "#":
            return False
        
    return True
    
if True:
    numvisible = [ [ 0 for x in range(0,cols) ] for y in range(0,rows) ]

    maxvisible = -1
    maxloc = None
    
    for x,y in itertools.product( range(0,cols), range(0,rows) ):
        #print( "x,y: %s" % ( (x,y,), ) )

        if grid[y][x] == ".":
            numvisible[y][x] = "  "
            continue

        for x2,y2 in itertools.product( range(0,cols), range(0,rows) ):
            if (x2 != x or y2 != y) and grid[y2][x2] == "#" and visible(grid, (x,y), (x2,y2) ):
                numvisible[y][x] = numvisible[y][x] + 1

        if numvisible[y][x] > maxvisible:
            maxloc = (x,y)
            maxvisible = numvisible[y][x]

if args.p1:
    print("Doing part 1")

    print("MaxLoc:%s maxVisible:%s" % (maxloc, maxvisible,))        

if args.p2:
    print("Doing part 2")

    sitelines = {}
    
    for x,y in itertools.product( range(0,cols), range(0,rows) ):
        if (x == maxloc[0] and y == maxloc[1]) or grid[y][x] != "#":
            continue
        dist = ( x - maxloc[0], y - maxloc[1] )

        if dist[0] == 0:
            delta = (0,1 if dist[1] > 0 else -1)
            steps = abs(dist[1])
        elif dist[1] == 0:
            delta = (1 if dist[0] > 0 else -1,0)
            steps = abs(dist[0])
        else:
            steps = math.gcd(abs(dist[0]), abs(dist[1]))
            delta = ( dist[0]//steps, dist[1]//steps, )

        if delta not in sitelines:
            sitelines[delta] = []
        sitelines[delta].append( (steps, (x,y,) ) )

    for sl in sitelines.values():
        sl.sort()

    dirs = []
    startangle = (0,-1)
    for delta in sitelines.keys():
        angle = math.atan2( delta[0], -delta[1])
        if angle < 0:
            angle = angle + 2*math.pi
        dirs.append(( angle , delta, sitelines[delta], ) )

    def quadrant(d):
        if d[0] == 0:
            if d[1] < 0:
                return 0
            else:
                return 8
        elif d[1] == 0:
            if d[0] < 0:
                return 12
            else:
                return 4
        elif d[0] < 0 and d[1] < 0:
            if d[0] == d[1]:
                return 14
            elif abs(d[0]) > abs(d[1]):
                return 13
            else:
                return 15
        elif d[0] < 0 and d[1] > 0:
            if d[0] == d[1]:
                return 10
            elif abs(d[0]) > abs(d[1]):
                return 11
            else:
                return 9
        elif d[0] > 0 and d[1] < 0:
            if d[0] == d[1]:
                return 2
            elif abs(d[0]) > abs(d[1]):
                return 3
            else:
                return 1
        elif d[0] > 0 and d[1] > 0:
            if d[0] == d[1]:
                return 6
            elif abs(d[0]) > abs(d[1]):
                return 5
            else:
                return 7

    def cross(a, b):
        return (a[1]*b[2] - a[2]*b[1],
                a[2]*b[0] - a[0]*b[2],
                a[0]*b[1] - a[1]*b[0])
            
    def deltacomp(d1,d2):
        delta1 = d1[1]
        delta2 = d2[1]

        q1 = quadrant(delta1)
        q2 = quadrant(delta2)

        cproduct = cross( delta1 + (0,), delta2 + (0,) )
        
        if q1 < q2:
            return -1
        elif q1 > q2:
            return 1

        if cproduct[-1] < 0:
            return 1
        elif cproduct[-1] > 0:
            return -1
        else:
            return 0
        
    dirs.sort( key = functools.cmp_to_key(deltacomp)  )

    rotations = max( len(sl) for sl in sitelines.values() )

    deaths = []
    for r in range(0,rotations):
        for d in dirs:
            angle, delta, sl = d
            if len(sl) > r:
                deaths.append( (sl[r][1],) + d)
    
    for n,d in enumerate(deaths):
        print("%s: %s (%s)"  % (n+1,d,(d[0][0] * 100 + d[0][1]),))
        

            
