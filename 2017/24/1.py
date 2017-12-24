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

comps = []
lineRe = re.compile("(\d+)/(\d+)")
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
        continue

    comps.append( (int(m.group(1)),int(m.group(2)),) )

print "Comps: %s" % (comps,)

def dogenbridge(pcomps,usedcomps,inports):
    if not inports in pcomps:
        return

    for c in pcomps[inports]:
        if c in usedcomps:
            continue

        yield (c,)
        if inports == c[0]:
            nextports = c[1]
        else:
            nextports = c[0]

        usedcomps.add(c)
        for rest in dogenbridge(pcomps,usedcomps,nextports):
            yield (c,) + rest
        usedcomps.remove(c)

def genbridge(comps):
    pcomps = {}
    for c in comps:
        if c[0] in pcomps:
            pcomps[c[0]].add(c)
        else:
            pcomps[c[0]] = set([ c ])
        if c[1] in pcomps:
            pcomps[c[1]].add(c)
        else:
            pcomps[c[1]] = set([ c ])

    for x in dogenbridge(pcomps,set([]),0):
        yield x

def strength(br):
    return sum( sum(x) for x in br)

if args.p1:
    print "Doing part 1"

    bigbr = tuple()
    maxstr = 0
    for x in genbridge(comps):
        s = strength(x)
        if s > maxstr:
            maxstr = s
            bigbr = x
        #print "Bridge: %s str %s" % (x,s,)
        
    print "Bridge: %s Str: %s" % (bigbr,maxstr,)


    
if args.p2:
    print "Doing part 2"

    bigbr = tuple()
    maxstr = 0
    for x in genbridge(comps):
        if len(x) > len(bigbr):
            bigbr = x
            maxstr = strength(x)
            continue
        s = strength(x)
        if s > maxstr:
            maxstr = s
            bigbr = x
        #print "Bridge: %s str %s" % (x,s,)
        
    print "Bridge: %s Str: %s" % (bigbr,maxstr,)
