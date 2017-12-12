#!/usr/bin/env python

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

progRe = re.compile("([a-z]+) \\(([0-9]+)\\)(?: -> ([a-z]+(?:, [a-z]+)*))?")

programs = {}

for x in open(args.input).readlines():
    x = x.strip()
    if x:
        m = progRe.match(x)
        if not m:
            print "Invalid line:%s" % (x,)
        else:
            prog = m.group(1)
            weight = int(m.group(2))
            children = m.group(3)
            if children:
                children = children.split(", ")
            programs[prog] = [prog,weight,children]

if True:
    prognames = set(programs.keys())
    for prog,weight,children in programs.values():
        if children:
            for child in children:
                prognames.remove(child)
                
    for p in prognames:
        root = p

def weightsum(p):
    pval = programs[p]
    if len(pval) >= 4:
        return pval[3]
    else:
        out = pval[1]
        children = pval[2]
        if children:
            for c in children:
                out += weightsum(c)
        pval.append(out)
        return out        

weightsum(root)

def balanced(p):
    pval = programs[p]
    if len(pval) >= 5:
        return pval[4]
    else:
        children = pval[2]
        out = True
        if children:
            cweight = weightsum(children[0])
            for child in children[1:]:
                if weightsum(child) != cweight:
                    out = False
                    break
        pval.append(out)
        return out

def visit(p,f):
    f(p)
    children = programs[p][2]
    if children:
        for c in children:
            visit(c,f)
visit(root,balanced)

if args.p1:
    print "Doing part 1"
    print "root: %s" % (root,)
    

def doshow(r,depth,off,out):
    while len(out) <= off:
        out.append([""] * depth)
    while len(out[off]) < depth:
        out[off].append("")
    out[off].append(r)
    children = programs[r][2]
    if children:
        for c in children:
            if c != children[0]:
                off = off+1
            off = doshow(c,depth+1,off,out) 
            
    return off


        
def show(r):
    def display(p):
        return "%s (%s,%s,%s)" % (p,programs[p][1],programs[p][3],programs[p][4])
    
    toshow = []
    doshow(r,0,0,toshow)

    maxlen = max(len(display(x)) for x in programs.keys())
    
    for r in toshow:
        s = []
        prev = False
        for i in range(0,len(r)):
            p = r[i]
            if p:
                p = display(p)
                if prev:
                    s.append(" -> ")
                else:
                    s.append("    ")
                prev = True
                while len(p) < maxlen:
                    p = p + " "
                s.append(p)
            else:
                prev = False
                s.append("    ")
                s.append(" " * maxlen)
        print "".join(s)
        

#show(root)

if args.p2:
    print "Doing part 2"

    unbal = root
    while True:
        uval = programs[unbal]
        unbalchildren = [ c for c in uval[2] if not programs[c][4] ]
        print "uval: %s unbalchildren: %s" % (uval,unbalchildren,)
        if unbalchildren:
            unbal = unbalchildren[0]
        else:
            break
    uval = programs[unbal]
    print "Unabalanced parent: %s vals: %s" % (unbal,uval,)
    cweights = {}
    for c in uval[2]:
        cval = programs[c]
        cweights[cval[3]] = cweights.get(cval[3],0) + 1
    print " Child weights: %s" % (cweights,)
    badweight = [ cweight for cweight,count in cweights.items() if count == 1 ][0]
    goodweight = [ cweight for cweight,count in cweights.items() if count != 1 ][0]
    badchild = [ c for c in uval[2] if programs[c][3] == badweight][0]
    print "  bad weight %s" % (badweight,)
    print "  good weight %s" % (goodweight,)
    print "  offset: %s" % (goodweight - badweight,)
    print "  bad child: %s (%s)" % (badchild,programs[badchild],)
    print "  fixed weight: %s" % (programs[badchild][1] - badweight + goodweight,)
    
        
