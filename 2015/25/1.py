#!/usr/bin/env python

import re, itertools, math, sys

lineRe = re.compile("To continue, please consult the code grid in the manual.  Enter the code at row (\\d+), column (\\d+).")

        
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    row = int(m.group(1))
    col = int(m.group(2))

print "Row:%s col:%s" % (row,col,)

startingval = 20151125

def nextcode(x):
    return x * 252533 % 33554393

def codes():
    prev = startingval

    while True:
        yield prev
        prev = nextcode(prev)


grid = []

currow = 1
curcol = 1

for x in codes():
    if currow <= 6 and curcol <= 6:
        while len(grid) < currow:
            grid.append([])
        grid[currow-1].append( (currow,curcol,x,) )

    if currow == row and curcol == col:
        print "%s,%s = %s" % (currow,curcol,x,)
        break

    curcol += 1
    currow -= 1

    if currow == 0:
        currow = curcol
        curcol = 1
    
print "Grid: %s" % (grid,)

    
