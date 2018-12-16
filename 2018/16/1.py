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

lineRe = re.compile("(?:(Before|After): +\\[([0-9+]), ([0-9]+), ([0-9]+), ([0-9]+)\\])|(?:([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+))")

samples = []
sample = []
code = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        sample.append( (int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5))) )
    else:
        sample.append( (int(m.group(6)),int(m.group(7)),int(m.group(8)),int(m.group(9))) )

        if len(sample) == 1:
            code.append(sample[0])
            sample = []
        
    if len(sample) == 3:
        samples.append(sample)
        sample = []

#for b in samples:
#    print("Sample: %s" % (b,))

ops = ["addr","addi",
       "mulr","muli",
       "banr","bani",
       "borr","bori",
       "setr","seti",
       "gtir","gtri","gtrr",
       "eqir","eqri","eqrr", ]

def applyop(instr, regs):
    regs = list(regs)

    op,A,B,C = instr
    
    if op == "addr":
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
            
    return tuple(regs)

def resolvemapping(opmapping):
    def resolvestep(used,i):
        if i == 16:
            yield tuple(used)
            return
        for op in opmapping[i]:
            if op in used:
                continue
            used.append(op)
            for o in resolvestep(used,i+1):
                yield o
            del used[-1]
                
    return list(resolvestep([],0))
    

if True:
    opmapping = { i : set(ops) for i in range(0,16) }
    
    manyops = 0
    for sample in samples:
        before,instr,after = sample

        possibleops = 0

        #print("Instr:     %s" % (instr,))
        #print("Expeced: - %s -> %s" % (before,after,))
        for op in ops:
            result = applyop( (op,) + instr[1:], before)
            #print("Op: %s - %s -> %s" % (op,before,result,))
            if result == after:
                possibleops += 1
            else:
                opmapping[ instr[0] ].discard(op)

        #print("%s: %s" % (sample,possibleops,))
        if possibleops >= 3:
            manyops += 1
            #print("Many ops: %s" % (sample,))

    print("OpMapping: %s" % (opmapping,))

    opcodes = resolvemapping(opmapping)[0]
    print("Ops: %s" % (opcodes,))
    
if args.p1:
    print("Doing part 1")
    print("Possible Ops >= 3: %s" % (manyops,))
    
if args.p2:
    print("Doing part 2")

    regs = (0,0,0,0)
    for instr in code:
        realinstr = (opcodes[instr[0]],) + instr[1:]
        newregs = applyop( realinstr, regs)

        #print("%s %s -> %s" % (regs, realinstr, newregs,) )
        regs = newregs
        
    print("Final Register Values: %s" % (regs,))
        
        
