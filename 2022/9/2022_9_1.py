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

lineRe = re.compile("^([UDLR]) ([0-9]+)$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (m.group(1), int(m.group(2)), ) )

dirs = { "U" : (0,-1),
         "D" : (0,1),
         "L" : (-1,0),
         "R" : (1,0),
}

def printrope(ropeloc):
    minx = min([p[0] for p in ropeloc] + [0,] )
    miny = min([p[1] for p in ropeloc] + [0,] )
    maxx = max([p[0] for p in ropeloc] + [0,] )
    maxy = max([p[1] for p in ropeloc] + [0,])

    lines = []
    for y in range(miny-1, maxy+2):
        line = []
        for x in range(minx-1, maxx + 2):
            try :
                n = ropeloc.index( (x,y) )
                if 0 == n:
                    line.append("H")
                elif len(ropeloc) - 1 == n:
                    line.append("T")
                else:
                    line.append(f"{n}")
            except ValueError as e:
                if (x,y) == (0,0):
                    line.append("s")
                else:
                    line.append(".")
        lines.append("".join(line))

    for l in lines:
        print(l)    

def printposes(poses):
    minx = min([p[0] for p in poses])
    miny = min([p[1] for p in poses])
    maxx = max([p[0] for p in poses])
    maxy = max([p[1] for p in poses])

    lines = []
    for y in range(miny-1, maxy+2):
        line = []
        for x in range(minx-1, maxx + 2):
            if x == 0 and y == 0:
                line.append("s")
            elif (x,y) in poses:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(line))

    for l in lines:
        print(l)

def adjust( frontloc, backloc ):
    backdelta = (0,0)
    if backloc[0] == frontloc[0]:
        if backloc[1] < frontloc[1] - 1:
            backdelta = ( 0, 1)
        elif backloc[1] > frontloc[1] + 1:
            backdelta = (0, -1)
        else:
            backdelta = (0, 0)
    elif backloc[1] == frontloc[1]:
        if backloc[0] < frontloc[0] - 1:
            backdelta = (1, 0)
        elif backloc[0] > frontloc[0] + 1:
            backdelta = (-1, 0)
        else:
            backdelta = (0,0)
    else:  # both different
        xdiff = frontloc[0] - backloc[0]
        ydiff = frontloc[1] - backloc[1]
        if abs(xdiff) > 1 or abs(ydiff) > 1:
            backdelta = ( -1 if xdiff < 0 else 1, -1 if ydiff < 0 else 1 )

    return ( backloc[0] + backdelta[0], backloc[1] + backdelta[1], )
        

def move( ropeloc, direction, steps, tailposes ):

    delta = dirs[direction]

    for i in range(0,steps):
        newropeloc = [ (ropeloc[0][0] + delta[0], ropeloc[0][1] + delta[1]) ]
        for rn in range(1,len(ropeloc)):
            newropeloc.append( adjust( newropeloc[-1], ropeloc[rn] ) )
        
        #print(f" {ropeloc} -> {newropeloc}")
        #printrope( newropeloc )

        tailposes.add( newropeloc[-1] )
        ropeloc = tuple(newropeloc)

    return ropeloc
                
    
if args.p1:
    print("Doing part 1")

    ropeloc = ( (0,0), (0,0), )

    tailposes = set([ (0,0) ] )
    for motion in data:
        ropeloc = move(ropeloc, motion[0], motion[1], tailposes)

    #printposes(tailposes)
        
    print(f"Rope Loc: {ropeloc}")
    print(f"Poses: {len(tailposes)}")

    
if args.p2:
    print("Doing part 2")

    ropeloc = ( (0,0), ) * 10

    tailposes = set([ (0,0) ] )
    for motion in data:
        ropeloc = move(ropeloc, motion[0], motion[1], tailposes)

    #printposes(tailposes)
        
    print(f"Rope Loc: {ropeloc}")
    print(f"Poses: {len(tailposes)}")
