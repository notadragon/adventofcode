#!/usr/bin/env python3

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
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = [ int(y) for y in x.split(",") ]

#print(f"Data: {data}")

if args.p1:
    print("Doing part 1")

    #print(f"len: {len(data)}")
    #print(f"sum: {sum(data)}")
    #print(f"min: {min(data)}")
    #print(f"max: {max(data)}")

    def cost(data,n):
        return sum([ abs(x-n) for x in data])

    mincost = None
    minpos = None
    for i in range(min(data),max(data)+1):
        icost = cost(data,i)

        if mincost == None or icost < mincost:
            mincost = icost
            minpos = i
        #print(f"{i} : {icost}")

    print(f"Best Pos: {minpos}  Cost: {mincost}")
    
if args.p2:
    print("Doing part 2")

    def movecost(x,y):
        d = abs(x-y)
        return (d * (d+1)) // 2

    def cost(data,n):
        return sum([ movecost(x,n) for x in data])

    mincost = None
    minpos = None
    for i in range(min(data),max(data)+1):
        icost = cost(data,i)

        if mincost == None or icost < mincost:
            mincost = icost
            minpos = i
        #print(f"{i} : {icost}")

    print(f"Best Pos: {minpos}  Cost: {mincost}")
