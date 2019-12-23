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
    blocks = 0
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

            if ival == -1:
                blocks = blocks + 1
                if blocks > 2:
                    yield None
            
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

class Computer:
    def __init__(self, n):
        self.inputs = collections.deque()
        self.inputs.append(n)

        self.gen = genoutput(instructions[:], self)
        
    def next(self):
        if not self.inputs:
            return -1
        else:
            return self.inputs.popleft()

    def handlePacket(self,p):
        self.inputs.append(p[1])
        self.inputs.append(p[2])

    def run(self):
        for p in self.gen:
            if p == None:
                return None
            x = next(self.gen)
            y = next(self.gen)
            #print("Pruduced packet:%s" % ( (p,x,y,), ) )
            return (p,x,y)

if args.p1:
    print("Doing part 1")

    computers = []
    
    for i in range(0,50):
        computers.append(Computer(i))

    lastNat = None
    done = False
    sentY = set()
    while not done:
        any = False
        for c in computers:
            p = c.run()
            if p == None:
                continue
            any = True
            if p[0] == 255:
                print("Packet for 255: %s" % (p,))
                lastNat = p
                continue
            computers[p[0]].handlePacket(p)

        if not any:
            print("Sending from NAT: %s" % (lastNat,))
            if lastNat[2] in sentY:
                print("  Double Y!")
            sentY.add(lastNat[2])
            computers[0].handlePacket(lastNat)
        
    
if args.p2:
    print("Doing part 2")
