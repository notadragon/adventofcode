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

lineRe = re.compile("^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z]+(?:, [A-Z]+)*).*$")

data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    tovalves = tuple( m.group(3).split(", ") )
    data.append( ( m.group(1), int(m.group(2)), tovalves,) )

#for d in data:
#    print(f"{d}")

valves = {}
for d in data:
    valves[d[0]] = d[1:]

for k,d in valves.items():
    for adj in d[1]:
        if not k in valves[adj][1]:
            print(f"Path not  bidirectional: {k} <-> {adj}")

def getsteps(valves, shortestpaths, loc, loc2):
    if (loc,loc2) in shortestpaths:
        return shortestpaths[ (loc,loc2) ]

    tovisit = collections.deque([ (loc,0) ])
    visited = set( [loc] )
    
    while tovisit:
        tocheck,distance = tovisit.popleft()
        tocheckdata = valves[tocheck]

        if tocheckdata[0] > 0 or tocheck == loc2:
            shortestpaths[ (loc, tocheck) ] = distance
            #print(f"{loc} -> {tocheck} : {distance}")
        
        for adj in tocheckdata[1]:
            if adj in visited:
                continue
            visited.add(adj)
            tovisit.append( (adj,distance+1,) )
            
    return shortestpaths[ (loc, loc2) ]
            
        
            
def paths(valves, shortestpaths, loc, openvalves, timelimit):
    if timelimit == 0:
        yield (0, ())
        return

    if not loc in openvalves and valves[loc][0] != 0:
        pressure =  (timelimit-1) * valves[loc][0]
        step = f"open-{loc} ({pressure})"

        openvalves.add(loc)
        bestrest = None
        for rest in paths(valves, shortestpaths, loc, openvalves, timelimit-1):
            if not bestrest or rest[0] > bestrest[0]:
                bestrest = rest
        yield ( pressure + bestrest[0], (step,) + bestrest[1], )
        openvalves.remove(loc)
        return
        
    nextstep = []
    for key,data in valves.items():
        if key in openvalves:
            continue
        if data[0] == 0:
            continue
        shortest = getsteps(valves, shortestpaths, loc, key)
        nextpressure = (timelimit - shortest - 1) * data[0]
        if nextpressure <= 0:
            continue
        nextstep.append( (nextpressure, shortest, key) )
        
    if nextstep:
        nextstep.sort(reverse=True)

        bestrest = None
        for nextpressure, shortest, key in nextstep:
            for rest in paths(valves, shortestpaths, key, openvalves, timelimit-shortest):
                if not bestrest or rest[0] > bestrest[0]:
                    bestrest = ( rest[0], (f"{shortest}->{key}",) + rest[1],)
                
        yield bestrest
        
    else:
        yield (0, ())
    
def paths2(valves, shortestpaths, loc, openvalves):
    # loc is list of pairs, timelimit,location
    # yield (<totalpressure>, (path,) )

    nexttimelimit, nextloc, nextid = loc[0]
    if nexttimelimit == 0:
        return (0, (), )
    
    if not (nextloc in openvalves) and valves[nextloc][0] != 0:
        pressure = (nexttimelimit-1) * valves[nextloc][0]
        step = f"open-{nextloc} ({pressure} by {nextid})"
        
        newloc = [ (nexttimelimit-1,nextloc,nextid), ] + loc[1:]
        newloc.sort(reverse=True)
        newloc = tuple(newloc)
        newopen = openvalues.union((nextloc))
        
        bestrest = paths2(valves, shortestpaths, newloc, newopen)
        return (pressure + bestrest[0], (step,) + bestrest[1], )

    nextstep = []
    for key,data in valves.items():
        if key in openvalves:
            continue
        if data[0] == 0:
            continue
        shortest = getsteps(valves, shortestpaths, nextloc, key)
        nextpressure = (nexttimelimit - shortest - 1) * data[0]
        if nextpressure <= 0:
            continue
        nextstep.append( (nextpressure, shortest, key) )

    if not nextstep:
        newloc = [ (0, nextloc, nextid), ] + loc[1:]
        newloc.sort(reverse=True)
        return paths2(valves, shortestpaths, newloc, openvalves)
    
    else:
        #determine number of movers:
        nummovers = 1
        while nummovers < min(len(nextstep),len(loc)) and loc[nummovers][0] == nexttimelimit and loc[nummovers][1] == nextloc:
            nummovers = nummovers + 1

        bestrest = None
        for steps in itertools.combinations( nextstep, nummovers ):
            newloc = []
            pressure = 0
            desc = []
            for n,step in enumerate(steps):
                nextpressure, shortest, key = step
                nid = loc[n][2]
                newloc.append( (nexttimelimit - shortest -1, key, nid) )
                openvalves.add(key)
                pressure = pressure + nextpressure
                desc.append(f"{shortest}->{key} ({nid})")
                desc.append(f"open-{key} ({nextpressure} by {nid})")
            desc = tuple(desc)
            
            newloc.extend( loc[nummovers:] )
            newloc.sort(reverse=True)
                
            rest = paths2(valves, shortestpaths, newloc, openvalves)
            if not bestrest or (pressure + rest[0]) > bestrest[0]:
                bestrest = ( pressure + rest[0],  desc + rest[1],)

            for step in steps:
                nextpressure, shortest, key = step
                openvalves.remove(key)
                
        return bestrest

    
if args.p1:
    print("Doing part 1")

    if False:
        timelimit = 30
        loc = "AA"
    
        openvalves = frozenset()
        maxpressure = 0
        shortestpaths = {}
        for p in paths(valves, shortestpaths, loc, openvalves, timelimit):
            if p[0] > maxpressure:
                print(f"Best Path: {p}")
                maxpressure = p[0]
    else:
        timelimit = 30
        loc = [ (30,"AA","H",), ]
        openvalves = set()
        maxpressure = 0
        shortestpaths = {}
        p = paths2(valves, shortestpaths, loc, openvalves)
        if p[0] > maxpressure:
            print(f"Best Path: {p}")
            maxpressure = p[0]


if args.p2:
    print("Doing part 2")

    timelimit = 26
    loc = [ (26,"AA","H",), (26,"AA","H",), ]
    openvalves = set()
    maxpressure = 0
    shortestpaths = {}
    p = paths2(valves, shortestpaths, loc, openvalves)
    if p[0] > maxpressure:
        print(f"Best Path: {p}")
        maxpressure = p[0]


    
