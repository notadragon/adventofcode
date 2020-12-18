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
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

tokenRe = re.compile("\d+|[\+\*\(\)]")

def evaltree1(ttree):
    #print("ttree: %s" % (ttree,))
    if type(ttree) == int:
        return ttree
    
    lhs = evaltree1(ttree[0])
    for op,rhs in zip(ttree[1::2],ttree[2::2]):
        rhs = evaltree1(rhs)
        if op == "+":
            lhs += rhs
        elif op == "*":
            lhs *= rhs
    return lhs
            
    

def process(line,et):
    stack = []
    first = True
    tokens = [ t for t in tokenRe.findall(line) ]

    stack = []
    ttree = []
    stack.append(ttree)
    
    for token in tokens:
        if token == "(":
            subexpr = []
            stack[-1].append(subexpr)
            stack.append(subexpr)
            pass
        elif token == ")":
            del stack[-1]
            pass
        elif token == "*":
            stack[-1].append(token)
            pass
        elif token == "+":
            stack[-1].append(token)
            pass
        else:
            val = int(token)
            stack[-1].append(val)

    #print("line: %s ttree: %s" % (line, ttree,))

    return et(ttree)

if args.p1:
    print("Doing part 1")

    alltotal = 0
    for eq in data:
        total = process(eq,evaltree1)
        #print("%s = %s" % (eq,total,))
        alltotal += total
    print("All Total: %s" % (alltotal,))

def evaltree2(ttree):
    #print("ttree: %s" % (ttree,))
    if type(ttree) == int:
        return ttree

    newttree = []
    
    newttree.append( evaltree2(ttree[0]) )
    
    for op,rhs in zip(ttree[1::2],ttree[2::2]):
        rhs = evaltree2(rhs)
        if op == "+":
            newttree[-1] += rhs
        elif op == "*":
            newttree.append("*")
            newttree.append(rhs)

    lhs = newttree[0]
    for op,rhs in zip(newttree[1::2],newttree[2::2]):
        lhs *= rhs
    
    return lhs
    
if args.p2:
    print("Doing part 2")

    alltotal = 0
    for eq in data:
        total = process(eq,evaltree2)
        #print("%s = %s" % (eq,total,))
        alltotal += total
    print("All Total: %s" % (alltotal,))
    
