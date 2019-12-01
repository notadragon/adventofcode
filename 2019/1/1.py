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

lineRe = re.compile("\d+")
vals = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals.append(int(x))

print("Vals %s" % (vals,))

def fuel(x):
    return max(0,(x // 3) - 2)

if args.p1:
    print("Doing part 1")

    fuels = [ fuel(x) for x in vals ]

    print("Fuels: %s" % (fuels,))

    print("Total Fuel %s" % (sum(fuels),))

def fullfuel(x):
    output = 0
    while x > 0:
        f = fuel(x)
        output += f
        x = f
    return output

if args.p2:
    print("Doing part 2")


    fullfuels = [ fullfuel(x) for x in vals ]

    print("FullFuels %s" % (fullfuels,))

    print("Total Fuel: %s" % (sum(fullfuels),))
