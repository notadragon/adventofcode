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

allvals = []
for l in open(args.input).readlines():
    vals = [x.strip() for x in l.split()]
    allvals.append(vals)

def valid(pp):
    s = set()
    for p in pp:
        if p in s:
            return False
        s.add(p)
    return True

if args.p1:
    print "Doing part 1"

    sum = 0
    for pp in allvals:
        if valid(pp):
            sum += 1
    print sum

def valid2(pp):
    s = set()
    for p in pp:
        p = tuple(sorted(p))
        if p in s:
            return False
        s.add(p)
    return True
    
if args.p2:
    print "Doing part 2"

    sum = 0
    for pp in allvals:
        if valid2(pp):
            sum += 1
    print sum

    
