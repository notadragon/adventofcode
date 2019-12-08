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

lineRe = re.compile("[0-2]*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals = [int(c) for c in x]

#print("Vals: %s" % (vals,))

if args.p1:
    print("Doing part 1")

    width = 25
    height = 6
    step = width * height

    flatlayers = [ vals[i:i+step] for i in range(0,len(vals),step) ]

    minz = None
    minl = None
    for l in flatlayers:
        lz = len([c for c in l if c == 0])
        if minz == None or lz < minz:
            minz = lz
            minl = l

    print
    print("Minz: %s" % (minz,))
    print("Minl: %s:%s" % (len(minl),minl,))

    ones = len([c for c in minl if c == 1])
    twos = len([c for c in minl if c == 2])
    print("Ones: %s Twos: %s Product: %s" % (ones, twos, ones*twos,))
    
if args.p2:
    print("Doing part 2")

    width = 25
    height = 6
    step = width * height

    flatlayers = [ vals[i:i+step] for i in range(0,len(vals),step) ]
    layers = [ [ l[i:i+width] for i in range(0,len(l),width)] for l in flatlayers ]

    outlayers = []
    for i in range(0,height):
        outlayers.append( [2]*width )

    for l in layers:
        for x,y in itertools.product(range(0,height),range(0,width)):
            if outlayers[x][y] == 2:
                outlayers[x][y] = l[x][y]
    
    for l in outlayers:
        ll = []
        for c in l:
            if c == 0:
                ll.append(" ")
            else:
                ll.append("X")
                
        print("".join( ll))
