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

lineRe = re.compile("(.*)\)(.*)")

vals = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals.append( (m.group(1),m.group(2),) )

#print("Vals: %s" % (vals,))

def getpath(orbits, p):
    output = [p,]
    while p in orbits:
        p = orbits[p]
        output.append(p)
    return output


if args.p1:
    print("Doing part 1")

    orbits = {}
    for a,b in vals:
        orbits[b] = a

    numorbits = 0
    for p in orbits.keys():
        numorbits += len(getpath(orbits,p))-1
    print("NumOrbits: %s" % (numorbits,))

if args.p2:
    print("Doing part 2")

    youpath = getpath(orbits,"YOU")
    sanpath = getpath(orbits,"SAN")

    while youpath[-1] == sanpath[-1]:
        del youpath[-1]
        del sanpath[-1]

    #print("YOU: %s" % (youpath,))
    #print("SAN: %s" % (sanpath,))

    print("Transfers: %s" % ( len(youpath)-1 + len(sanpath)-1, ) )
