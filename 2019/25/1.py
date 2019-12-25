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

lineRe = re.compile("(-?\d+)(?:,(-?\d+))*.*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    instructions = [ int(c) for c in x.split(",") ]

#print("Instructions: %s" % (instructions,))

def params(pmode, paramtypes, pos, relbase, values):
    #print("pmode: %s paramtypes: %s pos: %s values: %s" % (pmode, paramtypes, pos, values,))
    output = []
    i = 0
    while i < len(paramtypes):
        p = values.get(pos + 1 + i,0)
        imode = pmode % 10
        itype = paramtypes[i]
        #print("i: %s pmode: %s itype: %s imode: %s p: %s" % (i,pmode,itype,imode,p,))
        if itype == 1:
            if imode == 0:
                p = values.get(p,0)
            elif imode == 1:
                p = p
            elif imode == 2:
                p = values.get(p + relbase,0)
        elif itype == 0:
            if imode == 0:
                p = p
            elif imode == 2:
                p = p + relbase
        output.append(p)
        i = i + 1
        pmode /= 10
    #print("output: %s" % (output,))
    return tuple(output)

def genoutput(values, input):
    pos = 0
    relbase = 0
    vals = { i:v for i,v in enumerate(values) }
    while True:
        #print("Vals: %s" % (vals,))
        instruction = vals.get(pos,0)
        opcode = instruction % 100
        pmode = instruction / 100
        #print("pos: %s opcode: %s pmode: %s" % (pos,opcode, pmode, ))
        if opcode == 99:
            #print("HALTING")
            return
        elif opcode == 1:
            i1,i2,i3 = params(pmode, (1,1,0), pos, relbase, vals)
            vals[i3] = i1 + i2
            pos = pos + 4
        elif opcode == 2:
            i1,i2,i3 = params(pmode, (1,1,0), pos, relbase, vals)
            vals[i3] = i1 * i2
            pos = pos + 4
        elif opcode == 3:
            (i1,) = params(pmode, (0,), pos, relbase, vals)
            ival = input.next()
            if ival == None:
                yield None
                continue
            vals[i1] = ival
            pos = pos + 2
        elif opcode == 4:
            (i1,) = params(pmode, (1,), pos, relbase, vals)
            yield i1
            pos = pos + 2
        elif opcode == 5:
            (i1,i2) = params(pmode, (1,1,), pos, relbase, vals)
            if i1 != 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 6:
            (i1,i2) = params(pmode, (1,1,), pos, relbase, vals)
            #print("i1,i2: %s" % ( (i1,i2,), ) )
            if i1 == 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 7:
            (i1,i2,i3) = params(pmode, (1,1,0), pos, relbase, vals)
            if i1 < i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 8:
            (i1,i2,i3) = params(pmode, (1,1,0), pos, relbase, vals)
            if i1 == i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 9:
            (i1,) = params(pmode, (1,), pos, relbase, vals)
            relbase = relbase + i1
            pos = pos + 2
        else:
            print("Unknown opcode: %s" % (opcode,))
            return


class Bot:
    def __init__(self):
        self.input = collections.deque()

    def next(self):
        if self.input:
            return self.input.popleft()
        return None

    def addcommand(self,command):
        self.input.extend([ ord(c) for c in command])
        self.input.append(ord("\n"))
        
def testrun(n):

    k = [ False ] * 8

    for i in range(0,8):
        k[i] = n & (1 << i) != 0
    
    bot = Bot()
    bot.addcommand("north")
    if k[0]: bot.addcommand("take sand")
    bot.addcommand("north")
    #bot.addcommand("take escape pod")
    bot.addcommand("north")
    if k[1]: bot.addcommand("take astrolabe")
    bot.addcommand("south")
    bot.addcommand("south")
    bot.addcommand("west")
    bot.addcommand("west")
    if k[2]: bot.addcommand("take mutex")
    bot.addcommand("east")
    bot.addcommand("east")
    bot.addcommand("south")
    bot.addcommand("east")
    if k[3]: bot.addcommand("take klein bottle")
    bot.addcommand("east")
    if k[4]: bot.addcommand("take semiconductor")
    bot.addcommand("west")
    bot.addcommand("north")
    bot.addcommand("north")
    #bot.addcommand("take infinite loop")
    bot.addcommand("north")
    if k[5]: bot.addcommand("take dehydrated water")
    bot.addcommand("south")
    bot.addcommand("south")
    bot.addcommand("south")
    bot.addcommand("west")
    bot.addcommand("west")
    bot.addcommand("north")
    if k[6]: bot.addcommand("take shell")
    bot.addcommand("south")
    bot.addcommand("south")
    #bot.addcommand("take giant electromagnet")
    bot.addcommand("east")
    #bot.addcommand("take photons")
    bot.addcommand("south")
    #bot.addcommand("take molten lava")
    bot.addcommand("north")
    bot.addcommand("west")
    bot.addcommand("west")
    if k[7]: bot.addcommand("take ornament")
    bot.addcommand("west")
    bot.addcommand("south")
    bot.addcommand("inv")

    bot.addcommand("south")
    
    line = []
    for g in genoutput(instructions,bot):
        if g == None:
            break
        if g == ord("\n"):
            if not bot.input:
                print("".join([chr(c) for c in line]))
            line = []
        else:
            line.append(g)
        
if args.p1:
    print("Doing part 1")

    for i in range(0,255):
        print("TEST RUN: %s" % (i,))
        testrun(i)
    
if args.p2:
    print("Doing part 2")
