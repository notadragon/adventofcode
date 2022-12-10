#!/usr/bin/env pypy3

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

lineRe = re.compile("^(noop|addx)(?: (-?[0-9]+))?$")
ops = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
        
    # Process input line
    if m.group(2):
        ops.append( (m.group(1), int(m.group(2))) )
    else:
        ops.append( (m.group(1),))

#for op in ops:
#    print(f"{op}")

def applyOp(op, state):
    if op[0] == "noop":
        return ( state[0] + 1, state[1], )
    elif op[0] == "addx":
        return ( state[0] + 2, state[1] + op[1], )
            

def states(initstate, ops):
    state = initstate
    yield initstate

    while True:
        for n,op in enumerate(ops):
            if op[0] == "noop":
                state = ( state[0] + 1, state[1], )
                yield state
            elif op[0] == "addx":
                state = ( state[0] + 1, state[1], )
                yield state
                state = ( state[0] + 1, state[1] + op[1], )
                yield state
    
if args.p1:
    print("Doing part 1")

    wanted = set([20,60,100,140,180,220])
    maxwanted = max(wanted)
    total = 0
    
    for state in states( (0,1), ops):
        if state[0]+1 in wanted:
            strength = (state[0] + 1) * state[1]
            #print(f"{state} -> {strength}")
            total = total + strength

        if state[0] > maxwanted:
            break

    print(f"total: {total}")
        
def printcrt(crt):
    for r in crt:
        print("".join(r))
    
if args.p2:
    print("Doing part 2")

    crt = []
    for y in range(0,6):
        crt.append( ["."] * 40 )

    printcrt(crt)

    for state in states( (0,1), ops):
        cycle = state[0] + 1

        drawx = ((cycle-1) % 40)
        drawy = ((cycle-1) // 40) % 6

        if drawx >= state[1]-1 and drawx <= state[1] + 1:
            crt[drawy][drawx] = "#"

        print(f"{(drawx,drawy)} -> {state}")

        if state[0] >= 239:
            break

    printcrt(crt)
