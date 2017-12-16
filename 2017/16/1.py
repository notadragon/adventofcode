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

commands = open(args.input).readlines()[0].strip().split(",")

if args.input[0] == "s":
    plen = 5
else:
    plen = 16
    
spinRe = re.compile("s(\d+)")
exchangeRe = re.compile("x(\d+)/(\d+)")
partnerRe = re.compile("p([a-z])/([a-z])")

def dance(programs):
    
    for c in commands:
        #print "Programs: %s" % (programs,)
        m = spinRe.match(c)
        if m:
            sval = int(m.group(1))

            programs = programs[-sval:] + programs[:-sval]
            continue

        m = exchangeRe.match(c)
        if m:
            f = int(m.group(1))
            t = int(m.group(2))

            tmp = programs[f]
            programs[f] = programs[t]
            programs[t] = tmp
            
            continue

        m = partnerRe.match(c)
        if m:
            f = m.group(1)
            t = m.group(2)

            for i in range(0,len(programs)):
                if programs[i] == f:
                    programs[i] = t
                elif programs[i] == t:
                    programs[i] = f
            
            continue

        print "Invalid command: %s" % (c,)

    return programs

if args.p1:
    print "Doing part 1"

    programs = [ chr(ord('a') + i) for i in range(0,plen) ]

    programs = dance(programs)
    
    print "Final programs: %s" % ("".join(programs),)

if args.p2:
    print "Doing part 2"

    def dancer(x):
        yield tuple(x)
        while True:
            x = dance(x)
            yield tuple(x)


    d = dancer([ chr(ord('a') + i) for i in range(0,plen) ])
        
    dances = [d.next(),d.next()]
    while dances[0] != dances[-1]:
        dances.append(d.next())
    del dances[-1]
    
    print "Cycle length: %s" % (len(dances),)

    for i in range(0,len(dances)):
        print "%14s:%s" % (i,"".join(dances[i]),)

    limit = 1000000000
    print "%14s:%s" % (limit,"".join(dances[limit % len(dances)]),)
    
