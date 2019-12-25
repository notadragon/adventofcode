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

lineRe = re.compile("(\d+)")

weights = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    weights.append(int(x))

print("Weights: %s" % (weights,))

def groups(weights, group, groupweight):
    #print("Weights: %s group: %s groupweight: %s" % (weights, group, groupweight,))
    for i in range(len(weights)-1,-1,-1):
        w = weights[i]
        if w > groupweight:
            continue
        g = group + (w,)
        rest = weights[0:i] + weights[i+1:]

        if w == groupweight:
            yield g,rest
            continue

        minsize = None
        for rg, rr in groups(rest, g, groupweight-w):
            if not minsize or len(rg) <= minsize:
                yield (rg,rr)
                minsize = len(rg)
            

def splitup(weights):
    groupweight = sum(weights) / 3

    for g1,rest in groups(weights,(),groupweight):
        for g2,r2 in groups(rest, (), groupweight):
            yield g1,g2,r2
            break

def splitup2(weights):
    groupweight = sum(weights) / 4

    for g1,rest in groups(weights,(),groupweight):
        for g2,r2 in groups(rest, (), groupweight):
            for g3,r3 in groups(r2, (), groupweight):
                yield (g1,g2,g3,r3)
                break
            break
        
        
def entanglement(g):
    output = 1
    for c in g:
        output = output * c
    return output

if args.p1:
    print("Doing part 1")

    bestg = None
    bestq = 0
    for g in splitup(weights):
        if not bestg:
            bestg = g
            bestq = entanglement(bestg[0])
            print("Best: %s (QE=%s)" % (bestg[0], bestq,))
        else:
            if len(g[0]) > len(bestg[0]):
                continue
            e = entanglement(g[0])
            if len(g[0]) < len(bestg[0]) or e < bestq:
                bestg = g
                bestq = e
                print("Best: %s (QE=%s)" % (bestg[0], e,))
    
    
if args.p2:
    print("Doing part 2")

    bestg = None
    bestq = 0
    for g in splitup2(weights):
        if not bestg:
            bestg = g
            bestq = entanglement(bestg[0])
            print("Best: %s (QE=%s)" % (bestg[0], bestq,))
        else:
            if len(g[0]) > len(bestg[0]):
                continue
            e = entanglement(g[0])
            if len(g[0]) < len(bestg[0]) or e < bestq:
                bestg = g
                bestq = e
                print("Best: %s (QE=%s)" % (bestg[0], e,))
    
