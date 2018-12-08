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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lines = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    lines.append(x)

#print("Lines: %s" % (lines,))

def boxcount(x):
    output = {}
    for c in x:
        output[c] = output.get(c,0) + 1
    return output

if args.p1:
    print("Doing part 1")

    hastwos = 0
    hasthrees = 0
    
    for x in lines:
        counted = boxcount(x)
        if 2 in counted.values():
            hastwos += 1
        if 3 in counted.values():
            hasthrees += 1

    print("2s: %s  3s: %s  cksum: %s" % (hastwos, hasthrees, hastwos*hasthrees,))

def commonletters(x,y):
    output = []
    for i in range(0,min(len(x),len(y))):
        if x[i] == y[i]:
            output.append(x[i])
    return "".join(output)
    
if args.p2:
    print("Doing part 2")

    for i in range(0,len(lines)):
        for j in range(i+1,len(lines)):
            x = lines[i]
            y = lines[j]

            common = commonletters(x,y)

            if len(common) == (len(x)-1):
                print("%s %s -> %s" % (x,y,common,))
            
    
