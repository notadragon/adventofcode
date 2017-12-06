#!/usr/bin/env python

import re, md5

opRe = re.compile("(tgl|cpy|jnz|inc|dec|out) (-?[0-9a-z]+)(?: (-?[0-9a-z-]+))?")

ops = []

for l in open("input").readlines():
    l = l.strip()

    m = opRe.match(l)
    if m:
        op = m.group(1)
        arg1 = m.group(2)
        arg2 = m.group(3)

        if arg2:
            ops.append( [op,arg1,arg2,] )
        else:
            ops.append( [op,arg1,] )
            
        continue

    print l

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

def getVal(regs,a):
    if a == "a":
        return regs[0]
    if a == "b":
        return regs[1]
    if a == "c":
        return regs[2]
    if a == "d":
        return regs[3]
    return int(a)

def run(iVal,tSize):
    regs = [iVal,0,0,0]

    i = 0

    transmitted = []
            
    while i < len(ops) and len(transmitted) < tSize:
        op = ops[i]
    
        #print "i: %s Ops: %s regs:%s" % (i,op,regs,)
    
        if op[0] == "cpy":
            f = getVal(regs,op[1])
            regs[getReg(op[2])] = f
        elif op[0] == "tgl":
            f = i+getVal(regs,op[1])
            if f >= 0 and f < len(ops):
                tglop = ops[f]
                if tglop[0]== "inc":
                    tglop[0] = "dec"
                elif len(tglop) == 2:
                    tglop[0] = "inc"
                elif tglop[0] == "jnz":
                    tglop[0] = "cpy"
                elif len(tglop) == 3:
                    tglop[0] = "jnz"
                else:
                    print "TOGGLE WTF"
        elif op[0] == "inc":
            if i < len(ops)-4:
                if ops[i+1][0] == "dec" and ops[i+2][0] == "jnz" and ops[i+3][0] == "dec" and ops[i+4][0] == "jnz" and ops[i+1][1] == ops[i+2][1] and ops[i+2][2] == "-2" and ops[i+3][1] == ops[i+4][1] and ops[i+4][2] == "-5":
                    # add ops[i+1][1] * ops[i+3][1] to op[1]
                    a = getReg(op[1])
                    b = getReg(ops[i+1][1])
                    c = getReg(ops[i+3][1])
                    regs[a] = regs[a] + regs[b] * regs[c]
                    regs[b] = 0
                    regs[c] = 0
                    i = i + 5
                    continue
                if ops[i+1][0] == "dec" and ops[i+2][0] == "jnz" and ops[i+1][1] == ops[i+2][1] and ops[i+2][2] == "-2":
                    # add ops[i+1][1] to op[1]
                    a = getReg(op[1])
                    b = getReg(ops[i+1][1])
                    regs[a] = regs[a] + regs[b]
                    regs[b] = 0
                    i = i + 3
                    continue            
            regs[getReg(op[1])] += 1
        elif op[0] == "dec":
            r = getReg(op[1])
            old = regs[r]
            if old > 0:
                regs[r] = old - 1
        elif op[0] == "jnz":
            x = getVal(regs,op[1])
            if x != 0:
                i += int(getVal(regs,op[2]))
                continue
        elif op[0] == "out":
            x = getVal(regs,op[1])

            transmitted.append(x)
            if len(transmitted) >= 2:
                if transmitted[-2] == transmitted[-1]:
                    return transmitted
            else:
                if transmitted[-1] != 0:
                    return transmitted
        i += 1
    
    return transmitted

i = 0
while True:
    if i % 10 == 0:
        print i
    tsize = 1000
    transmitted = run(i,tsize)

    if len(transmitted) == tsize and transmitted[-2] != transmitted[-1]:
        print "Input:%s" % (i,)
        print "Transmitted:%s" % (transmitted,)
        break

    i = i + 1
