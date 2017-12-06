#!/usr/bin/env python

import re, itertools

lineRe = re.compile("[\\.#]+")

lights = []


for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue

    lights.append(line)

print "Starting:"
for line in lights:
    print line

def countneighbors(lights,i,j):
    output = 0
    for ioff in (-1,0,1):
        for joff in (-1,0,1):
            if ioff == 0 and joff == 0: continue
            i2=i+ioff
            j2=j+joff

            if i2 < 0: continue
            if j2 < 0: continue
            if i2 >= len(lights): continue
            if j2 >= len(lights[i2]): continue

            if lights[i2][j2] == "#":
                output += 1
    return output
            
            
def next(lights):
    output = []
    for i in range(0,len(lights)):
        outrow = []
        for j in range(0,len(lights[i])):
            current = lights[i][j]
            num = countneighbors(lights,i,j)

            if current == "#":
                if num == 2 or num == 3:
                    newval = "#"
                else:
                    newval = "."
            else:
                if num == 3:
                    newval = "#"
                else:
                    newval = "."
            outrow.append(newval)
            
        output.append("".join(outrow))
    return output

def breaklights(lights):
    lights[0] = "#" + lights[0][1:-1] + "#"
    lights[-1] = "#" + lights[-1][1:-1] + "#"
    return lights

def countlights(lights):
    output = 0
    for line in lights:
        for x in range(0,len(line)):
            if line[x] == "#":
                output += 1
    return output

l = breaklights(lights)
for step in range(0,100):
    l = breaklights(next(l))

print
print "Final:"
for line in l:
    print line

print "Count:%s" % (countlights(l),)
