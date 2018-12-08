#!/usr/bin/env python

import re, itertools

lineRe = re.compile("(.+) (\\d+): (.+): (\\d+), (.+): (\\d+), (.+): (\\d+)")


sues = []

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue

    suenum = int(m.group(2))
    suevals = {}
    suevals["num"] = suenum
    suevals[m.group(3)] = int(m.group(4))
    suevals[m.group(5)] = int(m.group(6))
    suevals[m.group(7)] = int(m.group(8))

    sues.append(suevals)

desiredVals = {
    "children":3,
    "cats":7,
    "samoyeds":2,
    "pomeranians":3,
    "akitas":0,
    "vizslas":0,
    "goldfish":5,
    "trees":3,
    "cars":2,
    "perfumes":1,
    }

for sue in sues:
    match=True
    #print "Sue:%s" %(sue,)
    for key,val in desiredVals.iteritems():
        if sue.has_key(key):
            #print "Key: %s Has: %s val: %s desired: %s" % (key,sue.has_key(key),sue[key],val,)
            if sue[key] != val:
                #print "Mismatch on key: %s" % (key,)
                match=False
    if match:
        print "Part1: %s" % (sue,)
    

for sue in sues:
    match = True
    #print "Sue:%s" %(sue,)
    for key,val in desiredVals.iteritems():
        if sue.has_key(key):
            #print "  Key: %s Has: %s val: %s desired: %s" % (key,sue.has_key(key),sue[key],val,)
            if key == "cats" or key == "trees":
                if sue[key] <= val:
                    match = False
            elif key == "pomeranians" or key == "goldfish":
                if sue[key] >= val:
                    match = False
            else:
                if sue[key] != val:
                    match = False
            if not match:
                #print "  Mismatch on key: %s" % (key,)
                break
    if match:
        print "Part2: %s" % (sue,)
    
    
