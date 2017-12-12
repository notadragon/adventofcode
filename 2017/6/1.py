#!/usr/bin/env python

import argparse

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

ivals = [ int(x.strip()) for x in open(args.input).readlines()[0].strip().split() ]

print ivals

def redist(mem):
    maxval=None
    maxndx = -1
    for i in range(0,len(mem)):
        if maxndx < 0 or mem[i] > maxval:
            maxval = mem[i]
            maxndx = i

    mem[maxndx] = 0
    rem = maxval

    all = rem // len(mem)
    
    for i in range(0,len(mem)):
        mem[i] = mem[i] + all
        rem -= all
        
    while rem > 0:
        maxndx += 1
        maxndx %= len(mem)
        mem[maxndx] = mem[maxndx] + 1
        rem -= 1
    

def vals(mem):
    mem = mem[:]
    yield tuple(mem)
    while True:
        redist(mem)
        yield tuple(mem)
           

valsiter = vals(ivals)

seen = set([])

num = 0
dup = None
for m in valsiter:
    if m in seen:
        print "first dup%s : %s" % (num,m,)
        dup = m
        break
    num += 1
    seen.add(m)

lnum = 0
for m in valsiter:
    lnum += 1
    if m == dup:
        print "looped: %s : %s" % (lnum,dup,)
        break
    
if args.p1:
    print "Doing part 1"
    print "  First Dup distance: %s" % (num,)
                
            
if args.p2:
    print "Doing part 2"
    print "  Loop size: %s" % (lnum,)
