#!/usr/bin/env pypy

import argparse,re

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lineRe = re.compile("Generator (.*) starts with (\\d+)")

igens = {}
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
    else:
        igens[m.group(1)] = int(m.group(2))

def gengen(x,y):
    while True:
        y = (x * y) % 2147483647
        yield y

def makegens():
    A = gengen(16807,igens["A"])
    B = gengen(48271,igens["B"])
    return (A,B)

def gengen2(x,m,y):
    while True:
        y = (x * y) % 2147483647
        if y % m == 0:
            yield y

def makegens2():
    A = gengen2(16807,4,igens["A"])
    B = gengen2(48271,8,igens["B"])
    return (A,B)

    
print "Gens: %s" % (igens,)

if args.p1:
    print "Doing part 1"

    gens = makegens()
    for i in range(0,5):
        print "%10s %10s" % (gens[0].next(),gens[1].next(),)

    gens = makegens()
    out = 0
    for i in range(0,40000000):
        vals = (gens[0].next() & 0xffff, gens[1].next() & 0xffff)
        if vals[0] == vals[1]:
            out = out + 1
    print "Matching:%s" % (out,)
            
if args.p2:
    print "Doing part 2"

    gens = makegens2()
    for i in range(0,5):
        print "%10s %10s" % (gens[0].next(),gens[1].next(),)

    gens = makegens2()
    out = 0
    for i in range(0,5000000):
        vals = (gens[0].next() & 0xffff, gens[1].next() & 0xffff)
        if vals[0] == vals[1]:
            out = out + 1
    print "Matching:%s" % (out,)
