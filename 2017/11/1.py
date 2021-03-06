#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

dirs=[]
for x in open(args.input).readlines():
    dirs = x.strip().split(',')

deltas = {"n":(0,2), "s":(0,-2), "ne":(1,1), "se":(1,-1), "nw":(-1,1), "sw":(-1,-1)}

def distance(loc):
    if loc[0] < 0 or loc[1] < 0:
        return distance( [abs(x) for x in loc] )

    vdelta = max(0,loc[1] - loc[0])
    return vdelta/2 + loc[0]

maxdistance = 0
loc = (0,0)
for d in dirs:
    delta = deltas[d]
    loc = (loc[0] + delta[0], loc[1] + delta[1])
    maxdistance = max(maxdistance,distance(loc))
    
print "Final loc: %s" % (loc,)

if args.p1:
    print "Doing part 1"

    print "  distance: %s" % (distance(loc),)

if args.p2:
    print "Doing part 2"

    print "  maxdistance: %s" % (maxdistance,)
