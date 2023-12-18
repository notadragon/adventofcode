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

lineRe = re.compile("^([DLUR]) ([0-9]+) \(\#([0-9a-f]+)\)$")

data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( ( m.group(1), int(m.group(2)), m.group(3), ) )

#for d in data:
#    print(f"{d}")

deltas = {
    "U" : (0,-1),
    "D" : (0,1),
    "L" : (-1,0),
    "R" : ( 1,0),
    }

def show(colors):
    minx = min( l[0] for l in colors.keys() )
    maxx = max( l[0] for l in colors.keys() )
    miny = min( l[1] for l in colors.keys() )
    maxy = max( l[1] for l in colors.keys() )

    for y in range(miny, maxy+1):
        row = []
        for x in range(minx,maxx+1):
            if (x,y) in colors:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))
        
def rundata(data, p2):
    loc = (0,0)
    rects = set()
    for d, s, c in data:
        if p2:
            if c[-1] == "0":
                d = "R"
            elif c[-1] == "1":
                d = "D"
            elif c[-1] == "2":
                d = "L"
            else:
                d = "U"
            s = int(c[0:-1],16)

        delta = deltas[d]
        endloc = ( loc[0] + s * delta[0], loc[1] + s * delta[1])
        rect = ( min(loc[0], endloc[0]), min(loc[1], endloc[1]),
                 max(loc[0], endloc[0])+1, max(loc[1], endloc[1])+1 )
        

        rects.add(rect)
        loc = endloc

    #colors = {}
    #for r in rects:
    #    for x in range(r[0], r[2]):
    #        for y in range(r[1], r[3] ):
    #            colors[ (x,y) ] = 1
    #show(colors)

    xvals = set()
    yvals = set()
    for d in (-1,0,1):
        xvals.update( r[0] + d for r in rects )
        xvals.update( r[2]-1 + d for r in rects )
        yvals.update( r[1] + d for r in rects )
        yvals.update( r[3]-1 + d for r in rects )

    xvals = list(xvals)
    xvals.sort()

    yvals = list(yvals)
    yvals.sort()

    #print(f"Xvals: {xvals}")
    #print(f"Yvals: {yvals}")

    splitrects = set()
    for r in rects:
        #print(f"  Rect: {r}")
        xs = [ x for x in xvals if x >= r[0] and x <= r[2] ]
        ys = [ y for y in yvals if y >= r[1] and y <= r[3] ]
        #print(f"     -> {xs} * {ys}")

        for (minx, maxx) in zip( xs[0:-1], xs[1:] ):
            for (miny, maxy) in zip( ys[0:-1], ys[1:] ):
                splitrects.add( (minx, miny, maxx, maxy) )

    #colors = {}
    #for r in splitrects:
    #    for x in range(r[0], r[2]):
    #        for y in range(r[1], r[3] ):
    #            colors[ (x,y) ] = 1
    #show(colors)

    def rectsize(rs):
        total = 0
        for r in rs:
            total = total + ( r[2] - r[0] ) * ( r[3] - r[1] )
        return total

    insiderects = set()
    outsiderects = set()

    rectgrid = {}

    for xr in range(0,len(xvals)-1):
        for yr in range(0,len(yvals)-1):
            r = ( xvals[xr], yvals[yr], xvals[xr+1], yvals[yr+1] )

            rectgrid[ (xr, yr) ] = r


    insiderects = set()
    outsiderects = set()
    
    for gloc, r in rectgrid.items():
        if r in insiderects or r in outsiderects or r in splitrects:
            continue

        tosearch = collections.deque()
        tosearch.append(gloc)

        found = set()
        outside = False
        
        while tosearch:
            l = tosearch.popleft();
            if not l in rectgrid:
                outside = True
                continue

            lr = rectgrid[l]
            if lr in outsiderects:
                outside = True
                continue
            
            if lr in found or lr in splitrects or lr in insiderects:
                continue
            
            found.add(lr)
            for d in deltas.values():
                dl = ( l[0] + d[0], l[1] + d[1] )
                tosearch.append( dl )

        if outside:
            outsiderects.update(found)
        else:
            insiderects.update(found)

    print(f"Border size: {rectsize(splitrects)}")

    print(f"Inside size: {rectsize(insiderects)}")
    print(f"Lake size: {rectsize(splitrects) + rectsize(insiderects)}")
    #show(colors)
    #print(f"Filled Size: {len(colors)}")
    


    
if args.p1:
    print("Doing part 1")

    rundata(data, False);
    
if args.p2:
    print("Doing part 2")

    rundata(data, True);
    
