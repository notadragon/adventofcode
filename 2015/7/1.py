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

lineRe = re.compile("(?:([a-z]+|[0-9]+) )?(?:(AND|OR|LSHIFT|RSHIFT|NOT) )?([a-z]+|[0-9]+) -> ([a-z]+)")
instrs = {}

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = lineRe.match(x)
    if not m:
        print("invalid line: %s" % (x,))
        continue

    instrs[ m.group(4) ] = ( m.group(1), m.group(2), m.group(3), m.group(4),) 

#print("Instrs: %s" % (instrs,))

numRe = re.compile("[0-9]+")

def run(signals):
    def getval(signals,reg):
        if numRe.match(reg):
            return int(reg)
        elif reg in signals:
            return signals[reg]
        else:
            return None
    
    while True:
        numdone = 0

        for fromreg, op, toreg, wire in instrs.values():
            if not wire in signals:
                newval = None
                if not op:
                    toval = getval(signals,toreg)
                    if toval != None:
                        newval = toval
                elif op == "NOT":
                    toval = getval(signals,toreg)
                    if toval != None:
                        newval = ~toval
                elif op == "AND":
                    fromval = getval(signals,fromreg)
                    toval = getval(signals,toreg)
                    if fromval != None and toval != None:
                        newval = fromval & toval
                elif op == "OR":
                    fromval = getval(signals,fromreg)
                    toval = getval(signals,toreg)
                    if fromval != None and toval != None:
                        newval = fromval | toval
                elif op == "LSHIFT":
                    fromval = getval(signals,fromreg)
                    toval = getval(signals,toreg)
                    if fromval != None and toval != None:
                        newval = fromval << toval
                elif op == "RSHIFT":
                    fromval = getval(signals,fromreg)
                    toval = getval(signals,toreg)
                    if fromval != None and toval != None:
                        newval = fromval >> toval
                else:
                    print ("Unkonwn Op:%s" % (op,))
                if newval != None:
                    numdone += 1
                    signals[wire] = newval & 0xffff
                    

        if numdone == 0:
            break

#    for k in sorted(signals.keys()):
#        print ("%s: %s" % (k,signals[k],))
    
p1signals = {}
run(p1signals)

p2signals = {"b":p1signals["a"],}
run(p2signals)
             
if args.p1:
    print("Doing part 1")

    print("a: %s" % (p1signals["a"],))
    
if args.p2:
    print("Doing part 2")

    print("a: %s" % (p2signals["a"],))
