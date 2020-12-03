#!/usr/bin/env pypy

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()
data = []

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)


def getpath(data,slope):
    pos = (0,0)
    while pos[0] < len(data):
        row = data[pos[0]]
        col = row[pos[1] % len(row)]
        yield (pos, col)
        pos = (pos[0] + slope[0], pos[1] + slope[1])
                       
    
if args.p1:
    print("Doing part 1")

    
    trees = len([ x for x in getpath(data, (1,3)) if x[1] == "#"])
    print("Trees: %s" % (trees,))
        
    
if args.p2:
    print("Doing part 2")

    total = 1
    for slope in [ (1,1), (1,3), (1,5), (1,7), (2,1) ]:
        trees = len([ x for x in getpath(data, slope) if x[1] == "#"])

        print("SLope: %s -> %s" % (slope, trees,) )
        total *= trees
    print("Product: %s" % (total,))
