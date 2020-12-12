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

lineRe = re.compile("([NSEWLRF])([0-9]+)")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (m.group(1),int(m.group(2)),))

if args.p1:
    print("Doing part 1")


    dirs = { "N" : (0,-1),
             "W" : (-1,0),
             "E" : (1,0),
             "S" : (0,1), }
             
    rots = { "L" : lambda x : ( x[1], -x[0] ) ,
             "R" : lambda x : ( -x[1], x[0] ) }

    loc = (0,0)
    facing = dirs["E"]

    for step in data:
        stepdir = None
        if step[0] in dirs:
            stepdir = dirs[step[0]]
        elif step[0] == "F":
            stepdir = facing
        elif step[0] in rots:
            degrees = 0
            steprot = rots[step[0]]
            while degrees < step[1]:
                facing = steprot(facing)
                degrees += 90
        if stepdir:
            loc = ( loc[0] + step[1] * stepdir[0],
                    loc[1] + step[1] * stepdir[1] )

        #print("Action: %s Loc: %s/%s" % (step,facing,loc,))

    print("Final Loc: %s (%s)" % (loc, sum([ abs(x) for x in loc ]),))
    
if args.p2:
    print("Doing part 2")

    dirs = { "N" : (0,-1),
             "W" : (-1,0),
             "E" : (1,0),
             "S" : (0,1), }
             
    rots = { "L" : lambda x : ( x[1], -x[0] ) ,
             "R" : lambda x : ( -x[1], x[0] ) }

    loc = (0,0)
    waypoint = (10,-1)
    facing = dirs["E"]

    for step in data:
        if step[0] in dirs:
            stepdir = dirs[step[0]]
            waypoint = ( waypoint[0] + step[1] * stepdir[0],
                         waypoint[1] + step[1] * stepdir[1], )
        elif step[0] in rots:
            wpdelta = ( waypoint[0] - loc[0], waypoint[1] - loc[1])
            steprot = rots[step[0]]

            degrees = 0
            while degrees < step[1]:
                wpdelta = steprot(wpdelta)
                degrees += 90
            waypoint = ( loc[0] + wpdelta[0], loc[1] + wpdelta[1], )            
        elif step[0] == "F":
            wpdelta = ( waypoint[0] - loc[0], waypoint[1] - loc[1])
            loc = ( loc[0] + step[1] * wpdelta[0],
                    loc[1] + step[1] * wpdelta[1], )
            waypoint = ( waypoint[0] + step[1] * wpdelta[0],
                         waypoint[1] + step[1] * wpdelta[1], )
                         
    
        #print("Action: %s Loc: %s/%s" % (step,waypoint,loc,))

    print("Final Loc: %s (%s)" % (loc, sum([ abs(x) for x in loc ]),))
