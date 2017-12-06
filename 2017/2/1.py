#!/usr/bin/env python

import argparse,re

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

allvals=[]
for x in open(args.input).readlines():
    x = x.strip()
    vals = [int(y) for y in x.split() if y]
    allvals.append(vals)

if args.p1:
    print "Doing part 1"
    sum = 0
    for vals in allvals:
        sum += max(vals) - min(vals)
    print sum

if args.p2:
    print "Doing part 2"

    sum = 0
    for vals in allvals:
        for x in vals:
            for y in vals:
                if x != y and x % y == 0:
                    sum += x / y
    print sum
