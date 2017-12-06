#!/usr/bin/env python

import re, itertools, math, sys

lineRe = re.compile("(hlf|tpl|inc) ([a-z])|(jie|jio) ([a-z]), ([+-]\\d+)|(jmp) ([+-]\\d+)")

class Uniop:
    def __init__(self,op,reg):
        self.op = op
        self.reg = reg
        if self.reg == "a":
            self.regoff = 0
        else:
            self.regoff = 1

    def __str__(self):
        return "%s(%s)" % (self.op,self.reg,)

    def doit(self,regs):

        if self.op == "hlf":
            regs[self.regoff] /= 2
        elif self.op == "tpl":
            regs[self.regoff] *= 3
        elif self.op == "inc":
            regs[self.regoff] += 1
        return 1
    
class JumpIf:
    def __init__(self,op,reg,offset):
        self.op = op
        self.reg = reg
        if self.reg == "a":
            self.regoff = 0
        else:
            self.regoff = 1
        self.offset = offset

    def __str__(self):
        return "%s(%s):%s" % (self.op,self.reg,self.offset,)

    def doit(self,regs):
        input = regs[self.regoff]
        if self.op == "jie":
            if input % 2 == 0:
                return self.offset
            else:
                return 1
        elif self.op == "jio":
            if input == 1:
                return self.offset
            else:
                return 1
    
class Jump:
    def __init__(self,offset):
        self.op = "jmp"
        self.offset = offset

    def __str__(self):
        return "%s:%s" % (self.op,self.offset,)

    def doit(self,regs):
        return self.offset
    
ops = []
        
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    if m.group(1):
        ops.append(Uniop(m.group(1),m.group(2)))
    elif m.group(3):
        ops.append(JumpIf(m.group(3),m.group(4),int(m.group(5))))
    else:
        ops.append(Jump(int(m.group(7))))

for i in range(0,len(ops)):
    print "Op[%s]: %s" % (i,ops[i],)

print 

def run(regs):
    regs = list(regs)
    opnum = 0
    while opnum >= 0 and opnum < len(ops):
        op = ops[opnum]
        
        oldop = opnum
        opnum += op.doit(regs)
        
        #print "Op[%s]: %s Regs: %s Nxt:%s" % (oldop,op,regs,opnum)

    return regs


for inregs in [ [0,0], [1,0], ]:
    outregs = run(inregs)

    print "%s -> %s" % (inregs,outregs,)
