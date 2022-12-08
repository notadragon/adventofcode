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
    grid.append(x)

def get(grid, x, y):
    if y < 0 or y >= len(grid):
        return -1
    if x < 0 or x >= len(grid[y]):
        return -1
    return grid[y][x]

trees = {}
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        trees[ (x,y) ] = int(grid[y][x])

minx = 0
maxx = max( len(row) for row in grid )
miny = 0
maxy = len(grid)


if args.p1:
    print("Doing part 1")

    treevisibilities = {}

    dirs = [
        #top
        ( "T",  (0,-1), ( (x, maxy-1) for x in range(minx,maxx) ), ),
        #bottom
        ( "B", (0,1),  ( (x, miny)   for x in range(minx,maxx) ), ),
        #right
        ( "L", (-1,0), ( (maxx-1, y) for y in range(miny,maxy) ), ),
        #left
        ( "R", (1,0),  ( (minx, y)   for y in range(miny,maxy) ), ),
    ]

    def addvis(dirname, loc):
        if not loc in treevisibilities:
            treevisibilities[loc] = []
        treevisibilities[loc].append(dirname)
    
    for dirname, delta, edges in dirs:
        for startloc in edges:
            height = -1
            loc = startloc
            while loc in trees:
                locheight = trees[loc]
                if locheight > height:
                    height = locheight
                    addvis(dirname, loc)
                
                loc = (loc[0] + delta[0], loc[1] + delta[1])
    

    print(f"Visible Trees: {len(treevisibilities)}")
    
if args.p2:
    print("Doing part 2")

    viewdistances = {}
    scenicscores = {}
    
    dirs = [ (0,-1), (0,1), (-1,0), (1,0) ]

    bestscore = ( None, 0 )
    for loc,locheight in trees.items():

        views = []
        score = 1
        for delta in dirs:
            view = 0
            vloc = (loc[0] + delta[0], loc[1] + delta[1])
            while vloc in trees:
                view = view + 1
                if trees[vloc] >= locheight:
                    break
                vloc = (vloc[0] + delta[0], vloc[1] + delta[1])
            views.append(view)
            score = score * view
        viewdistances[loc] = views
        scenicscores[loc] = score

        if score > bestscore[1]:
            bestscore = ( loc, score )
    
        #print(f"{loc} -> {views} -> {score}")

    print(f"Best Score: {bestscore}")
