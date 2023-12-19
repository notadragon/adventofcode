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

lineRe = re.compile("^"
                    +"(?:\{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)\})"
                    +"|"
                    +"(?:([a-z]+)\{(.*)\})"
                    +"$")
compRe = re.compile("^(?:([a-zA-Z]+)|(?:([xmas])([><])([0-9]+):([a-zA-Z]+)))$")

workflows = []
parts = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        parts.append( { "x" : int(m.group(1)),
                        "m" : int(m.group(2)),
                        "a" : int(m.group(3)),
                        "s" : int(m.group(4)) } )
    else:
        k = m.group(5)
        ki = []
        for i in m.group(6).split(","):
            m2 = compRe.match(i)
            if not m2:
                print(f"Invalid comp: {i}")
            if m2.group(1):
                ki.append( (m2.group(1),) )
            else:
                ki.append( ( m2.group(2), m2.group(3), int(m2.group(4)), m2.group(5), ) )
        workflows.append( (k, tuple(ki), ) )

    
if args.p1:
    print("Doing part 1")

    wfs = { k : w for k,w in workflows }

    def applywfs(wfs, p):

        wf = "in"

        while True:
            if wf == "A" or wf == "R":
                return wf

            wfd = wfs[wf]

            print(f"{wf} : {wfd}")

            for instr in wfd:
                if len(instr) == 1:
                    wf = instr[0]
                    continue

                v = p[instr[0]]
                if instr[1] == "<":
                    if v < instr[2]:
                        wf = instr[3]
                        break
                elif instr[1] == ">":
                    if v > instr[2]:
                        wf = instr[3]
                        break
    
    total = 0
    for p in parts:
        result = applywfs(wfs, p)
        if result == "A":
            for v in p.values():
                total = total + v
    print(f"Total: {total}")

    
if args.p2:
    print("Doing part 2")

    def findall(wfs):

        accepted = []
        rejected = []

        pending = [
            ( {"x" : (1,4001),"m" : (1,4001),"a" : (1,4001),"s" : (1,4001)} , "in" )
            ]

        while pending:
            newpending = []

            for p,wf in pending:
                if wf == "A":
                    accepted.append(p)
                    continue
                if wf == "R":
                    rejected.append(p)
                    continue

                wfd = wfs[wf]
                for instr in wfd:
                    if len(instr) == 1:
                        newpending.append( (p,instr[0]) )
                        break
                    
                    r = p[instr[0]]
                    c = instr[2]

                    if instr[1] == "<":
                        if c <= r[0]:
                            match = None
                            rest = r
                        elif r[1] <= c:
                            match = r
                            rest = None
                        else:
                            match = (r[0],c)
                            rest = (c,r[1])
                    elif instr[1] == ">":
                        if r[0] > c:
                            match = r
                            rest = None
                        elif r[1] <= c:
                            match = None
                            rest = r
                        else:
                            match = (c+1,r[1])
                            rest = (r[0],c+1)
                            
                            
                    if match and match[0] < match[1]:
                        p2 = p.copy()
                        p2[instr[0]] = match
                        newpending.append( (p2,instr[3]) )
                        
                    if rest and rest[0] < rest[1]:
                        p2 = p.copy()
                        p2[instr[0]] = rest
                        p = p2
                    else:
                        break

            pending = newpending

        print(f"Accepted: {accepted}")
        print(f"Rejected: {rejected}")

        total = 0
        for p in accepted:
            pt = 1
            for v in p.values():
                pt = pt * (v[1] - v[0])
            total = total + pt
        print(f"Total: {total}")
        
    wfs = { k : w for k,w in workflows }

    findall(wfs)

    
