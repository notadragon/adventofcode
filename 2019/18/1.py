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
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(x.strip())

directions = {
    (0,1),
    (0,-1),
    (-1,0),
    (1,0),
}
    
def findpaths(grid, loc, locations, blocked, cached = {}):
    # yield ( (list of keys,), steps )

    if not locations:
        yield ( (), 0)
        return

    locationskey = "%s %s" % (loc,"".join(sorted(locations.keys())))
    if locationskey in cached:
        yield cached[locationskey]
        return
    
    reachable = []

    tosearch = collections.deque( [ (loc,0,)] )
    searched = set()
    while tosearch:
        l,steps = tosearch.popleft()
        searched.add(l)
        for heading in directions:
            nextloc = ( l[0] + heading[0], l[1] + heading[1],)
            if grid[nextloc[1]][nextloc[0]] != ".":
                continue
            if nextloc in searched:
                continue

            nextsearch = ( nextloc, steps+1 if steps >= 0 else steps -1)
            
            if nextloc in blocked:
                atloc = blocked[nextloc]
                if atloc.isupper():
                    # locked door
                    continue
                elif nextsearch[1] > 0:
                    reachable.append( (nextsearch[1], atloc) )
                nextsearch = ( nextloc, -abs(nextloc[1]), )

            tosearch.append( nextsearch )

    reachable.sort()
    #print("Reachable: %s" % (reachable,))

    stepgens = {}
    for steps,k in reachable:
        newlocations = { a:b for a,b in locations.items() if a.lower() != k }
        newblocked = { l:v for v,l in newlocations.items() }

        stepgens[k] = (steps,findpaths(grid, locations[k], newlocations, newblocked))

    bestout = None
    minsteps = None
    while stepgens:
        for k in stepgens.keys():
            steps,g = stepgens[k]
            gmore = False
            for ks,ksteps in g:
                out = ( (k,) + ks, ksteps + steps)
                
                if minsteps == None or out[1] < minsteps:
                    bestout = out
                    minsteps = out[1]
                gmore = True
                break
            if not gmore:
                del stepgens[k]

    cached[locationskey] = bestout
    yield bestout
                                
def findpaths2(grid, locs, locations, blocked, cached = {}):
    # yield ( (list of keys,), steps )

    if not locations:
        yield ( (), 0)
        return

    locationskey = "%s %s" % (locs,"".join(sorted(locations.keys())))
    if locationskey in cached:
        yield cached[locationskey]
        return
    
    reachable = []

    for li in range(0,len(locs)):
        loc = locs[li]

        tosearch = collections.deque( [ (loc,0,)] )
        searched = set()
        while tosearch:
            l,steps = tosearch.popleft()
            searched.add(l)
            for heading in directions:
                nextloc = ( l[0] + heading[0], l[1] + heading[1],)
                if grid[nextloc[1]][nextloc[0]] != ".":
                    continue
                if nextloc in searched:
                    continue
    
                nextsearch = ( nextloc, steps+1 if steps >= 0 else steps -1)
                
                if nextloc in blocked:
                    atloc = blocked[nextloc]
                    if atloc.isupper():
                        # locked door
                        continue
                    elif nextsearch[1] > 0:
                        reachable.append( (nextsearch[1], li, atloc) )
                    nextsearch = ( nextloc, -abs(nextloc[1]), )
    
                tosearch.append( nextsearch )
    
    reachable.sort()
    #print("Reachable: %s" % (reachable,))

    stepgens = {}
    for steps,li,k in reachable:
        newlocations = { a:b for a,b in locations.items() if a.lower() != k }
        newblocked = { l:v for v,l in newlocations.items() }

        newlocs = list(locs)
        newlocs[li] = locations[k]
        
        stepgens[k] = (steps,findpaths2(grid, newlocs, newlocations, newblocked))

    bestout = None
    minsteps = None
    while stepgens:
        for k in stepgens.keys():
            steps,g = stepgens[k]
            gmore = False
            for ks,ksteps in g:
                out = ( (k,) + ks, ksteps + steps)
                
                if minsteps == None or out[1] < minsteps:
                    bestout = out
                    minsteps = out[1]
                gmore = True
                break
            if not gmore:
                del stepgens[k]

    cached[locationskey] = bestout
    yield bestout
                                
if args.p1:
    print("Doing part 1")
    
    w = len(grid[0])
    h = len(grid)

    locations = {}
    blocked = {}
    for x,y in itertools.product(range(0,w),range(0,h)):
        v = grid[y][x]
        if v == "." or v == "#":
            pass
        elif v == "@":
            loc = (x,y)
        else:
            if v in locations:
                print("Duplicate: %s" % (v,))
            locations[v] = (x,y)
            blocked[ (x,y) ] = v

    cleargrid = []
    for g in grid:
        g = "".join([ "#" if c == "#" else "." for c in g ])
        cleargrid.append(g)

    for g in grid:
        print(g)
    
    print("Locations: %s" % (locations,))

    bestpath = None
    for path in findpaths(cleargrid,loc,locations,blocked):
        if bestpath == None or path[1] < bestpath[1]:
            print("Best Path: %s" % (path,))
            bestpath = path

    print("Best Path: %s" % (bestpath,))
        
    
if args.p2:
    print("Doing part 2")

    w = len(grid[0])
    h = len(grid)

    locations = {}
    blocked = {}
    for x,y in itertools.product(range(0,w),range(0,h)):
        v = grid[y][x]
        if v == "." or v == "#":
            pass
        elif v == "@":
            loc = (x,y)
        else:
            if v in locations:
                print("Duplicate: %s" % (v,))
            locations[v] = (x,y)
            blocked[ (x,y) ] = v

    grid = list([ str(g) for g in grid])

    locs = ( (loc[0]-1, loc[1]-1),
             (loc[0]+1, loc[1]-1),
             (loc[0]-1, loc[1]+1),
             (loc[0]+1, loc[1]+1) )

    def splice(s, ndx, repl):
        return s[0:ndx-1] + repl + s[ndx+len(repl)-1:]
    grid[loc[1]-1] = splice(grid[loc[1]-1], loc[0], "@#@")
    grid[loc[1]  ] = splice(grid[loc[1]  ], loc[0], "###")
    grid[loc[1]+1] = splice(grid[loc[1]+1], loc[0], "@#@")
    
    cleargrid = []
    for g in grid:
        g = "".join([ "#" if c == "#" else "." for c in g ])
        cleargrid.append(g)
    
    for g in grid:
        print(g)

    bestpath = None
    for path in findpaths2(cleargrid,locs,locations,blocked):
        if bestpath == None or path[1] < bestpath[1]:
            print("Best Path: %s" % (path,))
            bestpath = path

    print("Best Path: %s" % (bestpath,))
