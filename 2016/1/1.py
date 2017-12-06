#!/usr/bin/env python

loc=(0,0)
facing=(0,1)

visitted = {}
visitted[(0,0)] = 1

print "%s %s %s %s" % ("", loc, facing, abs(loc[0]) + abs(loc[1]))

for x in open("input").readlines()[0].split(','):
    x=x.strip()

    if x[0] == "L":
        facing = ( -1 * facing[1], facing[0] )        
    elif x[0] == "R":
        facing = ( facing[1], -1 * facing[0] )

    distance=int(x[1:])
    loc = ( loc[0] + distance * facing[0], loc[1] + distance * facing[1], )

    if visitted.has_key(loc):
        visitted[loc]+=1
    else:
        visitted[loc]=1
    
    print "%s %s %s %s c:%s" % (x, loc, facing, abs(loc[0]) + abs(loc[1]), visitted[loc],)

    if visitted[loc] > 1:
        break
