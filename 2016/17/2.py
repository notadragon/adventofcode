#!/usr/bin/env python

import re, md5

code=open("input").readlines()[0].strip()
print code

openvals="bcdef"

def state(path):
    pcode = code + "".join(path[2:])
    m = md5.new()
    m.update(pcode)
    h = m.hexdigest()
    output = [h,]
    if path[1] > 0 and h[0] in openvals:
        output.append('U')
    if path[1] < 3 and h[1] in openvals:
        output.append('D')
    if path[0] > 0 and h[2] in openvals:
        output.append('L')
    if path[0] < 3 and h[3] in openvals:
        output.append('R')
    return output

deltas={ "U":(0,-1),
        "D":(0,1),
        "L":(-1,0),
        "R":(1,0),
      }

paths = [ (0,0) ]
finishpath = None
while paths:
    print "Steps: %s NumPaths:%s" % (len(paths[0]) - 2, len(paths),)
    for i in paths[0:5]:
        print "  %s - %s" % (i,state(i),)
    nextpaths = []
    for p in paths:
        dirs = state(p)
        for d in dirs[1:]:
            delta = deltas[d]
            nextp = ( p[0] + delta[0], p[1] + delta[1]) + p[2:] + (d,)

            if nextp[0] == 3 and nextp[1] == 3:
                finishpath = nextp
            else:
                nextpaths.append(nextp)
    paths = nextpaths

print "FinishPath:%s len:%s path:%s" % (finishpath,len(finishpath)-2,"".join(finishpath[2:]))
    
    
