#!/usr/bin/env python

import re

instructionRe=re.compile("(?:(\\d+)|(?:(?:(\\d+)|([a-z]+)) (AND|OR) ([a-z]+))|(?:([a-z]+) ([LR]SHIFT) (\\d+))|(?:NOT ([a-z]+))|([a-z]+)) -> ([a-z]+)")

circuit={}

class Fixed:
    def __init__(self,val,outKey):
        self.val=val
        self.outKey=outKey

    def eval(self,signals):
        return self.val

    def __str__(self):
        return "Fixed: %s -> %s" % (self.val,self.outKey,)

class Copy:
    def __init__(self,key,outKey):
        self.key = key
        self.outKey = outKey

    def eval(self,signals):
        if not signals.has_key(self.key):
            return None
        return signals[self.key]

    def __str__(self):
        return "Copy:%s -> %s" % (self.key,self.outKey)


class BaseOp:
    def __init__(self,op,outKey):
        self.outKey = outKey
        self.op = op
        
    def applyOp(self,lhs,rhs):
        if self.op == "NOT":
            output = ~ lhs & 0xffff
        elif self.op == "RSHIFT":
            output = lhs >> rhs
        elif self.op == "LSHIFT":
            output = lhs << rhs & 0xffff
        elif self.op == "AND":
            output = lhs & rhs
        elif self.op == "OR":
            output = lhs | rhs

        print "%s APPLYING:%s to:%s and:%s -> %s" % (self.outKey,self.op,lhs,rhs,output,)
        return output

    def __str__(self):
        return "%s %s %s -> %s" % (self.lhs,self.op,self.rhs,self.outKey,)
    
class FixedOp(BaseOp):
    def __init__(self,op,lhs,rhs,outKey):
        BaseOp.__init__(self,op,outKey)
        self.lhs=lhs
        self.rhs=rhs

    def eval(self,signals):
        if not signals.has_key(self.lhs):
            return None
        lhsVal=signals[self.lhs]
        rhsVal=self.rhs
        return self.applyOp(lhsVal,rhsVal)



class BinOp(BaseOp):
    def __init__(self,op,lhs,rhs,outKey):
        BaseOp.__init__(self,op,outKey)
        self.lhs=lhs
        self.rhs=rhs

    def eval(self,signals):
        if not signals.has_key(self.lhs):
            return None
        if not signals.has_key(self.rhs):
            return None
        lhsVal=signals[self.lhs]
        rhsVal=signals[self.rhs]
        return self.applyOp(lhsVal,rhsVal)


for line in open("input").readlines():
    line=line.strip()
    if not line: continue

    m=instructionRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    output=m.group(11)

    if circuit.has_key(output):
        print "Multiple inputs for: %s" % (output,)
    elif m.group(1):
        circuit[output]=Fixed(int(m.group(1)),output)
    elif m.group(4):
        if m.group(2):
            circuit[output]=FixedOp(m.group(4),m.group(5),int(m.group(2)),output)
        else:
            circuit[output]=BinOp(m.group(4),m.group(3),m.group(5),output)
    elif m.group(7):
        circuit[output]=FixedOp(m.group(7),m.group(6),int(m.group(8)),output)
    elif m.group(9):
        circuit[output]=FixedOp("NOT",m.group(9),None,output)
    elif m.group(10):
        circuit[output]=Copy(m.group(10),output)
        
    print "line:%-20s output:%-2s eval:%s" % (line, output, circuit.get(output,"None"),)

    

def build_signals(circuit,signals):
    while True:
        numApplied=0

        for signal in circuit:
            if signals.has_key(signal):
                continue
            
            func=circuit[signal]
            val=func.eval(signals)
            if val != None:
                signals[signal]=val
                numApplied=numApplied+1
    
        if numApplied == 0:
            break;
    return signals

signals=build_signals(circuit,{})
aVal=signals["a"]

signals=build_signals(circuit,{"b":aVal})
bVal=signals["a"]

print "aVal: %s newAVal: %s" % (aVal,bVal,)
