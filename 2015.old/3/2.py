#!/usr/bin/env python

loc=(0,0,)
roboloc=(0,0,)
robo=0
delivered={}

delivered[loc] = 2

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
        
        if robo:
            roboloc=tuple(map(lambda x, y: x + y, roboloc, delta))
            l=roboloc
        else:
            loc=tuple(map(lambda x, y: x + y, loc, delta))
            l=loc
            
        minloc=tuple(map(min,l,minloc))
        maxloc=tuple(map(max,l,maxloc))
        
        prev=delivered.get(l,0)
        delivered[l]=prev+1
            
        print "In:%s delta:%s robo:%s loc:%s delivered:%s" % (c,delta,robo,l,prev+1,)

        if robo:
            robo = 0
        else:
            robo = 1
        
print "Min: %s Max: %s Final Loc:%s %s Houses:%s" % (minloc,maxloc,loc,roboloc,len(delivered),)
