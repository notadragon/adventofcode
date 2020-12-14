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

lineRe = re.compile("(mem\[(\d+)\] = (\d+))|(mask = ([01X]+))")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        data.append( ( "mem", int(m.group(2)), int(m.group(3)), ) )
    else:
        data.append( ( "mask", m.group(5), ) )

#for d in data:
#    print("%s" % (d,))

def parsemask(mask):
    bit = 1
    ormask = 0
    andmask = (1 << 36) - 1
    for i in range(len(mask)-1, -1, -1):
        val = mask[i]
        if val == "1":
            ormask = ormask | bit
        elif val == "0":
            andmask = andmask & ~bit
        bit = bit << 1

    return ormask,andmask
    
if args.p1:
    print("Doing part 1")

    memory = {}
    
    mask = None
    for d in data:
        if d[0] == "mask":
            mask = d[1]
            ormask,andmask = parsemask(mask)
            #print("Mask: %s\n  OR: %36s\n AND: %36s\n" % (mask,format(ormask,"08b"),format(andmask,"08b"),))

        elif d[0] == "mem":
            val = d[2]
            val = val & andmask
            val = val | ormask
            
            memory[d[1]] = val
            #print("%s -> %s" % (d[1], val,))

    finalsum = sum(memory.values())
    print("Final Sum: %s" % (finalsum,))
    
def parsemask2(mask):
    bit = 1
    ormask = 0
    floatmask = 0
    andmask = (1 << 36) - 1
    for i in range(len(mask)-1, -1, -1):
        val = mask[i]
        if val == "1":
            ormask = ormask | bit
        elif val == "0":
            pass
            #andmask = andmask & ~bit
        elif val == "X":
            floatmask = floatmask | bit
            andmask = andmask & ~bit
        bit = bit << 1

    return ormask,andmask,floatmask
    
if args.p2:
    print("Doing part 2")

    memory = {}
    
    def iterbits(mask):
        bit = 1
        while mask != 0:
            if mask & 1:
                yield bit
            bit <<= 1
            mask >>= 1
                
    def iterfloats(floatmask):
        bits = [ x for x in iterbits(floatmask) ]
        #print("Bits: %s" % (bits,))

        andmask = (1 << 36) - 1
        for b in bits:
            andmask = andmask & ~b
        
        for j in range(0,1 << len(bits)):
            toset = 0
            ormask = 0

            i = j
            bitindex = 0
            while i != 0:
                if i & 1:
                    ormask = ormask | bits[bitindex]
                bitindex = bitindex + 1
                i = i >> 1

            #print("%s: %s, %s" % (j, andmask, ormask,))
            yield (andmask, ormask,)
    
    for d in data:
        if d[0] == "mask":
            mask = d[1]
            ormask,andmask,floatmask = parsemask2(mask)
            #print("Mask: %s\n  OR: %36s\n AND: %36s\n FLT: %36s\n" % (mask,format(ormask,"08b"),format(andmask,"08b"),format(floatmask,"08b"),))
        elif d[0] == "mem":
            addr = d[1]
            val = d[2]

            #print("addr: %s val: %s" % (format(addr,"08b"),val,))
            
            addr = addr & andmask
            addr = addr | ormask
            #print("maskaddr: %s" % (format(addr,"08b"),))
            for fandmask,formask in iterfloats(floatmask):
                #print("fandmask: %s  formask: %s" % (format(fandmask,"08b"), format(formask,"08b"),))
                outaddr = addr
                outaddr = outaddr & fandmask
                outaddr = outaddr | formask
                memory[outaddr] = val
                #print("%s[%s] -> %s" % (format(outaddr,"08b"), outaddr, val,) )

    finalsum = sum(memory.values())
    print("Final Sum: %s" % (finalsum,))
