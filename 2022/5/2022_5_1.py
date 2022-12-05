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

crates = {}
moves = []

lineRe = re.compile("(?:move ([0-9]+) from ([0-9]+) to ([0-9]+))|(?:(    |\\[[A-Z]\\])+)|([0-9 ]+)")

cratedefs = []
for x in open(args.input).readlines():
    x = x.rstrip()
    if not x:
        continue
        
    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    if m.group(1):
        moves.append( (int(m.group(1)), int(m.group(2)), int(m.group(3))))
    elif m.group(4) or m.group(5):
        cratedefs.append(x)

#for m in moves:
#    print(f"{m}")

for n,c in enumerate(cratedefs[-1]):
    if c == " ":
        continue

    cid = int(c)
    ciddata = []
    for cd in cratedefs[-2::-1]:
        if n >= len(cd) or cd[n] == " ":
            continue
        ciddata.append(cd[n])
    crates[cid] = tuple(ciddata)

def showcrates(cs):

    minkey = min(cs.keys())
    maxkey = max(cs.keys())

    lines = [ [] ]
    
    for i in range(minkey,maxkey+1):
        lines[-1].append(f"  {i} ")

        if i in cs:
            cd = cs[i]
        else:
            cd = []
            
        while len(lines) < len(cd) + 1:
            lines.insert(0, ["    ",] * (i - minkey))

        for n in range(0,len(lines)-1):
            if n < len(cd):
                lines[ len(lines)-2-n ].append(f" [{cd[n]}]")
            else:
                lines[ len(lines)-2-n ].append("    ")
                

    for l in lines:
        print("".join(l))


#showcrates(crates)

if args.p1:
    print("Doing part 1")

    cs = crates.copy()
    #showcrates(cs)
    for m in moves:
        q = m[0]
        fid = m[1]
        tid = m[2]

        fromd = cs[fid]
        tod = cs[tid]

        newfromd = fromd[:-q]
        newtod = tod + tuple(reversed(fromd[-q:]))

        cs[fid] = newfromd
        cs[tid] = newtod

        #showcrates(cs)

    
    minkey = min(cs.keys())
    maxkey = max(cs.keys())
    tops = []
    for i in range(minkey,maxkey+1):
        s = cs[i]
        tops.append(s[-1])
    tops = "".join(tops)

    print(f"CODE: {tops}")
    
if args.p2:
    print("Doing part 2")

    cs = crates.copy()
    #showcrates(cs)
    for m in moves:
        q = m[0]
        fid = m[1]
        tid = m[2]

        fromd = cs[fid]
        tod = cs[tid]

        newfromd = fromd[:-q]
        newtod = tod + fromd[-q:]

        cs[fid] = newfromd
        cs[tid] = newtod

        #showcrates(cs)

    
    minkey = min(cs.keys())
    maxkey = max(cs.keys())
    tops = []
    for i in range(minkey,maxkey+1):
        s = cs[i]
        tops.append(s[-1])
    tops = "".join(tops)

    print(f"CODE: {tops}")
    
