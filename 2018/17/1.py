#!/usr/bin/env pypy

import argparse, re

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

lineRe = re.compile("(x|y)=([0-9]+), (x|y)=([0-9]+)\\.\\.([0-9]+)")

clayranges = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1) == "x":
        clayranges.append( ( int(m.group(2)), int(m.group(2))+1, int(m.group(4)), int(m.group(5))+1, "#", ) )
    else:
        clayranges.append( ( int(m.group(4)), int(m.group(5))+1, int(m.group(2)), int(m.group(2))+1, "#", ) )

#for r in clayranges:
#    print("r: %s" % (r,))

if True:
    print("Doing part 1")

    minx = min( [ c[0] for c in clayranges ] ) -1
    maxx = max( [ c[1] for c in clayranges ] ) +1
    miny = min( [ c[2] for c in clayranges ] )
    maxy = max( [ c[3] for c in clayranges ] )
    print(" X: %s -> %s  Y: %s -> %s" % (minx,maxx,miny,maxy,))


def show(grid):
    for y in range(miny,maxy):
        print("%4s %s" % (y,"".join(grid[y-miny]),))

def showdiff(g1,g2):
    for y in range(miny,maxy):
        g1r = g1[y-miny]
        g2r = g2[y-miny]

        d = False
        for x in range(minx,maxx):
            if (g1r[x-minx] == "#") != (g2r[x-minx] == "#"):
                d = True
                break
        
        if d:
            print("%4s %s" % (y,"".join(g1[y-miny]),))
            print("%4s %s" % (y,"".join(g2[y-miny]),))
        
def getval(grid,x,y):
    if x < minx or x >= maxx or y < miny or y >= maxy:
        return " "
    else:
        return grid[y-miny][x-minx]

def setval(grid,x,y,v):
    if x < minx or x >= maxx or y < miny or y >= maxy or v == grid[y-miny][x-minx]:
        return 0
    grid[y-miny][x-minx] = v
    return 1

def checkbasin(grid,waterlocs,w):
    #print("CheckBasin: %s" % (w,))
    
    rightx = w[0]
    leftx = w[0]
    while True:
        leftval = getval(grid,leftx-1,w[1])
        #print("%s,%s left: %s below: %s" % (leftx,w[1],leftval,belowval,))
        if leftval in " ":
            return 0
        if leftval in "#~":
            break
        belowval = getval(grid,leftx-1,w[1]+1)
        if not belowval in "~#":
            return 0
        leftx = leftx - 1

    #print("Basin! %s,%s -> %s,%s" % (leftx,w[1],rightx,w[1],))
    out = 0
    for i in range(leftx,rightx+1):
        if getval(grid,i,w[1]) not in "~|":
            print("Invalid current value: %s,%s = %s" % (i,w[1],getval(grid,i,w[1]),))
        
        out += setval(grid,i,w[1],"~")
        waterlocs.discard( (i,w[1],) )

        aboveval = getval(grid,i,w[1]-1)
        if aboveval == "|":
            waterlocs.add( (i,w[1]-1,))
    return out

def flowwater(grid,waterlocs):
    out = 0
    for w in list(waterlocs):
        valat = getval(grid,w[0],w[1])
        if valat == " ":
            out += setval(grid,w[0],w[1],"|")
            continue

        valbelow = getval(grid,w[0],w[1]+1)

        if valbelow == " ":
            if w[1] < maxy-1:
                waterlocs.add( (w[0],w[1]+1) )
                waterlocs.discard(w)
                out = out + 1
            continue
        elif valbelow in "#~":
            leftloc = (w[0]-1,w[1])
            leftval = getval(grid,leftloc[0],leftloc[1])
            rightloc = (w[0]+1,w[1])
            rightval = getval(grid,rightloc[0],rightloc[1])

            if leftval == " ":
                waterlocs.add(leftloc)
                out = out + 1
            if rightval == " ":
                waterlocs.add(rightloc)
                out = out + 1
            if rightval in "~#":
                out += checkbasin(grid,waterlocs,w)
            else:
                waterlocs.discard(w)
                    
    return out
    

def initGrid():
    grid = [ [ " " for x in range(minx,maxx) ] for y in range(miny,maxy) ]

    for c in clayranges:
        for y in range(c[2],c[3]):
            for x in range(c[0],c[1]):
                grid[y-miny][x-minx] = c[4]

    return grid

if True:
    grid = initGrid()
    #show(grid)

    waterlocs = set([ (500,max(0,miny)) ])
    while True:
        flowed = flowwater(grid,waterlocs)
        #show(grid)
        #print("Water: %s Flowed: %s" % (waterlocs,flowed,))
        if not flowed:
            break
    #show(grid)

    #showdiff(initGrid(),grid)

if args.p1:
    print("Doing part 1")

    waterlocs = sum([ sum([ 1 for c in g if c in "|~" ]) for g in grid ])
    print("Water Total: %s" % (waterlocs,))
    
if args.p2:
    print("Doing part 2")

    waterlocs = sum([ sum([ 1 for c in g if c in "~" ]) for g in grid ])
    print("Still Water Total: %s" % (waterlocs,))
