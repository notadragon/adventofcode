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

lineRe = re.compile("^[\\\.\-\|/]+$")

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

deltas = {
    "e" : (1, 0),
    "w" : (-1, 0),
    "n" : (0, -1),
    "s" : (0, 1)
    }

mappings = {
    "." : {
        "n" : "n",
        "e" : "e",
        "s" : "s",
        "w" : "w"
        },

    "|" : {
        "n" : "n",
        "e" : "ns",
        "s" : "s",
        "w" : "ns"
        },
    
    "-" : {
        "n" : "ew",
        "e" : "e",
        "s" : "ew",
        "w" : "w"
        },

    "/" : {
        "n" : "e",
        "e" : "n",
        "s" : "w",
        "w" : "s"
        },

    "\\" : {
        "n" : "w",
        "e" : "s",
        "s" : "e",
        "w" : "n"
        },
    }
    


def numlit( beamstart, beamdir ):    
    beams = set()
    notdone = collections.deque([ ( beamstart, beamdir) ])
    while notdone:
        loc,d = notdone.popleft()

        #print(f"Loc: {loc} d: {d}")

        if loc[1] < 0 or loc[1] >= len(data):
            continue
        if loc[0] < 0 or loc[0] >= len(data[loc[1]]):
            continue

        if (loc,d) in beams:
            continue

        beams.add( (loc,d) )
        
        m = data[loc[1]][loc[0]]
        ddirs = mappings[m][d]

        for nextd in ddirs:
            nextddelta = deltas[nextd]
            nextloc = ( loc[0] + nextddelta[0], loc[1] + nextddelta[1], )

            notdone.append( (nextloc, nextd) )

    lit = len( set( loc for loc,d in beams ) )
    return lit

if args.p1:
    print("Doing part 1")

    lit = numlit( (0,0), "e" )
    print(f"Lit: {lit}")
    
if args.p2:
    print("Doing part 2")

    best = None
    
    for x in range(0, len(data[0])):
        loc = (x,0)
        d = "s"
        l = numlit( loc, d )

        if not best or best[2] < l:
            best = (loc,d,l)

        #print(f"{loc} {d} -> {l}")

        loc = (x,len(data)-1)
        d = "n"
        l = numlit( loc, d )

        if not best or best[2] < l:
            best = (loc,d,l)

        #print(f"{loc} {d} -> {l}")

    for y in range(0, len(data)):
        loc = (0, y)
        d = "e"
        l = numlit( loc, d )
        
        if not best or best[2] < l:
            best = (loc,d,l)

        #print(f"{loc} {d} -> {l}")

        loc = (len(data[0])-1, y)
        d = "w"
        l = numlit( loc, d )

        if not best or best[2] < l:
            best = (loc,d,l)

        #print(f"{loc} {d} -> {l}")

    print(f"best: {best}")

        
