#!/usr/bin/env pypy

import argparse, re, itertools

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

lineRe = re.compile("(.*) would (gain|lose) ([0-9]+) happiness units by sitting next to (.*)\\.")

people = set()
ivals = {}

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue

    if m.group(2) == "gain":
        offset = int(m.group(3))
    else:
        offset = -int(m.group(3))
    ivals[ (m.group(1),m.group(4),) ] = offset
    people.add(m.group(1))
    people.add(m.group(4))
    
#print("Ivals:%s" % (ivals,))

def happiness(ivals,p):
    output = 0
    for i in range(0,len(p)):
        p1 = p[i]
        if i == len(p) - 1:
            p2 = p[0]
        else:
            p2 = p[i+1]

        output += ivals[ (p1,p2) ] + ivals[ (p2,p1) ]
    return output
        
#for p in itertools.permutations(people):
#    print ("%s -> %s" % (p, happiness(ivals,p),))

if args.p1:
    print("Doing part 1")

    maxhap = max([ happiness(ivals,p) for p in itertools.permutations(people) ])
    print("MaxHap:%s" % (maxhap,))
    
if args.p2:
    print("Doing part 2")

    p2vals = dict(ivals)
    p2people = set(people)
    
    for p in people:
        p2vals[ ("me",p) ] = 0
        p2vals[ (p,"me") ] = 0
        
    p2people.add("me")

    maxhap = max([ happiness(p2vals,p) for p in itertools.permutations(p2people) ])
    print("MaxHap:%s" % (maxhap,))
