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

lineRe = re.compile("^([%&]?)([a-z]+) -> ([a-z, ]+).*$")

modules = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    modules.append( (m.group(1), m.group(2), tuple( x.strip() for x in m.group(3).split(",") ), ) )

#for d in modules:
#    print(f"{d}")
                   
if args.p1:
    print("Doing part 1")

    flipflops = {}
    conjunctions = {}
    broadcasters = {}

    for d in modules:
        if d[0] == "%":
            flipflops[d[1]] = [ False, d[2] ]
        elif d[0] == "&":
            conjunctions[d[1]] = [ {}, d[2] ]
        else:
            broadcasters[d[1]] = [ None, d[2] ]

    for d in modules:
        for t in d[2]:
            if t in conjunctions:
                conjunctions[t][0][d[1]] = False

    pulses = collections.deque()
    lowpulses = 0
    highpulses = 0

    for i in range(0,1000):
        pulses.append( ( "button", False, "broadcaster" ) )

        while pulses:
            source, ptype, dest = pulses.popleft()
            if ptype:
                highpulses = highpulses + 1
                ptname = "high"
            else:
                lowpulses = lowpulses + 1
                ptname = "low"
            #print(f"Pulse: {source} -{ptname}-> {dest}")
            
            if dest in broadcasters:
                targets = broadcasters[dest][1]
                for t in targets:
                    pulses.append( (dest, ptype, t) )
            elif dest in flipflops:
                d = flipflops[dest]
                if not ptype:
                    # low pulse flips
                    d[0] = not d[0]
                    tosend = d[0]
                    for t in d[1]:
                        pulses.append( (dest, tosend, t) )
            elif dest in conjunctions:
                d = conjunctions[dest]
    
                d[0][source] = ptype
    
                allhigh = True
                for v in d[0].values():
                    allhigh = allhigh and v
                if allhigh:
                    tosend = False
                else:
                    tosend = True
    
                for t in d[1]:
                    pulses.append( ( dest, tosend, t) )

        
                    
    print(f"Low pulses: {lowpulses}")
    print(f"High pulses: {highpulses}")

    print(f"Product: {lowpulses * highpulses}")
    
if args.p2:
    print("Doing part 2")
    
    
    flipflops = {}
    conjunctions = {}
    broadcasters = {}

    for d in modules:
        if d[0] == "%":
            flipflops[d[1]] = [ False, d[2] ]
        elif d[0] == "&":
            conjunctions[d[1]] = [ {}, d[2] ]
        else:
            broadcasters[d[1]] = [ None, d[2] ]

    for d in modules:
        for t in d[2]:
            if t in conjunctions:
                conjunctions[t][0][d[1]] = False

    pulses = collections.deque()
    lowpulses = 0
    highpulses = 0

    buttonpresses = 0
    rxpulses = 0

    while rxpulses == 0:
        pulses.append( ( "button", False, "broadcaster" ) )
        buttonpresses = buttonpresses + 1

        if buttonpresses % 100000 == 0:
            print(f"Button Presses: {buttonpresses}")

        while pulses:
            source, ptype, dest = pulses.popleft()
            if ptype:
                highpulses = highpulses + 1
                ptname = "high"
            else:
                lowpulses = lowpulses + 1
                ptname = "low"
            #print(f"Pulse: {source} -{ptname}-> {dest}")

            if not ptype and dest == "rx":
                rxpulses = rxpulses + 1
            
            if dest in broadcasters:
                targets = broadcasters[dest][1]
                for t in targets:
                    pulses.append( (dest, ptype, t) )
            elif dest in flipflops:
                d = flipflops[dest]
                if not ptype:
                    # low pulse flips
                    d[0] = not d[0]
                    tosend = d[0]
                    for t in d[1]:
                        pulses.append( (dest, tosend, t) )
            elif dest in conjunctions:
                d = conjunctions[dest]
    
                d[0][source] = ptype
    
                allhigh = True
                for v in d[0].values():
                    allhigh = allhigh and v
                if allhigh:
                    tosend = False
                else:
                    tosend = True
    
                for t in d[1]:
                    pulses.append( ( dest, tosend, t) )

        
                    
    print(f"Low pulses: {lowpulses}")
    print(f"High pulses: {highpulses}")


    print(f"Button Presses: {buttonpresses}")
    print(f"Rx pulses: {rxpulses}")

    
