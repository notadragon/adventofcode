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

elves = set()
for y in range(0,len(data)):
    for x in range(0,len(data[y])):
        if data[y][x] == "#":
            elves.add( (x,y) )

deltas = {
    "N"  : (0,-1),
    "NE" : (1,-1),
    "E"  : (1,0),
    "SE" : (1,1),
    "S"  : (0,1),
    "SW" : (-1,1),
    "W"  : (-1,0),
    "NW" : (-1,-1),
    ""   : (0,0), 
    }

conditions = [
    ("N" , set(( "N", "NE", "NW", )) ),
    ("S" , set(( "S", "SE", "SW", )) ),
    ("W" , set(( "W", "NW", "SW", )) ),
    ("E" , set(( "E", "NE", "SE", )) ),
    ]

def getadj(loc,d):
    delta = deltas[d]
    return (loc[0] + delta[0], loc[1] + delta[1])

def round(elves, roundnum):
    proposals = {}
    for loc in elves:
        proposeddir = ""
        newloc = None
        adjacencies = set()
        for d in deltas.keys():
            if d:
                adj = getadj(loc,d)
                if adj in elves:
                    adjacencies.add(d)

        if adjacencies:
            for n in range(0,len(conditions)):
                condition = conditions[ (roundnum + n) % len(conditions) ]
                d,tocheck = condition

                occupied = False
                for a in tocheck:
                    if a in adjacencies:
                        occupied = True
                        break
                if not occupied:
                    newloc = getadj(loc,d)
                    proposeddir = d
                    break

        if not newloc:
            newloc = loc

        #print(f"{loc} -> {adjacencies} -> {proposeddir}")
            
        if newloc in proposals:
            proposals[newloc].append(loc)
        else:
            proposals[newloc] = [loc,]

    output = set()
    for loc,es in proposals.items():
        if len(es) > 1:
            #elves don't move
            for e in es:
                output.add(e)
        else:
            # elf moves
            output.add(loc)

    return output

def bounds(elves):
    minx = min(e[0] for e in elves)
    maxx = max(e[0] for e in elves)
    miny = min(e[1] for e in elves)
    maxy = max(e[1] for e in elves)

    return (minx, maxx, miny, maxy)

def printelves(elves):
    minx, maxx, miny, maxy = bounds(elves)

    for y in range(miny,maxy+1):
        line = []
        for x in range(minx,maxx+1):
            if (x,y) in elves:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))



if args.p1:
    print("Doing part 1")

    estate = elves
    print("== Initial State ==")
    printelves(estate)
    
    for i in range(0,10):
        print(f"== End of Round {i+1} ==")
        estate = round(estate, i)
        printelves(estate)

    minx, maxx, miny, maxy = bounds(estate)
    rectsize = (maxx-minx+1) * (maxy-miny+1)
    print(f"Rectangle size: {maxx-minx+1} * {maxy-miny+1} = {rectsize}")
    print(f"Empty space: {rectsize - len(estate)}")
    
if args.p2:
    print("Doing part 2")

    estate = elves
    print("== Initial State ==")
    printelves(estate)

    rounds = 0
    while True:
        newstate = round(estate, rounds)
        rounds = rounds + 1

        if newstate == estate:
            break
        else:
            estate = newstate

    print("== Final State ==")
    printelves(estate)
    print(f"Rounds: {rounds}")
    
