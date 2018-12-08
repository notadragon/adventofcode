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

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    line = x

if args.p1:
    print("Doing part 1")

    f = 0
    for c in line:
        if c == "(":
            f = f + 1
        elif c == ")":
            f = f - 1
    print("Final Floor: %s" % (f,))
    
if args.p2:
    print("Doing part 2")

    f = 0
    p = 1
    for c in line:
        if c == "(":
            f = f + 1
        elif c == ")":
            f = f - 1
        if f < 0:
            print("In basement at pos: %s" % (p,))
            break
        p = p + 1
