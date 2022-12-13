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

lineRe = re.compile("^[SEa-z]+$")
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

elevations = {}
endpoints = [None, None]

dirdeltas = { (-1,0) : "<",
              (1,0)  : ">",
              (0,-1) : "^",
              (0,1)  : "v" }

for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        val = grid[y][x]
        if val == "S":
            endpoints[0] = (x,y)
            val = "a"
        elif val == "E":
            endpoints[1] = (x,y)
            val = "z"
        elevations[ (x,y) ] = ord(val) - ord("a")

def getPath(elevations, endpoints):
    prevsteps = {}
    prevsteps[ endpoints[0] ] = None
    tocheck = collections.deque([ endpoints[0] ])

    while tocheck and not endpoints[1] in prevsteps:
        ep = tocheck.popleft()
        epelev = elevations[ep]
        
        for delta in dirdeltas.keys(): 
            target = ( ep[0] + delta[0], ep[1] + delta[1] )
            if not target in elevations:
                continue
            if elevations[target] > epelev + 1:
                continue
            if target in prevsteps:
                continue
            
            prevsteps[target] = ep
            tocheck.append(target)

    path = [ endpoints[1] ]
    while path[-1] != endpoints[0]:
        path.append( prevsteps[path[-1]] )
    path.reverse()
            
    return path

def reversePath(elevations, endpoint):
    # take steps backwards to find closests "a"
    prevsteps = {}
    prevsteps[ endpoint ] = None
    tocheck = collections.deque([ endpoint ])

    startpoint = None
    
    while tocheck and startpoint == None:
        ep = tocheck.popleft()
        epelev = elevations[ep]
        
        for delta in dirdeltas.keys(): 
            target = ( ep[0] + delta[0], ep[1] + delta[1] )
            if not target in elevations:
                continue
            telev = elevations[target]
            if telev < epelev - 1:
                continue
            if target in prevsteps:
                continue
            
            prevsteps[target] = ep
            tocheck.append(target)

            if telev == 0:
                startpoint = target

    path = [ startpoint ]
    while path[-1] != endpoint:
        path.append( prevsteps[path[-1]] )
            
    return path


def showMap(elevations):
    minx = min([ loc[0] for loc in elevations.keys() ])
    miny = min([ loc[1] for loc in elevations.keys() ])
    maxx = max([ loc[0] for loc in elevations.keys() ])
    maxy = max([ loc[1] for loc in elevations.keys() ])

    for y in range(miny, maxy+1):
        line = []
        for x in range(minx, maxx+1):
            disp = "."
            if (x,y) in elevations:
                disp = chr( ord("a") + elevations[(x,y)])
            line.append(disp)
        print("".join(line))

def showPath(elevations,path):
    minx = min([ loc[0] for loc in elevations.keys() ])
    miny = min([ loc[1] for loc in elevations.keys() ])
    maxx = max([ loc[0] for loc in elevations.keys() ])
    maxy = max([ loc[1] for loc in elevations.keys() ])

    showpath = {}
    showpath[ path[-1] ] = "E"
    for x in range(0,len(path)-1):
        loc = path[x]
        nxt = path[x+1]
        pdelta = ( nxt[0] - loc[0], nxt[1] - loc[1] )
        showpath[ loc ] = dirdeltas[pdelta]
    
    for y in range(miny, maxy+1):
        line = []
        for x in range(minx, maxx+1):
            disp = "."
            if (x,y) in showpath:
                disp = showpath[ (x,y) ]
            elif (x,y) in elevations:
                disp = chr( ord("a") + elevations[(x,y)])
            line.append(disp)
        print("".join(line))

if args.p1:
    print("Doing part 1")

    path = getPath( elevations, endpoints )

    #print("MAP:")
    #showMap(elevations)

    #print("PATH:")
    #showPath(elevations,path)
    
    #print(f"Path: {path}")
    print(f"Path Length: {len(path)-1}")
    
if args.p2:
    print("Doing part 2")

    path = reversePath( elevations, endpoints[1] )

    #print("MAP:")
    #showMap(elevations)

    print("PATH:")
    showPath(elevations,path)
    
    #print(f"Path: {path}")
    print(f"Path Length: {len(path)-1}")
