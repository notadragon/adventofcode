#!/usr/bin/env python

import re

lineRe = re.compile("(.*) to (.*) = (\\d+)")

cities = set()
distances = {}

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue

    fromLoc=m.group(1)
    toLoc=m.group(2)
    distance=int(m.group(3))
    
    cities.add(fromLoc)
    cities.add(toLoc)
    distances[(fromLoc,toLoc)] = distance
    distances[(toLoc,fromLoc)] = distance



print "Cities: %s" % (cities,)

def minDistance(cities,path):
    if len(path) == len(cities):
        return path

    shortest = None
    shortestLength = 0
    
    for city in cities:
        if city in path:
            continue
        candidate = minDistance(cities,path + (city,))
        candidateLength = distance(candidate)
        if not shortest or candidateLength < shortestLength:
            shortest = candidate
            shortestLength = candidateLength

    return shortest

def maxDistance(cities,path):
    if len(path) == len(cities):
        return path

    longest = None
    longestLength = 0
    
    for city in cities:
        if city in path:
            continue
        candidate = maxDistance(cities,path + (city,))
        candidateLength = distance(candidate)
        if not longest or candidateLength > longestLength:
            longest = candidate
            longestLength = candidateLength

    return longest
        
def distance(path):
    total = 0
    prev = None
    for p in path:
        if prev:
            total = total + distances[(prev,p)]
        prev = p
    return total
        
minPath = minDistance(cities,())
print "MinPath: %s  Distance: %s" % (minPath,distance(minPath),)

maxPath = maxDistance(cities,())
print "MaxPath: %s  Distance: %s" % (minPath,distance(maxPath),)
