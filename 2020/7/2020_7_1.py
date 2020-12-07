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

lineRe = re.compile("(.*) bags contain ((no other bags)|(\d+) (.*) bags?(, (\d+) (.*)bags?)*)\.")
cRe = re.compile(" ?(\d+) (.*) bags?")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    bc = m.group(1)
    contents = m.group(2)
    if contents == "no other bags":
        data.append( (bc, []) )
    else:
        cd = []
        for cb in contents.split(","):
            m2 = cRe.match(cb)
            cd.append( (m2.group(2),int(m2.group(1)),))
        data.append( (bc, cd) )

datamap = {}        
for bc,cd in data:
    datamap[bc] = { cbc : cbcount for cbc,cbcount in cd }

if args.p1:
    print("Doing part 1")

    foundcolors = set()
    colors = [ "shiny gold" ]

    while colors:
        c = colors[0]
        foundcolors.add(c)
        del colors[0]

        for bc,bcc in datamap.items():
            if bc in foundcolors or bc in colors:
                continue
            if c in bcc:
                colors.append(bc)

    print("Found colors: %s" % (len(foundcolors)-1,))
                
if args.p2:
    print("Doing part 2")

    def numbags(datamap, bc):
        bcc = datamap[bc]
        output = 0
        for cbc,cbcount in bcc.items():
            cbn = numbags(datamap,cbc)
            output += cbcount * cbn
        return output + 1

    print("Num bags: %s" % (numbags(datamap,"shiny gold")- 1,))
