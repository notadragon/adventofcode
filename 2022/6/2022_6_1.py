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

lineRe = re.compile("[a-z]+")
inputs = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    inputs.append(x)

def isMarker(chrs):
    return len(set(chrs)) == len(chrs) 
    
def nextMarker(data,mlen):
    for i in range(0,len(data)-mlen):
        if isMarker(data[i:i+mlen]):
            return i + mlen
    
if args.p1:
    print("Doing part 1")

    for i in inputs:
        n = nextMarker(i,4) 
        print(f"{i} -> {n}")
    
if args.p2:
    print("Doing part 2")

    for i in inputs:
        n = nextMarker(i,14) 
        print(f"{i} -> {n}")
