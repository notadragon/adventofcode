#!/usr/bin/env pypy

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

lineRe = re.compile("(.*): (?:(\d+)-(\d+)) or (?:(\d+)-(\d+))|(\d+)(,\d+)*|your ticket:|nearby tickets:")

data = []
tickets = []

r = 1
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    if x == "your ticket:":
        r = 2
        continue
    elif x == "nearby tickets:":
        r = 3
        continue

    if r == 1:
        data.append( (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)),) )
    elif r == 2 or r == 3:
        tickets.append( [ int(y) for y in x.split(",") ] )

#for d in data:
#    print("%s" % (d,))

#for t in tickets:
#    print("%s" % (t,))

def getInvalid(t,data):
    output = []
    #print("Ticket: %s" % (t,))
    for v in t:
        #print("Value: %s" % (v,))
        good = False
        for d in data:
            #print("  Data: %s" % (d,))
            if d[1] <= v and v <= d[2]:
                #print("  %s <= %s <= %s" % (d[1], v, d[2]))
                good = True
                break
            if d[3] <= v and v <= d[4]:
                #print("  %s <= %s <= %s" % (d[3], v, d[4]))
                good = True
                break

        if not good:
            #print("  Invalid Value: %s" % (v,))
            output.append(v)
    return output

if args.p1:
    print("Doing part 1")

    invalidValues = [ getInvalid(t,data) for t in tickets[1:] ]
    total = 0
    for ivs in invalidValues:
        for v in ivs:
            total = total + v
    print("Error Rate: %s" % (total,))
    
if args.p2:
    print("Doing part 2")

    validTickets = [ t for t in tickets if not getInvalid(t,data) ]
    datamap = { d[0] : d[1:] for d in data }

    possibleFields = [ set(datamap.keys()) for t in tickets[0] ]
    for t in validTickets:
        #print("Valid Ticket: %s" % (t,))

        for i in range(0,len(possibleFields)):
            pf = possibleFields[i]
            tv = t[i]

            removeFields = []
            for f in pf:
                fd = datamap[f]
                good = False
                if fd[0] <= tv and tv <= fd[1]:
                    good = True
                if fd[2] <= tv and tv <= fd[3]:
                    good = True
                if not good:
                    removeFields.append(f)
            for f in removeFields:
                print("Removing Field: %s:%s" % (i,f,))
                pf.remove(f)

    modified = True
    while modified:
        modified = False
        
        for i in range(0,len(possibleFields)):
            if len(possibleFields[i]) == 1:
                found = next(iter(possibleFields[i]))
                for j in range(0,len(possibleFields)):
                    if j != i and found in possibleFields[j]:
                        possibleFields[j].remove(found)
                        modified = True

    product = 1
    for i in range(0,len(possibleFields)):
        print("%s: %s - %s" % (i,possibleFields[i],tickets[0][i]))

        f = next(iter(possibleFields[i]))
        if f.startswith("departure"):
            product *= tickets[0][i]
    print("Product: %s" %( product,))
        
