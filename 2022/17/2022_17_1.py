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

lineRe = re.compile("^[<>]+$")

data = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = x

rocks = (
    ( "####", ),
    ( ".#.", "###", ".#." ),
    ( "..#", "..#", "###" ),
    ( "#", "#", "#", "#" ),
    ( "##", "##" ),
    )

def windgen(data, start=0):
    if start != 0:
        for x in enumerate(start,data[start:]):
            yield x
    while True:
        for x in enumerate(data):
            yield x

def rockgen(rocks, start=0):
    if start != 0:
        for x in enumerate(start,rocks[start:]):
            yield x
    while True:
        for x in enumerate(rocks):
            yield x

def printchamber(chamber, rock = None):
    minx = 0
    maxx = 7
    miny = min(l[1] for l in chamber) if len(chamber) else 0
    maxy = max(l[1] for l in chamber) if len(chamber) else 0
    if rock:
        maxy = max(maxy, max(r[1] for r in rock))
    for y in range(maxy,miny-1,-1):
        line = ["|"]
        for x in range(minx,maxx):
            if (x,y) in chamber:
                line.append("#")
            elif rock and (x,y) in rock:
                line.append("@")
            else:
                line.append(".")
        line.append("|")
        print("".join(line))
    if miny > 0:
        print(f"...{miny} more...")
    print("+-------+")

def putrock(rock, rockloc, chamber):
    toput = set()
    for ry in range(0,len(rock)):
        for rx in range(0,len(rock[ry])):
            if rock[ry][rx] == ".":
                continue
            loc = ( rockloc[0] + rx, rockloc[1] + (len(rock)-ry-1), )
            if loc[0] < 0 or loc[0] >= 7:
                return (False,None)
            if loc[1] < 0:
                return (False,None)
            if loc in chamber:
                return (False,loc)
            toput.add(loc)
    return (True,frozenset(toput))
            
    
                
def droprock(rock, chamber, windg, verbose):
    maxy = max(l[1]+1 for l in chamber) if len(chamber) else 0
    #print(F"maxy: {maxy}")
    rockloc = (2, maxy + 3)

    placed,rockstart = putrock(rock, rockloc, chamber)
    windnum = None

    if verbose:
        print("A new rock begins falling:")
        printchamber(chamber, rockstart)
    
    downnext = False
    toput = None
    while True:
        if downnext:
            delta = (0,-1)
        else:
            windnum,winddir = next(windg)

            if winddir == "<":
                delta = (-1,0)
                dirname = "left"
            else:
                delta = (1,0)
                dirname = "right"
        downnext = not downnext
        newrockloc = ( rockloc[0] + delta[0], rockloc[1] + delta[1], )
        placed,canput = putrock( rock, newrockloc, chamber)
        if not placed:
            if delta == (0,-1):
                if verbose:
                    print("Rock falls 1 unit, causing it to come to a rest:")
                break
            else:
                if verbose:
                    print(f"Jet of gas pushes rock {dirname}, but nothing happens:")
        else:
            if verbose:
                if delta == (0,-1):
                    print("Rock falls 1 unit:")
                else:
                    print(f"Jet of gas pushes rock {dirname}:")
            toput = canput
            rockloc = newrockloc

        if verbose:
            printchamber(chamber, toput)

    output = chamber.union(toput)

    if verbose:
        printchamber(output)

    return windnum, output
    
    
#print(f"Data: {data}")

def normalizechamber(chamber):
    if not len(chamber):
        return frozenset()
        
    miny = min(l[1] for l in chamber) 
    return frozenset(( (l[0],l[1]-miny) for l in chamber ))

def cropchamber(chamber):
    newchamber = set()

    maxy = max(l[1]+1 for l in chamber) if len(chamber) else 0
    
    for r in rocks:
        rockloc = (2, maxy + 1)
        tocheck = collections.deque([rockloc])
        visited = set([rockloc])
        while tocheck:
            loc = tocheck.popleft()
            visited.add(loc)
            for delta in ( (-1,0), (1,0), (0,-1), ):
                newloc = ( loc[0] + delta[0], loc[1] + delta[1], )
                if newloc in visited:
                    continue
                placed,res = putrock(r, newloc, chamber)
                if placed:
                    tocheck.append( newloc )
                else:
                    if res:
                        newchamber.add(res)
    #print(f"Cropped {len(chamber)} -> {len(newchamber)}")
    return frozenset(newchamber)


def chamberheight(chamber):
    return max(l[1]+1 for l in chamber) if len(chamber) else 0

if args.p1:
    print("Doing part 1")

    verbose = False
    
    chamber = frozenset()

    windg = windgen(data)
    rockg = rockgen(rocks)

    numrocks = 0
    for rocknum,r in rockg:
        wind,chamber = droprock(r,chamber, windg, verbose)
        #chamber = cropchamber(chamber)
        if verbose:
            printchamber(chamber)
        numrocks = numrocks + 1
            
        if numrocks >= 2022:
            break

    #printchamber(chamber)
    maxy = chamberheight(chamber)
    print(f"Chamber height: {maxy}")


if args.p2:
    print("Doing part 2")

    verbose = False

    chamber = frozenset()

    windg = windgen(data)
    rockg = rockgen(rocks)

    period = len(rocks) * len(data)
    heights = {}
    
    genindex = 0
    numrocks = 0

    cycle = None
    cyclesize = None
    targetrocks = 1000000000000
    
    for rocknum,r in rockg:
        windnum,chamber = droprock(r,chamber, windg, verbose)
        numrocks = numrocks + 1

        if numrocks % 1000 == 0:
            print(f"Rocks: {numrocks}")
        
        if verbose:
            printchamber(chamber)

        chamber = cropchamber(chamber)
        height = chamberheight(chamber)
        
        key = (rocknum,windnum, normalizechamber(chamber))
        value = (numrocks, height)
        
        if key in heights:
            if cyclesize == None:
                cyclesize = value[0] - heights[key][0]
                print(f"Cycle found {heights[key]} -> {value}")
                desiredrocks = targetrocks % cyclesize
                while desiredrocks < numrocks:
                    desiredrocks = desiredrocks + cyclesize
                print(f"Will wait for {desiredrocks} rocks")
            if numrocks % cyclesize == targetrocks % cyclesize:
                cycle = (key, heights[key], value)
                break
        elif cyclesize != None:
            print(f"Non-cycle at {numrocks} after cycle found???")
        heights[key] = value

    heightdiff = cycle[2][1] - cycle[1][1]
    rockdiff = cycle[2][0] - cycle[1][0]

    print(f"Cycle size: {rockdiff} Height delta: {heightdiff}")
    

    numcycles = (targetrocks - cycle[1][0]) // rockdiff
    
    numrocks = cycle[1][0] + numcycles * rockdiff
    targetheight = cycle[1][1] + numcycles * heightdiff
    print(f"Rocks: {numrocks}  Height: {targetheight}")
