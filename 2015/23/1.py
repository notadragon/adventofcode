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

lineRe = re.compile("(jio|inc|tpl|jmp|jie|hlf) ([a-z]|[+-][0-9]+)(, ([+-][0-9]+))?")

instructions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    if m.group(3):
        instructions.append( (m.group(1), m.group(2),m.group(4),) )
    else:
        instructions.append( (m.group(1), m.group(2),) )

def execute(instrs, registers):
    pos = 0

    while pos >= 0 and pos < len(instrs):

        instr = instrs[pos]

        if instr[0] == "hlf":
            ndx = 0 if instr[1] == "a" else 1
            registers[ndx] = registers[ndx] // 2
            pos = pos + 1
        elif instr[0] == "tpl":
            ndx = 0 if instr[1] == "a" else 1
            registers[ndx] = registers[ndx] * 3
            pos = pos + 1
        elif instr[0] == "inc":
            ndx = 0 if instr[1] == "a" else 1
            registers[ndx] = registers[ndx] + 1
            pos = pos + 1
        elif instr[0] == "jmp":
            pos = pos + int(instr[1])
        elif instr[0] == "jie":
            ndx = 0 if instr[1] == "a" else 1
            if registers[ndx] % 2 == 0:
                pos = pos + int(instr[2])
            else:
                pos = pos + 1
        elif instr[0] == "jio":
            ndx = 0 if instr[1] == "a" else 1
            if registers[ndx] == 1:
                pos = pos + int(instr[2])
            else:
                pos = pos + 1
            
        
if args.p1:
    print("Doing part 1")

    registers = [0,0]
    execute(instructions,registers)

    print("Final Registers: %s" % (registers,))
    
if args.p2:
    print("Doing part 2")
    
    registers = [1,0]
    execute(instructions,registers)

    print("Final Registers: %s" % (registers,))
