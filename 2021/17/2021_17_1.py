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

lineRe = re.compile("target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")

areas = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    areas.append( ( (int(m.group(1)), int(m.group(2)),), (int(m.group(3)), int(m.group(4)), ),) )

for area in areas:
    print(f"Area: {area}")

def drag(x):
    if x < 0:
        return x + 1
    elif x > 0:
        return x -1
    else:
        return 0
    
def probe(vel):
    loc = (0,0)
    yield (loc,vel)

    while True:
        loc = (loc[0] + vel[0], loc[1] + vel[1],)
        vel = ( drag(vel[0]), vel[1]-1 )
        yield (loc,vel)

def inarea(loc,area):
    return loc[0] >= area[0][0] and loc[0] <= area[0][1] and loc[1] >= area[1][0] and loc[1] <= area[1][1]
        
def checkhit(initvel, area):
    for loc,vel in probe(initvel):
        #print(f"{loc}")
        if inarea(loc,area):
            return loc
        if vel[0] <= 0 and loc[0] < area[0][0]:
            return None
        if vel[0] >= 0 and loc[0] > area[0][1]:
            return None
        if vel[1] < 0 and loc[1] < area[1][0]:
            return None


def describe(initvel, area):
    if initvel[1] >= 0:
        maxy = initvel[1] * (initvel[1] + 1) // 2
    else:
        maxy = 0
    maxx = abs((initvel[0] * (initvel[0] + 1)) // 2)

    hitloc = None
    for loc,vel in probe(initvel):
        print(f"{loc} @ {vel}")
        if inarea(loc,area):
            hitloc = loc
            break
        if vel[0] == 0 and vel[1] < 0 and loc[1] < area[1][0]:
            break

    print(f"Max: ({maxx},{maxy}) hit: {hitloc}")

def figureX(xr):
    best = None
    i = 1
    while True:
        maxx = (i * (i+1)) // 2
        if maxx > xr[1]:
            break
        if maxx >= xr[0]:
            best = i
        i = i + 1
    return best
    
if args.p1:
    print("Doing part 1")

    xvel = figureX(area[0])
    yvel = abs(area[1][0]) - 1
        
    #print(f"{xvel},{yvel}")

    #describe( (xvel,yvel), area)

    maxy = ((yvel * (yvel+1))) // 2
    print(f"Highest: {maxy}")
    
    
if args.p2:
    print("Doing part 2")

    maxxvel = figureX(area[0])

    maxyvel = abs(area[1][0]) - 1

    hits = set()
    for xvel in range(0, max(area[0])+1):
        for yvel in range( area[1][0], maxyvel+1):
            #print(f"Checking: {(xvel,yvel)}")
            vel = (xvel, yvel)
            hitloc = checkhit( vel, area)
            if hitloc:
                hits.add(vel)
                #print(f"HIT: {hitloc} @ {vel}")

    print(f"Hits: {len(hits)}")
    
