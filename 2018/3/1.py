#!/usr/bin/env python3

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
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")

elves = {}

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    elves[int(m.group(1)) ] = ( (int(m.group(2)),int(m.group(3)),), (int(m.group(4)),int(m.group(5)),), )

    
if args.p1:
    print("Doing part 1")

    claims = {}
    for estat in elves.values():
        ((x,y),(w,h)) = estat
        for i in range(0,w):
            for j in range(0,h):
                loc = (x+i,y+j)
                if loc in claims:
                    claims[loc]+= 1
                else:
                    claims[loc] = 1

    mclaim = 0
    for ctotal in claims.values():
        if ctotal > 1:
            mclaim += 1
    print("Duplicate claims:%s" % (mclaim,))
    
if args.p2:
    print("Doing part 2")

    claims = {}
    for elf,estat in elves.items():
        ((x,y),(w,h)) = estat
        for i in range(0,w):
            for j in range(0,h):
                loc = (x+i,y+j)
                if not loc in claims:
                    claims[loc] = set()
                claims[loc].add(elf)

    nonoverlap = set(elves.keys())
    for cstats in claims.values():
        if len(cstats) > 1:
            for c in cstats:
                nonoverlap.discard(c)

    print("NonOverlapping:%s" % (nonoverlap,))
