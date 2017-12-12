#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, nargs='?', default="input")
parser.add_argument("--p1", dest="p1", action='store_true')
parser.add_argument("--no-p1", dest="p1", action='store_false')
parser.add_argument("--p2", dest="p2", action='store_true')
parser.add_argument("--no-p2", dest="p2", action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input, args.p1, args.p2)

vals = []
for x in open(args.input).readlines():
    x = int(x.strip())
    vals.append(x)

if args.p1:
    print "Doing part 1"

    p1vals = vals[:]

    pos = 0
    steps = 0
    while pos < len(p1vals):
        off = p1vals[pos]
        p1vals[pos] = off + 1
        pos = pos + off
        steps += 1

    print "Steps: %s Pos:%s" % (steps, pos,)

if args.p2:
    print "Doing part 2"

    p2vals = vals[:]

    pos = 0
    steps = 0
    while pos < len(p2vals):
        off = p2vals[pos]

        if off >= 3:
            p2vals[pos] = off - 1
        else:
            p2vals[pos] = off + 1

        pos = pos + off
        steps += 1

    print "Steps: %s Pos:%s" % (steps, pos,)
