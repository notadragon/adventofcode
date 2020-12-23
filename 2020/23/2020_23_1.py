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

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    labeling = x

print("Labeling: %s" % (labeling,))

def move(cups,cupmax):
    pickup = cups[1:4]
    del cups[1:4]

    destination = cups[0] - 1
    if destination < 1:
        destination = cupmax
        
    while destination in pickup:
        destination = destination - 1
        if destination < 1:
            destination = cupmax

    destndx = cups.index(destination)

    cups = cups[1:destndx+1] + pickup + cups[destndx+1:] + [cups[0]]

    return cups

if args.p1:
    print("Doing part 1")

    cups = list([ int(l) for l in labeling])
    cupmax = max(cups)
    for i in range(0,100):
        cups = move(cups,cupmax)

    onendx = cups.index(1)
    if onendx != len(cups)-1:
        cups = cups[onendx+1:] + cups[0:onendx+1]

    print("Final order 1 + %s" % ("".join([str(c) for c in cups[:-1]]),))

class Node:
    def __init__(self,val):
        self.val = val
        self.r = None

    def show(self,count = 10):
        x = self
        out = []
        for i in range(0,count):
            out.append(str(x.val))
            x = x.n
            if not x:
                break
        print("%s ... " % (", ".join(out),))

    def find(self,v):
        x = self
        while x.val != v:
            x = x.n
        return x

def move2(current, allcups, cupmax):
    pickup = current.n
    current.n = current.n.n.n.n
    pickup.n.n.n = None

    pickupvals = [ pickup.val, pickup.n.val, pickup.n.n.val, ]

    destination = current.val - 1
    if destination < 1:
        destination = cupmax
        
    while destination in pickupvals:
        destination = destination - 1
        if destination < 1:
            destination = cupmax

    destnode = allcups[destination]

    rest = destnode.n
    destnode.n = pickup
    pickup.n.n.n = rest

    current = current.n
    return current
        
if args.p2:
    print("Doing part 2")

    extracups = 1000000 - len(labeling)
    highest = max([int(i) for i in labeling])
    cupmax = highest + extracups 

    cups = [ Node(int(i)) for i in labeling ] + [ Node(i) for i in range(highest+1,highest+1+extracups) ]
    for i in range(0,len(cups)-1):
        cups[i].n = cups[i+1]
    cups[-1].n = cups[0]

    allcups = [ None ] * 1000001
    for c in cups:
        allcups[c.val] = c

    current = cups[0]

    current.show()

    for i in range(0,10000000):
        current = move2(current,allcups,cupmax)

    allcups[1].show()

    nv = allcups[1].n.val
    nnv = allcups[1].n.n.val
    print("Product: %s * %s = %s" % ( nv, nnv, nv * nnv,))
