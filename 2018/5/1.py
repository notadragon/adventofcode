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

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    polymer = x

#print("Polymer: %s" % (polymer,))

letters = "abcdefghijklmnopqrstuvwxyz"
pairs = {}
for c in letters:
    pairs[c] = c.upper()
    pairs[c.upper()] = c

def react(p,rem=""):
    result = []
    for c in p:
        if c == rem or c == rem.upper():
            continue
        elif result and result[-1] == pairs[c]:
            del result[-1]
        else:
            result.append(c)
    return "".join(result)
    
if args.p1:
    print("Doing part 1")

    result = react(polymer)
    print("Result Length:%s" % (len(result),))
            
if args.p2:
    print("Doing part 2")

    best = min( [ (len(react(polymer,c)), c,) for c in letters ] )

    print("Best: %s" % (best,))
    
