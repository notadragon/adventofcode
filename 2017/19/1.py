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

maze = []

nextdirs = {
    (0,1):[(0,1),(1,0),(-1,0)],
    (0,-1):[(0,-1),(-1,0),(1,0)],
    (1,0):[(1,0),(0,1),(0,-1)],
    (-1,0):[(-1,0),(0,-1),(0,1)],

    }

for x in open(args.input).readlines():
    x = x.strip("\n")

    maze.append(x)

if args.p1 or args.p2:
    print "Doing part 1"

    loc = (0,maze[0].index("|"))
    dir = (1,0)


    steps = 1
    letters = []
    while True:
        #print "loc: %s dir: %s" % (loc,dir,)

        found = False
        for nextdir in nextdirs[dir]:
            nextloc = (loc[0] + nextdir[0], loc[1] + nextdir[1])
            if nextloc[0] >= 0 and nextloc[0] < len(maze) and nextloc[1] >= 0 and nextloc[1] < len(maze[nextloc[0]]):
                nextval = maze[nextloc[0]][nextloc[1]]

                #print "nextloc: %s nextval: %s" % (nextloc,nextval,)
                
                if nextval == " ":
                    continue

                if nextval != '|' and nextval != '+' and nextval != '-':
                    print "Letter: :%s" % (nextval,)
                    letters.append(nextval)
                found = True
                loc = nextloc
                dir = nextdir
                steps = steps + 1
                break

        if not found:
            break

    print "Letters: %s" % ( "".join(letters),)
    print "Steps: %s" % (steps,)
    
if args.p2:
    print "Doing part 2"
