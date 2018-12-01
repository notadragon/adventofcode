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

inputvals = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    inputvals.append(int(x))

print("InputVals:%s" % (inputvals,))

if args.p1:
    print("Doing part 1")

    print("Sum:%s" % (sum(inputvals,)))
    
if args.p2:
    print("Doing part 2")

    vals = set()

    frequency = 0
    vals.add(frequency)
    done = False
    while not done:
        for d in inputvals:
            frequency += d
            if frequency in vals:
                print("Duplicate:%s" % (frequency,))
                done = True
                break
            vals.add(frequency)
            
