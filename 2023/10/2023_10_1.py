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

lineRe = re.compile("^[\|\-\.LFJS7]+$")
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

pipedeltas  = {
    "|" : ( (0, -1), (0, 1) ),
    "-" : ( (-1, 0), (1, 0) ),
    "L" : ( (0, -1), (1, 0) ),
    "J" : ( (-1, 0), (0, -1), ),
    "7" : ( (-1, 0), (0, 1),  ),
    "F" : ( (0, 1), (1, 0) )
}

def neighbors(val):
    return pipedeltas.get(val, ())

adjdeltas = ( (-1,0), (1, 0), (0, -1), (0, 1) )


def addlocs(l1, l2):
    return ( l1[0] + l2[0], l1[1] + l2[1], )
    

if args.p1:
    print("Doing part 1")

    pipes = {}
    startpos = None
    for y in range(0,len(data)):
        for x in range(0,len(data[y])):
            val = data[y][x]
            if val != ".":
                pipes[ (x,y) ] = val
                
            if val == "S":
                startpos = (x,y)

    def getval(loc):
        return pipes.get(loc, ".")
        
    connected = []
    for adj in adjdeltas:
        sadj = addlocs( startpos, adj )
        v = getval(sadj)
        for cposd in neighbors(v):
            if addlocs(sadj, cposd) == startpos:
                connected.append(adj)
    connected.sort()
    connected = tuple(connected)
    startval = None
    for v,ds in pipedeltas.items():
        if connected == ds:
            startval = v

    pipes[startpos] = startval

    #print(f"Start Pos: {startpos} : {connected} -> {startval}")


    distances = {
        startpos : 0
    }
    distance = 0
    dposes = [ startpos, ]

    while True:
        found = False
        nextposes = []
        for pos in dposes:
            v = getval(pos)
            for delta in neighbors(v):
                npos = addlocs(pos, delta)
                if not npos in distances:
                    distances[npos] = distance + 1
                    nextposes.append(npos)
                    found = True
        if not found:
            break
        #print(f"{nextposes} -> {distance+1}")
        dposes = nextposes
        distance = distance + 1
        
    maxdist = max( distances.values() )
    print(f"Max distance: {maxdist}")
    
    
    
if args.p2:
    print("Doing part 2")

    pipes = {}
    startpos = None
    for y in range(0,len(data)):
        for x in range(0,len(data[y])):
            val = data[y][x]
            if val != ".":
                pipes[ (x,y) ] = val
                
            if val == "S":
                startpos = (x,y)

    def getval(loc):
        return pipes.get(loc, ".")
        
    connected = []
    for adj in adjdeltas:
        sadj = addlocs( startpos, adj )
        v = getval(sadj)
        for cposd in neighbors(v):
            if addlocs(sadj, cposd) == startpos:
                connected.append(adj)
    connected.sort()
    connected = tuple(connected)
    startval = None
    for v,ds in pipedeltas.items():
        if connected == ds:
            startval = v

    pipes[startpos] = startval

    distances = {
        startpos : 0
    }
    distance = 0
    dposes = [ startpos, ]

    while True:
        found = False
        nextposes = []
        for pos in dposes:
            v = getval(pos)
            for delta in neighbors(v):
                npos = addlocs(pos, delta)
                if not npos in distances:
                    distances[npos] = distance + 1
                    nextposes.append(npos)
                    found = True
        if not found:
            break
        #print(f"{nextposes} -> {distance+1}")
        dposes = nextposes
        distance = distance + 1
        
    # mainloop = distances.keys()

    loop = set(distances.keys())
               
    minx = min( loc[0] for loc in distances.keys() )
    maxx = max( loc[0] for loc in distances.keys() )
    miny = min( loc[1] for loc in distances.keys() )
    maxy = max( loc[1] for loc in distances.keys() )

    def inloop( pos, loop, pipes):
        if pos in loop:
            return False
        x = pos[0]
        crossings = 0
        xingstart = None
        while x >= minx-1:
            l = (x, pos[1] )
            if l in loop:
                v = pipes[l]
                if v == "|":
                    crossings = crossings + 1
                elif v != "-":
                    if xingstart == None:
                        xingstart = v
                    else:
                        # J,7 start, L, F end
                        if (v == "L" and xingstart == "7") or (v == "F" and xingstart == "J"):
                            crossings = crossings + 1
                        xingstart = None
                        
            x = x - 1

        return (crossings % 2) == 1

    inlooptiles = set()
    for x in range(minx-1, maxx+2):
        for y in range(miny-1, maxy+2):
            if inloop( (x,y), loop, pipes ):
                inlooptiles.add( (x,y) )

    for y in range(miny-1, maxy+2):
        row = []
        for x in range(minx-1, maxx+2):
            if (x,y) in inlooptiles:
                row.append("I")
            elif (x,y) in loop:
                row.append( pipes[(x,y)] )
            else:
                row.append(".")
        print("".join(row))
                
            

    print(f"inlooptiles: {len(inlooptiles)}")
            
        
