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

lineRe = re.compile("[v.>]+")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)
    
def tomap(data):
    output = {}

    for y in range(0,len(data)):
        for x in range(0,len(data[y])):
            if data[y][x] != ".":
                output[ (x,y) ] = data[y][x]

    return output
    
    
dmap = tomap(data)
maxx = len(data[0])
maxy = len(data)


def step(dmap):
    newmap = {}
    for loc, cucu in dmap.items():
        if cucu == ">":
            nloc = ( (loc[0] + 1) % maxx, loc[1] )
            if nloc in dmap:
                nloc = loc
            newmap[nloc] = ">"
    for loc, cucu in dmap.items():
        if cucu == "v":
            nloc = ( loc[0], (loc[1] + 1) % maxy, )
            if (nloc in dmap and dmap[nloc] == "v") or nloc in newmap:
                nloc = loc
            newmap[nloc] = "v"
    return newmap

def show(dmap):
    toshow = [ ["."] * maxx for i in range(0,maxy) ]

    for loc,val in dmap.items():
        toshow[loc[1]][loc[0]] = val

    for r in toshow:
        print("".join(r))

if args.p1:
    print("Doing part 1")

    cucumap = dmap
    steps = 0

    print("Step: 0")
    #show(cucumap)
    
    while True:
        newmap = step(cucumap)

        steps = steps + 1

        #print(f"Step: {steps}")
        #show(newmap)
        
        if newmap == cucumap:
            break
        cucumap = newmap
    print(f"Fixed positions after step: {steps}")
    
    
if args.p2:
    print("Doing part 2")
