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

lineRe = re.compile("(.*) ([+-]\d+)")
instructions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    instructions.append( (m.group(1), int(m.group(2)),))

def runinstructions(instructions):
    ip = 0
    accumulator = 0

    ran = set()
    
    while ip >= 0 and ip < len(instructions):
        if ip in ran:
            break
        ran.add(ip)
        
        instr = instructions[ip]

        if instr[0] == "acc":
            accumulator += instr[1]
            ip += 1
            pass
        elif instr[0] == "jmp":
            ip += instr[1]
            pass
        elif instr[0] == "nop":
            ip += 1
            pass

    return ip,accumulator
    
if args.p1:
    print("Doing part 1")

    out = runinstructions(instructions)
    print("First acc before second run of an instruction: %s" % (out[1],))
    
if args.p2:
    print("Doing part 2")

    for i in range(0,len(instructions)):
        instr = instructions[i]
        if instr[0] == "acc":
            continue

        fixed = instructions[:]
        if instr[0] == "jmp":
            newinstr = ("nop",instr[1])
        else:
            newinstr = ("jmp",instr[1])
        fixed[i] = newinstr

        out = runinstructions(fixed)
        if out[0] == len(fixed):
            print("Run %s Completed: %s" % (i,out,))
            break

            
            
