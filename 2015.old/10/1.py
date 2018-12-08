#!/usr/bin/env python

import re

dataRe = re.compile("((.)\\2*)")

def lookAndSay(data):
    output=[]

    for x in re.findall(dataRe,data):
        m=x[0]
        output += ( "%i%s" % (len(m),m[0],), )
        
    return "".join(output)
        
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    l = line
    for x in range(0,51):
        print "%i: %i %s" % (x,len(l),l[:25] + "..." if len(l) > 25 else l,)
        l = lookAndSay(l)
        

