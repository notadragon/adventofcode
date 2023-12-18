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

if args.p1:
    print("Doing part 1")

    loc = (0,0)
    colors = { loc : "#000000" }

    for d, s, c in data:
        delta = deltas[d]
        for i in range(0,s):
            loc = ( loc[0] + delta[0] , loc[1] + delta[1], )
            colors[loc] = c

    #show(colors)
    print(f"Border size: {len(colors)}")

    minx = min( l[0] for l in colors.keys() )
    maxx = max( l[0] for l in colors.keys() )
    miny = min( l[1] for l in colors.keys() )
    maxy = max( l[1] for l in colors.keys() )

    outside = set()
    for y in range(miny, maxy+1):
        for x in range(minx,maxx+1):
            loc = (x,y)
            if loc in colors or loc in outside:
                continue

            tofill = set()
            out = False

            tosearch = collections.deque()
            tosearch.append( loc )

            while tosearch:
                l = tosearch.popleft()
                if l in colors or l in tofill:
                    continue
                if l in outside:
                    out = True
                if l[0] < minx or l[0] > maxx or l[1] < miny or l[1] > maxy:
                    out = True
                    continue
                tofill.add(l)
                for d in deltas.values():
                    tosearch.append( ( l[0] + d[0], l[1] + d[1] ) )

            if out:
                outside.update(tofill)
            else:
                for l in tofill:
                    colors[l] = "#000000"

    #show(colors)
    print(f"Filled Size: {len(colors)}")
        
    
if args.p1:
    print("Doing part 1")

    rundata(data, False);
    
if args.p2:
    print("Doing part 2")

    rundata(data, True);
    
def rundata(data, p2):
    loc = (0,0)
    colors = { loc : "#000000" }

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
        for i in range(0,s):
            loc = ( loc[0] + delta[0] , loc[1] + delta[1], )
            colors[loc] = c

    #show(colors)
    print(f"Border size: {len(colors)}")

    minx = min( l[0] for l in colors.keys() )
    maxx = max( l[0] for l in colors.keys() )
    miny = min( l[1] for l in colors.keys() )
    maxy = max( l[1] for l in colors.keys() )

    outside = set()
    for y in range(miny, maxy+1):
        for x in range(minx,maxx+1):
            loc = (x,y)
            if loc in colors or loc in outside:
                continue

            tofill = set()
            out = False

            tosearch = collections.deque()
            tosearch.append( loc )

            while tosearch:
                l = tosearch.popleft()
                if l in colors or l in tofill:
                    continue
                if l in outside:
                    out = True
                if l[0] < minx or l[0] > maxx or l[1] < miny or l[1] > maxy:
                    out = True
                    continue
                tofill.add(l)
                for d in deltas.values():
                    tosearch.append( ( l[0] + d[0], l[1] + d[1] ) )

            if out:
                outside.update(tofill)
            else:
                for l in tofill:
                    colors[l] = "#000000"

    #show(colors)
    print(f"Filled Size: {len(colors)}")
        
    
    
