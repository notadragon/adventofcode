#!/usr/bin/env python

loc=(0,0,)
delivered={}

delivered[loc] = 1

minloc=(0,0)
maxloc=(0,0)
for line in open("input").readlines():
    for c in line:
        if c == "^":
            delta=(0,1,)
        elif c == ">":
            delta=(1,0,)
        elif c == "v":
            delta=(0,-1,)
        elif c == "<":
            delta=(-1,0,)
        else:
            continue
        loc=tuple(map(lambda x, y: x + y, loc, delta))

        minloc=tuple(map(min,loc,minloc))
        maxloc=tuple(map(max,loc,maxloc))
        
        prev=delivered.get(loc,0)
        delivered[loc]=prev+1
            
        print "In:%s delta:%s loc:%s delivered:%s" % (c,delta,loc,prev+1,)

print "Min: %s Max: %s Final Loc:%s Houses:%s" % (minloc,maxloc,loc,len(delivered),)
