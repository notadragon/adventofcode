#!/usr/bin/env pypy

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

grid = []

for x in open(args.input).readlines():
    x = x.rstrip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(x)


portals = {}
letters = list([ chr(c) for c in range(ord("A"),ord("Z")+1 ) ])

directions = {
    "^" : (0,-1),
    "v" : (0,1),
    "<" : (-1,0),
    ">" : (1,0),
}

if True:
    w = max([len(g) for g in grid])
    h = len(grid)

    for x,y in itertools.product(range(0,w),range(0,h)):
        if x >= len(grid[y]):
            continue
        #print("x,y: %s,%s" % (x,y,))
        if grid[y][x] in letters:
            #print("x,y:%s %s" % ((x,y,),grid[y][x],))
            for d in directions.values():
                ll = (x + d[0], y + d[1])
                if ll[1] < 0 or ll[1] >= h or ll[0] < 0 or ll[0] >= len(grid[ll[1]]):
                    continue
                pl = (x + 2*d[0], y + 2*d[1])
                if pl[1] < 0 or pl[1] >= h or pl[0] < 0 or pl[0] >= len(grid[pl[1]]):
                    continue
                #print("  d: %s" % (d,))
                #print("  PL: %s" % (pl,))
                nl = grid[y+d[1]][x+d[0]]
                #print("  %s %s" % (nl,grid[pl[1]][pl[0]],))
                if nl in letters and grid[pl[1]][pl[0]] == ".":
                    key = grid[y][x] + nl
                    if d[0] < 0 or d[1] < 0:
                        key = "".join(reversed(key))
                    if key not in portals:
                        portals[key] = []

                    if x == 0 or y == 0 or y+1 == h or x+1 == w:
                        portals[key].append( pl + (1,) )
                    else:
                        portals[key].insert( 0, pl + (-1,) )
                        
                    
            
#for x in grid:
#    print(x)
            
print("Portals: %s" % (portals,))
    

if args.p1:
    print("Doing part 1")

    start = portals["AA"][0][0:2]
    end = portals["ZZ"][0][0:2]
    
    connections = {}
    for v in portals.values():
        if len(v) == 2:
            connections[v[0][0:2]] = v[1][0:2]
            connections[v[1][0:2]] = v[0][0:2]
    
    tosearch = collections.deque( [start])
    distances = { start : 0 }
    while end not in distances:
        nextsearch = tosearch.popleft()
        nextd = distances[nextsearch]
        for d in directions.values():
            nl = (nextsearch[0] + d[0], nextsearch[1] + d[1],)
            if nl in distances:
                continue
            if nl[1] < 0 or nl[1] >= h or nl[0] < 0 or nl[0] >= len(grid[nl[1]]):
                continue
            if grid[nl[1]][nl[0]] == ".":
                distances[nl] = nextd + 1
                tosearch.append(nl)                
        if nextsearch in connections:
            nl = connections[nextsearch]
            if nl in distances:
                continue
            if nl[1] < 0 or nl[1] >= h or nl[0] < 0 or nl[0] >= len(grid[nl[1]]):
                continue
            distances[nl] = nextd + 1
            tosearch.append(nl)                

    print("Distance: %s" % (distances[end],))
                
if args.p2:
    print("Doing part 2")

    start = portals["AA"][0][0:2] + (0,)
    end = portals["ZZ"][0][0:2] + (0,)
    
    connections = {}
    for v in portals.values():
        if len(v) == 2:
            connections[v[0][0:2]] = v[1]
            connections[v[1][0:2]] = v[0]
    
    tosearch = collections.deque( [start] )
    distances = { start : 0 }
    while end not in distances:
        nextsearch = tosearch.popleft()
        nextd = distances[nextsearch]
        for d in directions.values():
            nl = (nextsearch[0] + d[0], nextsearch[1] + d[1], nextsearch[2], )
            if nl in distances:
                continue
            if nl[1] < 0 or nl[1] >= h or nl[0] < 0 or nl[0] >= len(grid[nl[1]]):
                continue
            if grid[nl[1]][nl[0]] == ".":
                distances[nl] = nextd + 1
                tosearch.append(nl)                
        if nextsearch[0:2] in connections:
            c = connections[nextsearch[0:2]]
            nl = c[0:2] + (nextsearch[2] + c[2],)
            if nl[2] < 0:
                continue
            if nl in distances:
                continue
            if nl[1] < 0 or nl[1] >= h or nl[0] < 0 or nl[0] >= len(grid[nl[1]]):
                continue
            distances[nl] = nextd + 1
            tosearch.append(nl)                

    print("Distance: %s" % (distances[end],))
