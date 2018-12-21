#!/usr/bin/env python3

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

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))
lineRe = re.compile("(?:#ip ([0-9]+))|(?:([a-z]+) (-?[0-9]+) (-?[0-9]+) (-?[0-9]+)).*")
instrs = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        ip = int(m.group(1))
    else:
        instrs.append( (m.group(2),int(m.group(3)),int(m.group(4)),int(m.group(5)),) )

print("Ip: %s" % (ip,))
for i,instr in enumerate(instrs):
    print("%4d: %s" % (i,instr,))

def applyop(instr, regs):
    op,A,B,C = instr
    if C < 0 or C >= len(regs): return None
    
    if op == "sumdivisors":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        regs[C] = sum([ p for p in range(1,regs[A]+1) if regs[A] % p == 0 ])
        regs[B] += 14
    elif op == "addr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        regs[C] = regs[A] + regs[B]
    elif op == "addi":
        if A < 0 or A >= len(regs): return None
        regs[C] = regs[A] + B
    elif op == "mulr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        regs[C] = regs[A] * regs[B]
    elif op == "muli":
        if A < 0 or A >= len(regs): return None
        regs[C] = regs[A] * B
    elif op == "banr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        regs[C] = regs[A] & regs[B]
    elif op == "bani":
        if A < 0 or A >= len(regs): return None
        regs[C] = regs[A] & B
    elif op == "borr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        regs[C] = regs[A] | regs[B]
    elif op == "bori":
        if A < 0 or A >= len(regs): return None
        regs[C] = regs[A] | B
    elif op == "setr":
        if A < 0 or A >= len(regs): return None
        regs[C] = regs[A]
    elif op == "seti":
        regs[C] = A
    elif op == "gtir":
        if B < 0 or B >= len(regs): return None
        if A > regs[B]:
            regs[C] = 1
        else:
            regs[C] = 0
    elif op == "gtri":
        if A < 0 or A >= len(regs): return None
        if regs[A] > B:
            regs[C] = 1
        else:
            regs[C] = 0
    elif op == "gtrr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        if regs[A] > regs[B]:
            regs[C] = 1
        else:
            regs[C] = 0
    elif op == "eqir":
        if B < 0 or B >= len(regs): return None
        if A == regs[B]:
            regs[C] = 1
        else:
            regs[C] = 0
    elif op == "eqri":
        if A < 0 or A >= len(regs): return None
        if regs[A] == B:
            regs[C] = 1
        else:
            regs[C] = 0
    elif op == "eqrr":
        if A < 0 or A >= len(regs): return None
        if B < 0 or B >= len(regs): return None
        if regs[A] == regs[B]:
            regs[C] = 1
        else:
            regs[C] = 0
    else:
        print("UNKNOWN OP: %s" % (op,))


def runinstrs(instrs,regs):
    exitvals = [0,0]
    allexitvals = set()
    
    pos = 0
    while pos >= 0 and pos < len(instrs):
        instr = instrs[pos]
        regs[ip] = pos
        
        if pos == 14:
            #print("Pos: %s op: %s registers: %s" % (pos,instr,regs,))

            if regs[5] >= 256:
                regs[2] = int(regs[5] / 256)
                regs[3] = 1
                regs[4] = 25
            else:
                regs[4] = 27
                
        else:
            applyop(instr,regs)
            
        if pos == 28:
            exitval = regs[1]

            if not allexitvals:
                exitvals[0] = exitval
            if exitval in allexitvals:
                break
            allexitvals.add(exitval)
            exitvals[1] = exitval

            
            #print("Exit Test: %s" % (regs,))
            #print("Exit Vals: %s" % (len(allexitvals),))

        pos = regs[ip] + 1
        #print("  -> Pos; %s registers: %s" % (pos,regs,))
        
    return regs,exitvals
       

if True:
    
    r1 = 0
    
    regs = [0] * 6
    regs[0] = r1
    regs,exitvals = runinstrs(instrs,regs)

    print("Completed: r1=%s" % (r1,))
    print("Final registers: %s" % (regs,))
    print("ExitVals: %s" % (exitvals,))

if args.p1:
    print("Doing part 1")
    print("Min exit val: %s" % (exitvals[0],))

if args.p2:
    print("Doing part 2")
    print("Max exit val: %s" % (exitvals[1],))
