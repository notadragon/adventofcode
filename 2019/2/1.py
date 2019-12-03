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

lineRe = re.compile("(\d+)(,\d+)*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    values = tuple([ int(y) for y in x.split(",") ])

print("Values: %s" % (values,))

def runprogram1(values):
    pos = 0
    vals = list(values)
    while True:
        opcode = vals[pos]
        if opcode == 99:
            return vals
        elif opcode == 1:
            i1 = vals[pos+1]
            i2 = vals[pos+2]
            i3 = vals[pos+3]
            vals[i3] = vals[i1] + vals[i2]
            pos = pos + 4
        elif opcode == 2:
            i1 = vals[pos+1]
            i2 = vals[pos+2]
            i3 = vals[pos+3]
            vals[i3] = vals[i1] * vals[i2]
            pos = pos + 4
        else:
            print("Unknown opcode: %s" % (opcode,))
            return vals
if args.p1:
    print("Doing part 1")

    p1vals = values[0:1] + (12,2) + values[3:]
    
    print("Input Vals: %s" % (p1vals,))
    vals = runprogram1(p1vals)
    print("Final Vals: %s" % (vals,))

    
if args.p2:
    print("Doing part 2")

    for noun,verb in itertools.product(range(0,100),range(0,100)):
        pvals = values[0:1] + (noun,verb) + values[3:]

        outvals = runprogram1(pvals)

        if outvals[0] == 19690720:
            print("Outvals: %s" % (outvals,))
            print("Found noun=%s verb=%s" % (noun,verb,))
            print("Result: %s" % ( 100 * noun + verb,))
            break    
