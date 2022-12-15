#!/usr/bin/env pypy3

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue

    # Process input line
    data.append( ( (int(m.group(1)), int(m.group(2))), (int(m.group(3)),int(m.group(4))), ) )

#for d in data:
#    print(f"{d}")

def printgrid(grid):
    minx = min(g[0] for g in grid.keys())
    miny = min(g[1] for g in grid.keys())
    maxx = max(g[0] for g in grid.keys())
    maxy = max(g[1] for g in grid.keys())

    numlines = []
    for x in range(minx,maxx+1):
        if x == minx or x == maxx or (x % 10 == 0):
            xs = f"{x}"
            while len(numlines) < len(xs):
                numlines.append([" " * 4])
            for n,c in enumerate(xs):
                numlines[n].append(c)
            for n in range(len(xs),len(numlines)):
                numlines[n].append(" ")
        else:
            for l in numlines:
                l.append(" ")
        
    for l in numlines:
        print("".join(l))
    
    for y in range(miny,maxy+1):
        line = [f"{y:3} "]
        for x in range(minx,maxx+1):
            if (x,y) in grid:
                line.append(grid[ (x,y) ])
            else:
                line.append(".")
        print("".join(line))


def emptyintervals(data, row, coordrange = None):
    intervals = []
    for s,b in data:
        sbdist = abs(b[0] - s[0]) + abs(b[1] - s[1])
        srdist = abs(row - s[1])
        if srdist < sbdist:
            iwidth = sbdist - srdist
            cint = (s[0] - iwidth, s[0] + iwidth )
            if coordrange != None:
                cint = ( max(cint[0], coordrange[0]), min(cint[1], coordrange[1]), )
                if cint[1] < cint[0]:
                    continue
            #print(f"{s} -> {b} dist {sbdist} covers {cint} in {row} which is {srdist} away")
            intervals.append( cint )
    intervals.sort()
    #print(f"{intervals}")

    newintervals = [ intervals[0] ]
    for i in intervals[1:]:
        last = newintervals[-1]
        if i[0] <= last[1] +1:
            newintervals[-1] = ( min(i[0], last[0]), max(i[1],last[1]), )
        else:
            newintervals.append(i)

    #print(f"{newintervals}")
    return newintervals

def intervalssize(intervals):
    total = 0
    for i in intervals:
        total = total + (i[-1] - i[0] )
    return total
    
if args.p1:
    print("Doing part 1")

    grid = {}
    for s,b in data:
        grid[s] = "S"
        grid[b] = "B"

    #printgrid(grid)

    if args.input == "sample":
        trow = 10
    else:
        trow = 2000000
        
    rintervals = emptyintervals(data, trow)
    covered = intervalssize(rintervals)
    print(f"Covered spaces in row {trow}: {covered}")
    
    
if args.p2:
    print("Doing part 2")

    def tuningfrequency(loc):
        return loc[0] * 4000000 + y

    if args.input == "sample":
        coordrange = ( 0, 20 )
    else:
        coordrange = ( 0, 4000000 )

    for y in range(*coordrange):
        covered = emptyintervals(data,y,coordrange)
        if len(covered) != 1 or covered[0] != coordrange:
            covered.insert(0, (coordrange[0]-1,coordrange[0]-1))
            covered.append( (coordrange[1]+1, coordrange[1]+1) )
            for i in range(0,len(covered)-1):
                for x in range( covered[i][1]+1, covered[i+1][0] ):
                    print(f"Uncovered: {x,y}")
                    freq = tuningfrequency( (x,y) )
                    print(f"Frequency: {freq}")
