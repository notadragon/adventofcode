#!/usr/bin/env python

import re, md5, itertools

layout = [ l.strip() for l in open("input").readlines() ]

locs = []
for y in range(0,len(layout)):
    r = layout[y]
    for x in range(0,len(r)):
        c = r[x]
        if c in "0123456789":
            i = int(c)
            while len(locs) <= i:
                locs.append(0)
            locs[i] = (x,y)

def distance(f,t):
    found = { f:0 }
    ends = [f]
    step = 0
    while ends and not found.has_key(t):
        nextends = []
        for e in ends:
            for dx,dy in [ (-1,0), (1,0), (0,-1), (0,1) ]:
                n = (e[0] + dx, e[1] + dy)
                if found.has_key(n):
                    continue
                if layout[n[1]][n[0]] != "#":
                    nextends.append(n)
                    found[n] = step+1
        step = step + 1
        ends = nextends
    return step
            
for i in range(0,len(locs)):
    print " %s -> %s" % (i,locs[i],)

distances = {}
for f in range(0,len(locs)):
    for t in range(f+1,len(locs)):
        d = distance(locs[f],locs[t])

        distances[ (f,t) ] = d
        distances[ (t,f) ] = d
        
        print "%s: %s" % ( (f,t,), d,)

minsteps = -1
        
for p in itertools.permutations(range(1,len(locs))):
    d = 0
    ds = []
    for i in range(0,len(p)+1):
        if i == 0:
            nd = distances[ (0,p[i]) ]
        elif i == len(p):
            nd = distances[ (p[i-1],0) ]
        else:
            nd = distances[ ( p[i-1], p[i], ) ]
        d = d + nd
        ds.append(nd)

    if minsteps < 0 or d < minsteps:
        minsteps = d
        
    print "%s -> %s = %s" % ((0,) + p,ds,d,)

print "Min steps: %s" % (minsteps,)
