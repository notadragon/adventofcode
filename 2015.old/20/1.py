#!/usr/bin/env python

import re, itertools, math

lineRe = re.compile("(\\d+)")

puzzle = None

def total(x):
    total = 0
    end=int(math.floor(math.sqrt(x)))
    for i in range(1,end+1):
        if x % i == 0:
            total += (i*10)
            iv = x/i
            if i != iv:
                total += (iv*10)
    return total

def findHouse(y):
    for x in itertools.count():
        xval = total(x)
        if xval >= y:
            return (x,xval)

def findHouse2(y):
    for x in itertools.count():
        xval = total2(x)
        if xval >= y:
            return (x,xval)

def total2(x):
    total = 0
    minval = x/50
    
    end=int(math.floor(math.sqrt(x)))
    for i in range(1,end+1):
        if x % i == 0:
            iv = x/i

            if i*50 >= x:
                total += (iv*11)
            if i != iv and i <= 50:
                total += (iv*11)

    return total

#for x in itertools.count():
    #print "House %d got %d presents" % (x,total(x),)
    #print "House %d got %d presents" % (x,total2(x),)

        
for line in open("input").readlines():
    line = line.strip();
    if not line: continue
    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    #print "House %d got %d presents" % findHouse(int(line))
    print "House %d got %d presents" % findHouse2(int(line))



    
