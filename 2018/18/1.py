#!/usr/bin/env python3

import argparse, re, sys, time

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')
parser.add_argument("--animate",dest="animate",action='store_true')

args = parser.parse_args()

if not args.p1 and not args.p2 and not args.animate:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile(".*")
grid = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(tuple(x))

padx = 100
pady = 25
padg = []
for i in range(0,pady):
    padg.append( (".",) * ( 2 * padx  + len(grid[0]) ) )

for g in grid:
    padg.append( (".",) * padx + g + (".",) * padx)
    
for i in range(0,pady):
    padg.append( (".",) * ( 2 * padx  + len(grid[0]) ) )

grid = tuple(padg)


def nextstate(x,adj):
    out = x
    if x == ".":
        if sum([1 for c in adj if c == "|"]) >= 3:
            out = "|"
    elif x == "|":
        if sum([1 for c in adj if c == "#"]) >= 3:
            out = "#"
    elif x == "#":
        if "#" in adj and "|" in adj:
            out = "#"
        else:
            out = "."
    #print("x: %s adj: %s out: %s" % (x,"".join(adj),out,))
    return out

def adjacent(g,x,y):
    out = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
            ty = y + dy
            if ty < 0 or ty >= len(g):
                continue
            tr = g[ty]
            tx = x + dx
            if tx < 0 or tx >= len(tr):
                continue
            out.append(tr[tx])
    return out
        
def step(g):
    out = []
    for y in range(0,len(g)):
        r = g[y]
        newr = []
        for x in range(0,len(r)):
            c = r[x]
            adj = adjacent(g,x,y)
            newr.append(nextstate(c,adj))
        out.append(tuple(newr))

    return tuple(out)

def show(g):
    for r in g:
        print("".join(r),flush=False)


def score(g):
    woods = sum([ sum([ 1 for c in r if c == "|"]) for r in g])
    yards = sum([ sum([ 1 for c in r if c == "#"]) for r in g])
    return woods * yards
    
if args.p1:
    print("Doing part 1")

    g = grid
    show(g)

    for i in range(1,11):
        g = step(g)

        print("")
        print("After %s minutes:" % (i,))
        show(g)
        print("  Score: %s" % (score(g),))
    
if args.p2:
    print("Doing part 2")

    g = grid

    grids = { g:0, }

    end = 1000000000
    
    i = 0
    while i != end:
        g = step(g)
        i = i + 1

        if g in grids:
            lastcase = grids[g]
            print("Cycle %s -> %s" % (lastcase,i,))

            delta = i - lastcase
            count = int((end - i) / delta)
            i += count * delta

            break
        
        else:
            grids[g] = i

    while i != end:
        g = step(g)
        i = i + 1
        
            
    print("")
    print("After %s minutes:" % (i,))
    #show(g)
    print("  Score: %s" % (score(g),))
        
            
if args.animate:
    i = 0
    g = grid
    
    while True:
        g = step(g)
        i = i + 1
        
        print("\x1b[2J\x1b[H",flush=False)

        
        print("",flush=False)
        print("After %s minutes:" % (i,),flush=False)
        show(g)
        print("  Score: %s" % (score(g),),flush=True)
        
        time.sleep(1)
