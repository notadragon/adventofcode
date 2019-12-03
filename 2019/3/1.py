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

lineRe = re.compile("[LRUD]\d+(,[LRUD]\d+)*")

vals = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals.append(x.split(","))

print("Vals: %s" % (vals,))

dirs = { "U" : (0,1),
         "R" : (1,0),
         "L" : (-1,0),
         "D" : (0,-1),
         }

def makegrid(vals):
    output = set()
    pos = (0,0)
    for i in vals:
        d = dirs[i[0]]
        for r in range(0,int(i[1:])):
            pos = (pos[0] + d[0], pos[1] + d[1],)
            output.add(pos)
    return output

if args.p1:
    print("Doing part 1")

    poses = (makegrid(vals[0]) , makegrid(vals[1]), )

    intersections = poses[0].intersection(poses[1])
    print("Intersections: %s" % (intersections,))
    mindist = min( [ abs(p[0]) + abs(p[1]) for p in intersections] )
    print("Min: %s" % (mindist,))
    
def makegrid2(vals):
    output = {}
    pos = (0,0)
    step = 0
    for i in vals:
        d = dirs[i[0]]
        for r in range(0,int(i[1:])):
            pos = (pos[0] + d[0], pos[1] + d[1],)
            step = step + 1
            if pos not in output:
                output[pos] = step
    return output

if args.p2:
    print("Doing part 2")

    steps = (makegrid2(vals[0]) , makegrid2(vals[1]), )
    poses = (makegrid(vals[0]) , makegrid(vals[1]), )

    intersections = poses[0].intersection(poses[1])

    minsteps = min( [ steps[0][p] + steps[1][p] for p in intersections ] )

    print("MinSteps: %s" % (minsteps,))
    
