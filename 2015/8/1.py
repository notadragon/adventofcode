#!/usr/bin/env pypy

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
    args.p2 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lines = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    lines.append(x)

def decode(x):
    output = []
    i = 1
    while i < len(x)-1:
        c = x[i]
        i = i + 1
        
        if c == "\\":
            c2 = x[i]
            i = i + 1
            if c2 == "\\":
                output.append("\\")
            elif c2 == "\"":
                output.append("\"")
            elif c2 == "x":
                h1 = x[i]
                h2 = x[i+1]
                i = i + 2
                output.append(".")
            else:
                output.append("\\")
                output.append("\\")
        else:
            output.append(c)
    return "".join(output)

def encode(x):
    output = ["\""]

    for c in x:
        if c == "\"":
            output.append("\\\"")
        elif c == "\\":
            output.append("\\\\")
        else:
            output.append(c)
            
    output.append("\"")
            
    return "".join(output)

if args.p1:
    print("Doing part 1")

    filetotal = 0
    memtotal = 0
    for x in lines:
        y = decode(x)

        print( "%s -> %s" % (x,y,))
        filetotal += len(x)
        memtotal += len(y)

    print("FileTotal: %s" % (filetotal,))
    print("MemTotal: %s" % (memtotal,))
    print("Diff: %s" % (filetotal - memtotal,))
    
if args.p2:
    print("Doing part 2")

    filetotal = 0
    memtotal = 0
    for x in lines:
        y = encode(x)

        print( "%s -> %s" % (x,y,))
        filetotal += len(x)
        memtotal += len(y)

    print("FileTotal: %s" % (filetotal,))
    print("MemTotal: %s" % (memtotal,))
    print("Diff: %s" % (filetotal - memtotal,))
