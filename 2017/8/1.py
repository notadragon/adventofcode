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

inputRe = re.compile("([a-z]+) (inc|dec) (-?[0-9]+) if ([a-z]+) ([<!=>]+) (-?[0-9]+)")

instructions = []
for x in open(args.input).readlines():
    x = x.strip()
    m = inputRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
    instructions.append([m.group(1),m.group(2),int(m.group(3)),m.group(4),m.group(5),int(m.group(6))])

if True:
    registers = {}
    for inst in instructions:
        registers[inst[0]] = 0
        registers[inst[3]] = 0

    maxEver = 0

    for inst in instructions:
        tval = registers[inst[3]]
        comp = inst[4]
        doit = False
        if comp == "==":
            if tval == inst[5]:
                doit = True
        elif comp == "<":
            if tval < inst[5]:
                doit = True
        elif comp == ">":
            if tval > inst[5]:
                doit = True
        elif comp == "!=":
            if tval != inst[5]:
                doit = True
        elif comp == ">=":
            if tval >= inst[5]:
                doit = True
        elif comp == "<=":
            if tval <= inst[5]:
                doit = True
        else:
            print "Unknown comp: %s" % (comp,)


        if doit:
            rval = registers[inst[0]]
            ract = inst[1]
            if ract == "inc":
                registers[inst[0]] = rval + inst[2]
            elif ract == "dec":
                registers[inst[0]] = rval - inst[2]
            else:
                print "Unknown action: %s" % (ract,)

            maxEver = max(maxEver,registers[inst[0]])
            
    print "Registers: %s" % (registers,)

if args.p1:
    print "Doing part 1"
    print "Max: %s" % (max(registers.values()),)

if args.p2:
    print "Doing part 2"
    print "MaxEver: %s" % (maxEver,)
