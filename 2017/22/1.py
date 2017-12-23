#!/usr/bin/env pypy

import argparse, re

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

grid = []
for x in open(args.input).readlines():
    x = x.strip()

    if x:
        grid.append(x)

for x in grid:
    print x

right = {
    (-1,0): (0,1),
    (0,1):(1,0),
    (1,0):(0,-1),
    (0,-1):(-1,0),    
    }
left = {
    (0,1):(-1,0),
    (1,0):(0,1),
    (0,-1):(1,0),
    (-1,0):(0,-1),
    }

reverse = {
    (0,1):(0,-1),
    (0,-1):(0,1),
    (1,0):(-1,0),
    (-1,0):(1,0),
    }

if args.p1:
    print "Doing part 1"

    pos = (len(grid)/2,len(grid)/2)
    facing = (-1,0)
    infected = set([])
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j] == "#":
                infected.add( (i,j) )

    infections = 0
    cleans = 0
    for i in range(0,10000):
        #print "Iter: %s Infected: %s" % (i,infected,)
        if pos in infected:
            facing = right[facing]
            infected.remove(pos)
            cleans = cleans + 1
        else:
            facing = left[facing]
            infected.add(pos)
            infections = infections + 1
        pos = (pos[0] + facing[0], pos[1] + facing[1])


    print "Infections: %s cleans: %s" % (infections,cleans,)
            
if args.p2:
    print "Doing part 2"


    pos = (len(grid)/2,len(grid)/2)
    facing = (-1,0)
    infected = {}
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j] == "#":
                infected[ (i,j) ] = "I"

                
    infections = 0
    cleans = 0
    flags = 0
    weakens = 0
    for i in range(0,10000000):
        #print "Iter: %s Infected: %s" % (i,infected,)
        nstate = infected.get(pos,"C")
        if nstate == "C":
            facing = left[facing]
            infected[pos] = "W"
            weakens = weakens + 1
        elif nstate == "W":
            facing = facing
            infected[pos] = "I"
            infections = infections + 1
        elif nstate == "I":
            facing = right[facing]
            infected[pos] = "F"
            flags = flags + 1
        elif nstate == "F":
            facing = reverse[facing]
            infected[pos] = "C"
            cleans = cleans + 1
        pos = (pos[0] + facing[0], pos[1] + facing[1])


    print "Infections: %s flags: %s weakens: %s cleans: %s" % (infections,flags,weakens,cleans,)
