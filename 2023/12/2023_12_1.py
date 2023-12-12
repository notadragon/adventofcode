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

lineRe = re.compile("^([\?\.#]+) ([0-9,]+)$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (tuple(c for c in m.group(1)), tuple( int(z) for z in m.group(2).split(",") ),) )

#for d in data:
#    print(f"{d}")
    

cached = {}

def countOptions(spec,spans):
    key = (spec,spans)
    if key in cached:
        return cached[key]
    output = doCountOptions(spec,spans)
    cached[key] = output
    return output

def doCountOptions(spec, spans):
    if not spans:
        #print(f"  Ret: {spec} + {spans} -> 1")
        if "#" in spec:
            return 0
        else:
            return 1

    slen = spans[0]
    if len(spec) < slen:
        #print(f"  Ret: {spec} + {spans} -> 0")
        return 0

    output = 0

    remspans = spans[1:]
    if "." not in spec[0:slen] and (len(spec) == slen or spec[slen] in ".?"):
        output = output + countOptions(spec[slen+1:], spans[1:])

    if spec[0] != "#":
        remspec = spec[1:]
        while remspec and remspec[0] == ".":
            remspec = remspec[1:]
        if spec:
            output = output + countOptions(remspec, spans)

    #print(f"  Ret: {spec} + {spans} -> {output}")
        
    return output

if args.p1:
    print("Doing part 1")

    total = 0
    for d in data:
        c = countOptions(d[0], d[1])
        print(f"{d} -> {c}")
        total = total + c

    print(f"Total: {total}")
    
if args.p2:
    print("Doing part 2")

    total = 0
    for d in data:
        spec = list(d[0])
        for i in range(0,4):
            spec.append("?")
            spec.extend(d[0])

        md0 = tuple(spec)                
        md1 = d[1] * 5
        c = countOptions(md0, md1)
        print(f"{(md0,md1)} -> {c}")
        total = total + c

    print(f"Total: {total}")
