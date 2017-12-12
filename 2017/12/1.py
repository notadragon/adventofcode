#!/usr/bin/env python

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

lineRe = re.compile("(\\d+) \<-\> (\\d+(?:, \\d+)*)")
pipes = {}
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
    else:
        pipes[int(m.group(1))] = [ int(v.strip()) for v in m.group(2).split(",") ]

print " pipes %s" % (len(pipes),)

def complete(vs):
    tocomplete = list(vs)

    while tocomplete:
        x = tocomplete.pop()
        for c in pipes[x]:
            if c in vs:
                continue
            vs.add(c)
            tocomplete.append(c)

    
if args.p1:
    print "Doing part 1"
    
    zeroset = set([0])
    complete(zeroset)
    print "Zeroset: %s" % (zeroset,)
    print "Size: %s" % (len(zeroset),)

if args.p2:
    print "Doing part 2"

    all = set(pipes.keys())
    subsets = []
    while all:
        init = all.pop()
        subset = set([init])
        complete(subset)

        subsets.append(subset)
        all.difference_update(subset)

    print "Subsets: %s" % (len(subsets),)
