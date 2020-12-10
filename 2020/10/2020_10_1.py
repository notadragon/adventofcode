#!/usr/bin/env pypy

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
    data.append(int(x))

if args.p1:
    print("Doing part 1")

    sdata = sorted(data)
    
    highest = sdata[-1]
    builtin = highest + 3
    print("Builtin rating: %s" % (builtin,))

    diffs = [ j-i for i,j in zip([0] + sdata, sdata + [builtin]) ]
    diffcounts = { 1 : 0, 2 : 0, 3 : 0}
    for d in diffs:
        diffcounts[d] += 1

    print("Diffs; %s" % (diffcounts,))
    print("Result: %s" % (diffcounts[1] * diffcounts[3],))
    
if args.p2:
    print("Doing part 2")

    sdata = sorted(data)
    
    highest = sdata[-1]
    builtin = highest + 3

    alldata = [0,] + sdata + [builtin,]

    counts = [0] * len(alldata)
    counts[-1] = 1
    for i in range(len(counts)-1,-1,-1):
        pos = alldata[i]
        j = i + 1
        while j < len(alldata) and alldata[j] <= pos + 3:
            counts[i] += counts[j]
            j = j + 1
    #print("Counts: %s" % (counts,))
    print("Possible paths: %s" % (counts[0],))
    
