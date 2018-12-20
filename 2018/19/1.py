#!/usr/bin/env pypy

import argparse, re, itertools

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
        continue
    
    # Process input line
    if m.group(1):
        ip = int(m.group(1))
    else:
        instrs.append( (m.group(2),int(m.group(3)),int(m.group(4)),int(m.group(5)),) )

print("Ip: %s" % (ip,))
for i,instr in enumerate(instrs):
    instr=list(instr)
    
    if instr[0] == "seti" or instr[0] == "setr":
        instr[2] = "_"

    if instr[3] == ip:
        instr[3] = "P"
        if instr[0] == "seti":
            instr[0] = "goto"
        elif instr[0] == "addr":
            instr[0] = "jmpr"
        elif instr[0] == "addi":
            instr[0] = "jmpi"
        if instr[0][-1] == "r":
            if instr[2] == ip:
                instr[2] = "P"
        if instr[1] == ip:
            instr[1] = "P"

    if instr[0] == "addi" and instr[1] == 1:
        instr[0] = "incr"
        instr[1] = "_"


    print("Instr[%d]: %s %s %s %s" % (i,instr[0],instr[1],instr[2],instr[3],))

#Instr[1]: seti 1 _ 5   # F = 1          #for F = 1  F <= C  F++
#Instr[2]: seti 1 _ 3   # C = 1          #for D = 1  D <= C  D++
#Instr[3]: mulr 5 3 1   # B = D * F
#Instr[4]: eqrr 1 2 1   # B = B == C     #if D*F == C A += F
#Instr[5]: jmpr 1 P P   # skip B lines
#Instr[6]: jmpi P 1 P   # skip next line
#Instr[7]: addr 5 0 0   # A = A + F
#Instr[8]: addi 3 1 3   # D = D + 1
#Instr[9]: gtrr 3 2 1   # B = D > C
#Instr[10]: jmpr P 1 P  # skip B lines
#Instr[11]: goto 2 _ P  # end for on D
#Instr[12]: addi 5 1 5  # F = F + 1
#Instr[13]: gtrr 5 2 1  # B = F > C 
#Instr[14]: jmpr 1 P P  # skip B lines
#Instr[15]: goto 1 _ P  # end for on F

# making assumptions about location of function
instrs[1] = ("sumdivisors",instrs[13][2], ip, instrs[7][3],)
    
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
            
if args.p1:
    print("Doing part 1")

    regs = list([0 for r in range(0,6)])

    pos = 0
    while pos >= 0 and pos < len(instrs):
        instr = instrs[pos]
        regs[ip] = pos
        
        #print("Pos: %s op: %s registers: %s" % (pos,instr,regs,))

        applyop(instr,regs)

        pos = regs[ip] + 1
        #print("  -> Pos; %s registers: %s" % (pos,regs,))
        
    print("Final registers: %s" % (regs,))
    
    
if args.p2:
    print("Doing part 2")

    regs = list([0 for r in range(0,6)])
    regs[0] = 1
    
    pos = 0
    while pos >= 0 and pos < len(instrs):
        instr = instrs[pos]
        regs[ip] = pos

        #print("Pos: %s op: %s registers: %s" % (pos,instr,regs,))
        
        applyop(instr,regs)

        pos = regs[ip] + 1
        #print("  -> Pos; %s registers: %s" % (pos,regs,))
        
    print("Final registers: %s" % (regs,))
