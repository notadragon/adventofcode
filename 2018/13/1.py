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

lineRe = re.compile(".*")
grid = []

for x in open(args.input).readlines():
    x = x.rstrip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(list(x))

for g in grid:
    print(g)

def getval(grid,x,y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return " "
    return grid[y][x]

def show(s):
    grid,carts,crashed = s
    for g in grid:
        print("".join(g))
    for c in carts:
        print("Cart: %s" %(c,))
    for c in crashed:
        print("Crashed: %s" % (c,))

turns = { ("v","l") : (">","s"),
          ("v","s") : ("v","r"),
          ("v","r") : ("<","l"),
          (">","l") : ("^","s"),
          (">","s") : (">","r"),
          (">","r") : ("v","l"),
          ("^","l") : ("<","s"),
          ("^","s") : ("^","r"),
          ("^","r") : (">","l"),
          ("<","l") : ("v","s"),
          ("<","s") : ("<","r"),
          ("<","r") : ("^","l"), }

deltas = { "v" : (0,1),
           ">" : (1,0),
           "^" : (0,-1),
           "<" : (-1,0), }

moves = { ("-", "<") : "<",
          ("-", ">") : ">",
          ("|", "^") : "^",
          ("|", "v") : "v",
          ("\\", "v") : ">",
          ("\\", ">") : "v",
          ("\\", "^") : "<",
          ("\\", "<") : "^",
          ("/", "v") : "<",
          ("/", ">") : "^",
          ("/", "^") : ">",
          ("/", "<") : "v", }

def tick(state):
    grid,carts,crashed = state

    cartlocs = set( [ (c[0], c[1],) for c in carts ] )
    crashedlocs = set()
    
    newcarts = []
    newcrashed = list(crashed)

    for c in carts:
        x,y,s,d = c

        if (x,y) in crashedlocs:
            crashedlocs.remove( (x,y) )
            newcrashed.append( (x,y,s,d,) )
            
            continue
        
        track = grid[y][x]
        if track == "+":
            #need to turn
            s,d = turns[ (s,d,) ]
            delta = deltas[s]
        else:
            s = moves[ (track,s) ]
            delta = deltas[s]

        cartlocs.remove( (x,y) )
            
        x = x + delta[0]
        y = y + delta[1]

        if (x,y) in cartlocs:
            newcrashed.append( (x,y,s,d,) )

            found = False
            for i in range(0,len(newcarts)):
                nc = newcarts[i]
                if nc[0] == x and nc[1] == y:
                    del newcarts[i]
                    newcrashed.append(nc)
                    found = True
                    break
            if not found:
                crashedlocs.add( (x,y,) )

            cartlocs.remove( (x,y) )
        else:
            cartlocs.add( (x,y) )
            newcarts.append( (x,y,s,d,) )

    if crashedlocs:
        print("DIDN'T FIND CRASHED PAIR: %s" % (crashedlocs,))

    newcarts.sort()
        
    return grid,newcarts,newcrashed


if True:
    carts = []
    for y in range(0,len(grid)):
        row = grid[y]
        for x in range(0,len(row)):
            s = row[x]
            if s == "v" or s == "^" or s == ">" or s == "<":
                carts.append( (x,y,s,"l"), )
                neighbors = (getval(grid,x-1,y), getval(grid,x,y-1), getval(grid,x+1,y), getval(grid,x,y+1), )
                leftin = (neighbors[0] == "\\" or neighbors[0] == "/" or neighbors[0] == "-" or neighbors[0] == "+")
                upin = (neighbors[1] == "\\" or neighbors[1] == "|" or neighbors[1] == "/" or neighbors[1] == "+")
                rightin = (neighbors[2] == "/" or neighbors[2] == "-" or neighbors[2] == "\\" or neighbors[2] == "+")
                downin = (neighbors[3] == "/" or neighbors[3] == "|" or neighbors[3] == "\\" or neighbors[3] == "+")

                if (leftin and upin) or (downin and rightin):
                    underval = "/"
                elif (rightin and upin) or (leftin and downin):
                    underval = "\\"
                elif (leftin and rightin):
                    underval = "-"
                elif (upin and downin):
                    underval = "|"
                else:
                    underval = "?"
                row[x] = underval
                #print("Loc: %s,%s Neighbors: %s Left: %s Up: %s Right: %s Down: %s Underval: %s" % (x,y,neighbors,leftin,upin,rightin,downin,underval,))
                
if args.p1:
    print("Doing part 1")

    s = (grid,sorted(carts),(),)
    show(s)

    while not s[2]:
        s = tick(s)
    show(s)
        
if args.p2:
    print("Doing part 2")

    s = (grid,sorted(carts),(),)
    show(s)

    time = 0
    while len(s[1]) > 1:
        s = tick(s)
        time = time + 1
    show(s)

    print("Tick: %s" % (time,))
