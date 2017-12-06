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

line = open(args.input).readlines()[0]

ds = [ int(x) for x in line.strip() ]

if args.p1:
    sum =0
    for (a,n) in zip(ds,ds[1:] + ds):
        if a == n:
            sum += a
    print sum
    
if args.p2:
    sum = 0
    for (a,n) in zip(ds,ds[len(ds)/2:] + ds):
        if a == n:
            sum += a
    print sum
