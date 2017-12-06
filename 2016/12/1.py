#!/usr/bin/env python

import re, md5

opRe = re.compile("(cpy|jnz|inc|dec) ([0-9a-z]+)(?: ([0-9a-z-]+))?")

ops = []

for l in open("input").readlines():
    l = l.strip()

    m = opRe.match(l)
    if m:
        op = m.group(1)
        arg1 = m.group(2)
        arg2 = m.group(3)

        if arg2:
            ops.append( (op,arg1,arg2,) )
        else:
            ops.append( (op,arg1,) )
            
        continue

    print l

regs = [0,0,1,0]

def getReg(a):
    if a == "a":
        return 0
    if a == "b":
        return 1
    if a == "c":
        return 2
    if a == "d":
        return 3
    return -1    

def getVal(a):
    if a == "a":
        return regs[0]
    if a == "b":
        return regs[1]
    if a == "c":
        return regs[2]
    if a == "d":
        return regs[3]
    return int(a)

i = 0
while i < len(ops):
    op = ops[i]

    #print "i: %s Ops: %s regs:%s" % (i,op,regs,)

    if op[0] == "cpy":
        f = getVal(op[1])
        regs[getReg(op[2])] = f
    elif op[0] == "inc":
        regs[getReg(op[1])] += 1
    elif op[0] == "dec":
        r = getReg(op[1])
        old = regs[r]
        if old > 0:
            regs[r] = old - 1
    elif op[0] == "jnz":
        x = getVal(op[1])
        if x != 0:
            i += int(op[2])
            continue
    i += 1
    
print ("Regs: %s" % (regs,))
