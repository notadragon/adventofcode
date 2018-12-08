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

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    ival = x

print("Ival:%s" % (ival,))

def lookandsay(x):
    output = []
    ndx = 0
    while ndx < len(x):
        c = x[ndx]
        l = 1
        ndx = ndx + 1
        
        while ndx < len(x) and x[ndx] == c:
            ndx = ndx +1
            l = l + 1
        output.append(str(l))
        output.append(c)
        
    return "".join(output)
        
if args.p1:
    print("Doing part 1")

    x = ival
    print("0:%s" % (x,))
    for i in range(1,41):
        x = lookandsay(x)
        print("%d:%s (%s)" % (i,x[:20],len(x),))
        
if args.p2:
    print("Doing part 2")

    x = ival
    print("0:%s" % (x,))
    for i in range(1,51):
        x = lookandsay(x)
        print("%d:%s (%s)" % (i,x[:20],len(x),))
