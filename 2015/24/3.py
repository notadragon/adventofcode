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
    for i in range(0,len(items)):
        val = items[i]
        if val > total:
            break

        if val == total:
            unuseditems = items[0:i] + items[i+1:]
            yield ( (val,), unuseditems, )
        elif (maxlen > 1 or maxlen < 0):
            nextitems = items[i+1:]
            if not nextitems:
                continue

            previtems = items[0:i]
            
            for (a,b) in splitvals(total-val,maxlen-1,nextitems):
                yield ( a + (val,), previtems + b, )

def qe(g):
    out = 1
    for x in g:
        out *= x
    return out

def findSmallest(values,total):
    for x in itertools.count():
        out = []
        for v in splitvals(total,x,values):
            out.append( (qe(v[0]),) + v)
        if out:
            return out

def cansplit(values,subgroups,groupsum):
    if subgroups == 1:
        return sum(values) == groupsum
    
    for (g1,rest) in splitvals(groupsum,-1,values):
        if cansplit(rest,subgroups-1,groupsum):
            return True

    return False
        
for n in [3, 4]:
    svalues = list(values)
    svalues.sort()
    svalues.reverse()
    
    groupsum = sum(svalues)/n
    smallest = findSmallest(svalues,groupsum)
    smallest.sort()

    for (q,g1,rest) in smallest:
        if cansplit(rest,n-1,groupsum):
            print "N:%s QE:%s g1:%s rest: %s" % (n,q,g1,rest,)
            break
        
