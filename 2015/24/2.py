#!/usr/bin/env python

import re, itertools, math, sys

lineRe = re.compile("\\d+")

values = []
        
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    values.append(int(line))

total = sum(values)

print "Values:%s Total:%s" % (values,total,)

def splitvals( total, maxlen, items ):
    if maxlen == 0:
        return
    
    #print "Total:%s Items: %s" % (total,items, )
    for i in range(len(items)-1,-1,-1):
        val = items[i]
        if val > total:
            continue

        if val == total:
            unuseditems = items[0:i] + items[i+1:]
            yield ( (val,), unuseditems, )
        elif i > 0 and (maxlen > 1 or maxlen < 0):

            previtems = items[0:i]

            nextitems = items[i+1:]
            
            for (a,b) in splitvals(total-val,maxlen-1,previtems):
                yield ( (val,) + a, b + nextitems, )

def findgroups(values):
    grouptotal = sum(values)/4

    smallestlen = -1

    for (g1,r1) in splitvals(grouptotal,smallestlen,values):
        g1l = len(g1)
        if smallestlen < 0:
            smallestlen = g1l
        elif smallestlen < g1l:
            continue
        elif g1l < smallestlen:
            groupings = []
            smallestlen = g1l        

        found = False
        for (g2,r2) in splitvals(grouptotal,-1,r1):
            for (g3,r3) in splitvals(grouptotal,-1,r2):
                found = True
                yield (g1,g2,g3,r3,)
                break
            if found:
                break

def qe(g):
    out = 1
    for x in g:
        out *= x
    return out

smallestgroup = None
numgroupings = 0
smallestlen = -1
smallestqe = -1
for grouping in findgroups(values):
    numgroupings += 1

    if sum(grouping[0]) != sum(grouping[1]):
        print "Invalid Grouping sum: %s" % (grouping,)
    if sum(grouping[0]) != sum(grouping[2]):
        print "Invalid Grouping sum: %s" % (grouping,)
    if sum(grouping[0]) != sum(grouping[3]):
        print "Invalid Grouping sum: %s" % (grouping,)

    if sum( [ len(x) for x in grouping ] ) != len(values):
        print "Invalid number of items: %s" % (grouping,)
        
    g1l = len(grouping[0])
    if smallestlen < 0:
        smallestgroup = grouping
        smallestlen = g1l
        smallestqe = qe(grouping[0])

        print "Grouping: %s len: %s qe: %s" % (grouping,smallestlen,smallestqe,)
    elif smallestlen > g1l:
        continue
    elif g1l < smallestlen:
        smallestgroup = grouping
        smallestlen = g1l
        smallestqe = qe(grouping[0])

        print "Grouping: %s len: %s qe: %s" % (grouping,smallestlen,smallestqe,)
    elif g1l == smallestlen:
        gqe = qe(grouping[0])
        if gqe < smallestqe:
            smallestgroup = grouping
            smallestqe = gqe
            print "Grouping: %s len: %s qe: %s" % (grouping,smallestlen,smallestqe,)
        

    
print "Groupings found: %s" % (numgroupings,)
