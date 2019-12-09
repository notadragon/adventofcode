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

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals = [ int(c) for c in x.split(",") ]

#print("Vals: %s" % (vals,))

def genoutput(values, input):
    ipos = 0
    pos = 0
    vals = list(values)
    while True:
        if pos >= len(vals):
            return
        instruction = vals[pos]
        opcode = instruction % 100
        pmode = instruction / 100
        if opcode == 99:
            return
        elif opcode == 1:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 + i2
            pos = pos + 4
        elif opcode == 2:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 * i2
            pos = pos + 4
        elif opcode == 3:
            (i1,) = params(pmode, (0,), pos+1, vals)
            if ipos >= len(input):
                yield None
            vals[i1] = input[ipos]
            ipos = ipos + 1
            pos = pos + 2
        elif opcode == 4:
            (i1,) = params(pmode, (1,), pos+1, vals)
            yield i1
            pos = pos + 2
        elif opcode == 5:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 != 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 6:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 == 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 7:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 < i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 8:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 == i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        else:
            print("Unknown opcode: %s" % (opcode,))
            return

if args.p1:
    print("Doing part 1")

    
if args.p2:
    print("Doing part 2")
