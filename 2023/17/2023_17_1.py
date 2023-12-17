#!/usr/bin/env pypy3

import argparse, re, itertools, collections, queue

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

lineRe = re.compile("^[0-9]+$")

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

losses = {}
for y in range(0,len(data)):
    for x in range(0,len(data[y])):
        losses[ (x,y) ] = int(data[y][x])
    
    
deltas = {
    "e" : (1, 0),
    "w" : (-1, 0),
    "n" : (0, -1),
    "s" : (0, 1)
    }

if args.p1:
    print("Doing part 1")

    startloc = (0,0)
    destloc = ( len(data[-1])-1, len(data)-1 )

    found = {
        #loc, indir -> heat
    }

    tosearch = queue.PriorityQueue()
    tosearch.put( ( 0, 1, startloc, "n", ) )
    tosearch.put( ( 0, 1, startloc, "w", ) )

    while not tosearch.empty():
        heat, numsteps, loc, indir = tosearch.get()

        if (loc, indir) in found:
            best = found[ (loc,indir) ]
            if heat >= best:
                continue
        found[ (loc, indir) ] = heat
        
        outdirs = []
        if len(indir) < 3:
            outdirs.append(indir[-1])
        if indir[-1] in "ns":
            outdirs.extend(("e", "w"))
        else:
            outdirs.extend(("s", "n"))
            
        for d in outdirs:
            ddelta = deltas[d]
            nextloc = ( loc[0] + ddelta[0], loc[1] + ddelta[1], )
            nextdir = None
            if d == indir[-1]:
                nextdir = indir + d
            else:
                nextdir = d
            if nextloc not in losses:
                continue
            
            nextheat = losses[ nextloc ]
            nexttotal = heat + nextheat

            tosearch.put( (nexttotal, len(nextdir), nextloc, nextdir,) )

    minheat = min( [ h for x,h in found.items() if x[0] == destloc ] )

    print(f"Min heat: {minheat}")
            
if args.p2:
    print("Doing part 2")

    startloc = (0,0)
    destloc = ( len(data[-1])-1, len(data)-1 )

    found = {
        #loc, indir -> heat
    }

    tosearch = queue.PriorityQueue()
    tosearch.put( ( 0, 1, startloc, "n", ) )
    tosearch.put( ( 0, 1, startloc, "w", ) )


    while not tosearch.empty():
        heat, numsteps, loc, indir = tosearch.get()

        #print(f"{loc} {indir} -> {heat}")
        
        if (loc, indir) in found:
            best = found[ (loc,indir) ]
            if heat >= best:
                continue
        
        found[ (loc, indir) ] = heat
        
        outdirs = []
        if len(indir) < 10:
            outdirs.append(indir[-1])
        if indir[-1] in "ns":
            outdirs.extend(("eeee", "wwww"))
        else:
            outdirs.extend(("ssss", "nnnn"))
            
        for d in outdirs:
            nextloc = loc
            nextheat = 0
            for step in d:
                sdelta = deltas[step]
                nextloc = ( nextloc[0] + sdelta[0], nextloc[1] + sdelta[1], )
                if nextloc not in losses:
                    nextloc = None
                    break
                nextheat = nextheat + losses[nextloc]
            if not nextloc:
                continue
            if d[0] == indir[-1]:
                nextdir = indir + d
            else:
                nextdir = d

            nexttotal = heat + nextheat

            tosearch.put( (nexttotal, len(nextdir), nextloc, nextdir) )

    minheat = min( [ h for x,h in found.items() if x[0] == destloc ] )
    print(f"Min heat: {minheat}")
