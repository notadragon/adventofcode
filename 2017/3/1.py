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

inputval = int(open(args.input).readlines()[0].strip())

print "Target val: %s" % (inputval,)

def spiral():
    yield (0,0)
    dist = 1
    while True:
        #(dist,-dist+1) to (dist,dist)
        for n in range(0,2*dist):
            yield (dist,-dist+1+n)
        #(dist-1,dist) to (-dist,dist)
        for n in range(0,2*dist):
            yield (dist-1-n,dist)
        #(-dist,dist-1) to (-dist,-dist)
        for n in range(0,2*dist):
            yield (-dist,dist-1-n)
        #(-dist+1,-dist) to (dist,-dist)
        for n in range(0,2*dist):
            yield(-dist+1+n,-dist)
        dist = dist+1
            
sp = spiral()
for i in range(0,25):
    print "i:%s loc:%s" %  (i+1,sp.next(),)

if args.p1:
    print "Doing part 1"
    
    loc = None
    sp = spiral()
    for i in xrange(0,inputval):
        ndx=i+1
        loc = sp.next()

    print "ndx: %s loc: %s" % (inputval,loc,)
    print "Dist: %s" % (abs(loc[0]) + abs(loc[1]))
    
if args.p2:
    print "Doing part 2"

    deltas = [ (x,y) for x in [-1,0,1] for y in [-1,0,1] if x != 0 or y != 0]
    sp = spiral()
        
    svals={}
    sval = 1
    svals[ sp.next() ] = sval
    
    while sval < inputval:
        loc = sp.next()
        sval = 0
        for d in deltas:
            dloc = tuple( map( sum, zip(loc,d)))
            sval += svals.get(dloc,0)
        svals[loc] = sval

    print "First bigger values:%s" % (sval,)
    
    
