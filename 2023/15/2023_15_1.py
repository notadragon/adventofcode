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

lineRe = re.compile("^.*$")
instrRe = re.compile("^([a-z]+)(-|=[0-9]+)$")

initseq = []
instructions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    for e in x.split(","):
        m = instrRe.match(e)
        if not m:
            print(f"Invalid Instruction: {x}")

        initseq.append(e)
        instructions.append( (m.group(1), m.group(2)) )
        
#for instr in instructions:
#    print(f"{instr}")

if args.p1:
    print("Doing part 1")

    def hash(chars):
        current = 0
        for c in chars:
            ascii = ord(c)
            current = current + ascii
            current = (current * 17) % 256

        return current

    total = 0
    for i in initseq:
        total = total + hash(i)
    print(f"Total: {total}")
    
if args.p2:
    print("Doing part 2")

    boxes = [ ]
    for i in range(0,256):
        boxes.append([])
    
    for label, i in instructions:

        box = hash(label)
        if i == "-":
            boxes[box] = list([
                l for l in boxes[box] if l[0] != label 
                ])
        else:
            found = False
            length = int(i[1:])
            for l in boxes[box]:
                if l[0] == label:
                    found = True
                    l[1] = length
            if not found:
                boxes[box].append( [label, length] )

        #print(f"After \"{label}{i}\"")
        #for i in range(0,len(boxes)):
        #    if boxes[i]:
        #        print(f"Box {i}: {boxes[i]}")
            

    power = 0
    for b in range(0,len(boxes)):
        box = boxes[b]        
        for s in range(0,len(box)):
            l = box[s]
            lp = (1+b) * (1+s) * l[1]
            #print(f"{l[0]} : {1+b} (box {b}) * {1+s} (slot {s}) * {l[1]} (focal length) = {lp}")
            power = power + lp
    print(f"Power: {power}")
        
