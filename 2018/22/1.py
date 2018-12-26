#!/usr/bin/env pypy

import argparse, re, collections

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

lineRe = re.compile("(?:depth: ([-?[0-9]+))|(?:target: (-?[0-9]+),(-?[0-9]+))")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        depth = int(m.group(1))
    else:
        target = (int(m.group(2)), int(m.group(3)),)

print("Depth: %s Target: %s" % (depth,target,))

indexes = { (0,0) : 0,
            target : 0, }
levels = {}

def geologicIndex(x,y):
    if (x,y) in indexes:
        return indexes[(x,y)]
    
    if y == 0:
        out = 16807 * x
    elif x == 0:
        out = y * 48271
    else:
        out = erosionLevel(x-1,y) * erosionLevel(x,y-1)
        
    indexes[ (x,y) ] = out
    return out

def erosionLevel(x,y):
    if (x,y) in levels:
        return levels[ (x,y) ]
    
    out = (geologicIndex(x,y) + depth) % 20183

    levels [ (x,y) ] = out
    return out
    
def displayRegion(x,y):
    if (x,y) == (0,0):
        return "M"
    elif (x,y)  == target:
        return "T"
    else:
        return regionType(x,y)

# rocky, wet, narrow
regionTypes = [".","=","}"]

    
def regionType(x,y):
    return [".","=","|",][erosionLevel(x,y) % 3]

def riskLevel(x,y):
    return erosionLevel(x,y) % 3
    
def showRegion( maxx, maxy ):
    for y in range(0,maxy+1):
        print("".join([ displayRegion(x,y) for x in range(0,maxx+1) ]))

if args.p1:
    print("Doing part 1")

    totalRisk = sum([ sum([ riskLevel(x,y) for x in range(0,target[0]+1)]) for y in range(0,target[1]+1) ])

    print("Total Risk: %s" % (totalRisk,))
    
# "." = no equipment
# "c" = climmbing gear
# "t" = torch

toolTypes = [ ".", "c", "t" ]
allowedTypes = { "." : ["c","t"],
                 "=" : [".","c"],
                 "|" : [".","t"], }

dirs = [ (-1,0), (0,-1), (1,0), (0,1) ]

if args.p2:
    print("Doing part 2")

    mintimes = { (0,0) : [-1,7,0] }
    tocheck = collections.deque()
    tocheck.append( (0,0) )

    targetTime = -1
    
    while tocheck:
        loc = tocheck.popleft()
        loctimes = mintimes[loc]

        for delta in dirs:
            #print("Delta; %s" % (delta,))
            updated = False

            tloc = (loc[0] + delta[0], loc[1] + delta[1])
            if tloc[0] < 0 or tloc[1] < 0:
                continue
            trtype = regionType(tloc[0],tloc[1])
            trtools = allowedTypes[trtype]

            if tloc not in mintimes:
                mintimes[tloc] = [ -1, ] * len(toolTypes)
            ttimes = mintimes[tloc]

            #print("Tloc: %s (%s %s)" % (tloc,trtype,trtools,))
            
            
            for toolidx in range(0,len(toolTypes)):
                tool = toolTypes[toolidx]
                time = loctimes[toolidx]
                if time < 0:
                    # not an allowed tool for this location
                    #print("Cannot have %s here" % (tool,))
                    continue

                if not tool in trtools:
                    #print("Cannot take %s to %s" % (tool,trtools,))
                    continue

                #print("Taking %s to %s" % (tool,tloc,))

                # we can go to target region!
                ttime = time + 1
                if ttimes[toolidx] < 0 or ttimes[toolidx] > ttime:
                    ttimes[toolidx] = ttime
                    updated = True

            if updated:
                # we found a faster route to tloc!
                mintime = min(t for t in ttimes if t >= 0)
                for toolidx in range(0,len(toolTypes)):
                    tool = toolTypes[toolidx]
                    if tool in trtools:
                        if ttimes[toolidx] < 0 or ttimes[toolidx] >= mintime + 7:
                            ttimes[toolidx] = mintime + 7

                if tloc == target:
                    targetTime = ttimes[2]
                else:
                    if targetTime < 0 or mintime < targetTime:
                        tocheck.append(tloc)
                            
                #print("Tloc: %s ttimes: %s" % (tloc,ttimes,))
                
    print("Target Time: %s" % (targetTime,))
