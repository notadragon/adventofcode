#!/usr/bin/env python3

import argparse, re, itertools, collections, queue

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

lineRe = re.compile("\d+")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(tuple( int(c) for c in x) )
data = tuple(data)

def gget(grid, loc):
    if loc[1] < 0 or loc[1] >= len(grid):
        return None
    if loc[0] < 0 or loc[0] >= len(grid[loc[1]]):
        return None
    return grid[loc[1]][loc[0]]

def gadj(getter, loc):
    for d in ( (-1,0), (1,0), (0,-1), (0,1) ):
        a = ( loc[0] + d[0], loc[1] + d[1])
        val = getter(a)
        if val != None:
            yield a

def minRisk(getter, startloc, endloc):
    paths = queue.PriorityQueue()
    paths.put( ( 0, startloc, ) )

    found = set()
    found.add(startloc)

    while not paths.empty():
        path = paths.get()

        #print(f"Path: {path}")
        
        if path[-1] == endloc:
            return path

        for a in gadj(getter,path[-1]):
            if a in found:
                continue
            found.add(a)
            
            acost = path[0] + getter(a)
            #paths.put( (acost,) + path[1:] + (a,) )
            paths.put( (acost,a,) )

    
if args.p1:
    print("Doing part 1")

    def getter(loc):
        return gget(data,loc)
    
    path = minRisk(getter, (0,0), (len(data[-1])-1, len(data)-1))

    print(f"Optimal Path: {path}")
    print(f"Minimal Risk: {path[0]}")
    
def gget2(data, loc):
    y = loc[1] % len(data)
    x = loc[0] % len(data[y])
    ymult = loc[1] // len(data)
    if ymult < 0 or ymult >= 5:
        return None
    xmult = loc[0] // len(data[y])
    if xmult < 0 or xmult >= 5:
        return None
    val = data[y][x] + ymult + xmult
    while val > 9:
        val = val - 9
    return val
    
    
    
    
if args.p2:
    print("Doing part 2")

    def getter(loc):
        return gget2(data,loc)
    
    path = minRisk(getter, (0,0), (5*len(data[-1])-1, 5*len(data)-1))

    print(f"Optimal Path: {path}")
    print(f"Minimal Risk: {path[0]}")
