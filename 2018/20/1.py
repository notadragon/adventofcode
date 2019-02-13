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

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = x

print("Data size: %s" % (len(data,)))
dataRe = re.compile(data)

deltas = { "N" : (0,-1,0,3,"-"),
           "W" : (-1,0,1,2,"|"),
           "E" : (1,0, 2,1,"|"),
           "S" : (0,1, 3,0,"-"), }

dirs = [ "N", "W", "E", "S" ]

def doGenerate(splitup):
    #print("Generating for: %s" % (splitup,))

    if len(splitup) == 0:
        yield ""
        return
    
    if type(splitup) is str:
        #print("  Yielding String: %s" % (splitup,))
        yield splitup
        return
    
    if len(splitup) == 1:
        for e in doGenerate(splitup[0]):
            yield e
        return
    
    alternates = []
    alt = []
    alternates.append(alt)
    for t in splitup:
        if t == "|":
            alt = []
            alternates.append(alt)
        else:
            alt.append(t)

    for alt in alternates:
        #print("alt: %s" % (alt,))

        parts = [ list(doGenerate(part)) for part in alt ]

        #print("Parts: %s" % (parts,))
        
        for e in itertools.product(*parts):
            yield "".join(e)

def generatePaths(tokens):

    out = []
    outstack = []

    outstack.append(out)

    for t in tokens:
        if t == "(":
            newout = []
            out.append(newout)
            outstack.append(newout)
            out = newout
        elif t == ")":
            out = outstack[-2]
            del outstack[-1]
        else:
            out.append(t)

    #print("Splitup: %s" % (out,))            

    for p in doGenerate(out):
        yield p

def showrooms(rooms):
    minx = min([ x[0] for x in rooms.keys() ])
    maxx = max([ x[0] for x in rooms.keys() ]) + 1
    miny = min([ x[1] for x in rooms.keys() ])
    maxy = max([ x[1] for x in rooms.keys() ]) + 1
    
    print(" Grid Range: %s - %s x %s - %s" % (minx,maxx,miny,maxy,))

    grid = [ [ " " for x in range(0, (maxx-minx+1) * 2 ) ] for y in range(0, (maxy-miny+1)*2) ]

    for loc,room in rooms.items():
        #print("%s -> %s" % (loc,room,))

        roomloc = ( (loc[0] - minx) * 2, (loc[1] - miny) * 2, )
        grid[roomloc[1]][roomloc[0]]     = "#"
        grid[roomloc[1]][roomloc[0]+1]   = room[0]
        grid[roomloc[1]][roomloc[0]+2]   = "#"
        grid[roomloc[1]+1][roomloc[0]]   = room[1]
        grid[roomloc[1]+1][roomloc[0]+1] = room[4]
        grid[roomloc[1]+1][roomloc[0]+2] = room[2]
        grid[roomloc[1]+2][roomloc[0]]   = "#"
        grid[roomloc[1]+2][roomloc[0]+1] = room[3]
        grid[roomloc[1]+2][roomloc[0]+2] = "#"
    
    for g in grid:
        print("".join(g))


def generateRooms(tokens):
    rooms = {}
    rooms[ (0,0) ] = [ "#", ] * 4 + ["X"]

    for m in generatePaths(tokens):
        #print("Path: %s" % (m,))

        loc = (0,0)
        
        for dir in m:
            dx,dy,idx,ridx,doorsym = deltas[dir]

            tloc = (loc[0] + dx, loc[1] + dy)
            room = rooms[loc]
            if tloc in rooms:
                troom = rooms[tloc]
            else:
                troom = [ "#", ] * 4 + ["."]
                rooms[tloc] = troom

            room [ idx  ] = doorsym
            troom[ ridx ] = doorsym

            loc = tloc

    return rooms

def buildrooms( startloc, splitup, rooms):

    #print("BuildRooms: %s %s" % (startloc,splitup,))
    
    if len(splitup) == 0:
        return

    if type(splitup) is str:
        loc = startloc
        room = rooms[loc]
        
        for d in splitup:
            dx, dy, idx, ridx, doorsym = deltas[d]

            tloc = (loc[0] + dx, loc[1] + dy)
            if tloc in rooms:
                troom = rooms[tloc]
            else:
                troom = [ "#", ] * 4 + ["."]
                rooms[tloc] = troom

            room [ idx  ] = doorsym
            troom[ ridx ] = doorsym

            loc = tloc
            room = troom

        yield loc
        return

    if len(splitup) == 1:
        for l in buildrooms(startloc,splitup[0],rooms):
            yield l
        return

    alternates = []
    alt = []
    alternates.append(alt)
    for t in splitup:
        if t == "|":
            alt = []
            alternates.append(alt)
        else:
            alt.append(t)


    for alt in alternates:

        locs = set()
        locs.add(startloc)

        
        for step in alt:
            nextlocs = set()
            for loc in locs:
                for nloc in buildrooms( loc, step, rooms):
                    nextlocs.add(nloc)
            locs = nextlocs

        for loc in locs:
            yield loc

        
            
def generateRooms2(tokens):
    rooms = {}
    rooms[ (0,0) ] = [ "#", ] * 4 + ["X"]

    out = []
    outstack = []

    outstack.append(out)

    for t in tokens:
        if t == "(":
            newout = []
            out.append(newout)
            outstack.append(newout)
            out = newout
        elif t == ")":
            out = outstack[-2]
            del outstack[-1]
        else:
            out.append(t)

    #print("Splitup: %s" % (out,))            

    for c in buildrooms( (0,0), out, rooms):
        pass

    return rooms
    
if True:
    tokenRe = re.compile("[NSEW]+|[()\\|]")

    tokens = list(tokenRe.findall(data));

    rooms = generateRooms2(tokens)

    showrooms(rooms)
    
    distances = { (0,0) : 0 }
    tocheck = collections.deque()
    tocheck.append( (0,0) )
    while tocheck:
        loc = tocheck.popleft()
        room = rooms[loc]
        roomdistance = distances[loc]
        
        for d in dirs:
            dx, dy, idx, ridx, doorsym = deltas[d]
            if room[idx] != "#":
                tloc = (loc[0] + dx, loc[1] + dy)
                if tloc in distances:
                    continue
                distances[tloc] = roomdistance + 1
                tocheck.append( tloc )

    #print("Distances: %s" % (distances,))


if args.p1:
    print("Doing part 1")
    print("Max Distance: %s" % (max([d for d in distances.values()]),))

                
if args.p2:
    print("Doing part 2")
    print(">1000 distance: %s" % (sum([1 for d in distances.values() if d >= 1000]),))
    
