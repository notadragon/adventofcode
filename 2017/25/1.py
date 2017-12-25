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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

initstate = None
diagsteps = 0
states = {}

lineRe = re.compile("^ *(?:Begin in state ([A-Z]).)|(?:Perform a diagnostic checksum after ([0-9]+) steps.)|(?:(?:In state ([A-Z]):)|(?:If the current value is ([0-9]):)|(?:- Write the value ([0-9]).)|(?:- Move one slot to the (left|right).)|(?:- Continue with state ([A-Z]).))$")
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue
    
    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
        continue
        
    if m.group(1):
        initstate = m.group(1)
    elif m.group(2):
        diagsteps = int(m.group(2))
    elif m.group(3):
        s = m.group(3)
        if not s in states:
            states[s] = {}
    elif m.group(4):
        cv = int(m.group(4))
        if not cv in states[s]:
            states[s][cv] = {}
    elif m.group(5):
        states[s][cv]["wval"] = int(m.group(5))
    elif m.group(6):
        states[s][cv]["dir"] = m.group(6)
    elif m.group(7):
        states[s][cv]["next"] = m.group(7)

print "InitState: %s" % (initstate,)
print "Steps: %s" % (diagsteps,)
print "States: %s" % (states,)

def gentape(initstate,states):
    tape = {}
    pos = 0
    state = initstate
    step = 0
    
    while True:
        sdata = states[state]
        currentval = tape.get(pos,0)
        todo = sdata[currentval]
        tape[pos] = todo["wval"]
        if todo["dir"] == "left":
            pos = pos - 1
        else:
            pos = pos + 1
        state = todo["next"]

        step = step + 1

        yield (step,state,pos,tape)
            

if args.p1:
    print "Doing part 1"

    for step,state,pos,tape in gentape(initstate,states):
        if step == diagsteps:
            print "Checksum: %s" % (sum(tape.values()),)
            break
if args.p2:
    print "Doing part 2"
