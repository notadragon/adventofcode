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

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("(?:initial state: ([#\\.]+))|(?:([#\\.]+) => ([#\\.]))")

transitions = {}


for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        initialState = m.group(1)
    else:
        transitions[m.group(2)] = m.group(3)

print("Initial State: %s" % (initialState,))
print("Transitions: %s" % (transitions,))

def iterate(state):
    offset,values = state
    newvalues = []
    for i in range(offset-2,offset + len(values) + 3):
        start = i - 2
        if start < offset:
            key = ("." * (offset-start)) + values[0:5-offset+start]
        else:
            key = values[start-offset:start-offset+5]
            if len(key) < 5:
                key = key + ("." * (5-len(key)))
        newvalues.append( transitions.get(key,"."))
    retstart = 0
    while newvalues[retstart] == ".":
        retstart += 1
    newvalues = newvalues[retstart:]
    begin = offset - 2 + retstart

    while newvalues[-1] == ".":
        del newvalues[-1]

    return (begin,"".join(newvalues),)

def potvals(state):
    offset,values = state

    output = 0
    for i in range(0,len(values)):
        if values[i] == "#":
            output += (i + offset)
    return output

if args.p1:
    print("Doing part 1")

    states = []
    s = (0,initialState)
    states.append(s)
    for i in range(1,21):
        s = iterate(s)
        states.append(s)

    minoffset = min([s[0] for s in states])
    maxoffset = max([s[0] + len(s[1]) for s in states])

    prevv = None
    for i in range(0,len(states)):
        s = states[i]
        v = potvals(s)
        if prevv:
            vd = v - prevv
        else:
            vd = ""
        print("%2d: %s%s%s -> %s (%s)" % (i,("." * (s[0] - minoffset + 1)),s[1],("." * (maxoffset - len(s[1]) - s[0] + 1)),v,vd))

        prevv = v

def getStep(step):

    s = (0,initialState)

    mystep = 0
    while mystep != step:
        nexts = iterate(s)

        if s[1] == nexts[1]:
            #duplicate found
            stepoffset = nexts[0]  - s[0]
            s = (s[0] + ((step - mystep) * stepoffset), s[1],)
            mystep = step
        else:
            s = nexts
            mystep = mystep + 1
    return s
            
if args.p2:
    print("Doing part 2")

    for i in [ 20, 50000000000, ]:
        s = getStep(i)
        print("%s: %s - %s = %s" % (i, s[0], s[1], potvals(s),))
            
