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

lineRe = re.compile("[0-9]*")

data = []


currdata = None
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))

    # Process input line
    if not x:
        if currdata:
            currdata = None
    else:
        if not currdata:
            currdata = []
            data.append(currdata)
        currdata.append(int(x.strip()))
        
#for d in data:
#    print(f"{d}")
        
if args.p1:
    print("Doing part 1")

    largest = 0
    for elf in data:
        elfcalories = sum(elf)
        if elfcalories > largest:
            largest = elfcalories
    print(f"{largest}")
    
if args.p2:
    print("Doing part 2")

    cals = [ sum(d) for d in data ]
    cals.sort()

    top3 = sum( cals[-3:] )
    print(f"{top3}")
    
