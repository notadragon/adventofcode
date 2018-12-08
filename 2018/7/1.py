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

steps = set()
deps = {}
lineRe = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    s1 = m.group(1)
    s2 = m.group(2)
    steps.add(s1)
    steps.add(s2)
    if s2 not in deps:
        deps[s2] = set()
    deps[s2].add(s1)

steps = sorted(list(steps))
for s in steps:
    if s not in deps:
        deps[s] = set()

print("Steps: %s" % (steps,))
print("Deps: %s" % (deps,))
    
if args.p1:
    print("Doing part 1")

    order = []
    done = set()
    while len(done) < len(steps):
        doable = []
        for s in steps:
            if s in done:
                continue
            dep = deps[s]
            if dep.issubset(done):
                order.append(s)
                done.add(s)
                break
            
    print("Order:%s" % ("".join(order,)))

    
if args.p2:
    print("Doing part 2")

    freeworkers = 5
    padtime = 60

    freeworkers = 2
    padtime = 0

    unstarted = list(steps)
    activeworkers = []
    time = 0
    order = []
    done = set()
    while len(done) < len(steps):
        #print("Time:%s active:%s" % (time,activeworkers,))
        
        found = False
        if freeworkers > 0:
            for s in unstarted:
                dep = deps[s]
                if dep.issubset(done):
                    freeworkers = freeworkers - 1
                    found = True
                    activeworkers.append( [ ord(s) - ord('A') + padtime + 1 , s ])
                    unstarted.remove(s)
        if found:
            continue
        # nothing startable, advance time
        if not activeworkers:
            break
        activeworkers.sort()

        advancetime = activeworkers[0][0]
        time += advancetime
        for w in activeworkers:
            w[0] -= advancetime
        while activeworkers and activeworkers[0][0] == 0:
            freeworkers += 1
            
            finished = activeworkers[0]
            del activeworkers[0]
            order.append(finished[1])
            done.add(finished[1])

    print("Order:%s" % ("".join(order,)))
    print("Total time: %s" % (time,))
        

    
