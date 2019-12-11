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

lineRe = re.compile("(\d+)-(\d+)")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    instructions = [ int(c) for c in x.split(",") ]

print("Instructions: %s" % (instructions,))

class Input:
    def __init__(self,vals):
        self.ipos = 0
        self.vals = vals

    def next(self):
        if self.ipos < len(self.vals):
            ouput = self.vals[self.ipos]
            self.ipos = self.ipos + 1
            return output
        else:
            return None

headinglabels = {
    (0,-1) : "^",
    (0,1) : "v",
    (1,0) : ">",
    (-1,0) : "<",
    }
        
class Robot:
    def __init__(self):
        self.grid = {}
        self.loc = (0,0)
        self.heading = (0,-1)
        
    def handleOutput(self,o1,o2):
        if o1 == 0:
            self.grid[self.loc] = '.'
        else:
            self.grid[self.loc] = "#"

        if o2 == 0:
            self.heading = ( self.heading[1], -self.heading[0], )
        else:
            self.heading = ( -self.heading[1], self.heading[0], )

        self.loc = ( self.loc[0] + self.heading[0], self.loc[1] + self.heading[1], )

    def next(self):
        if self.loc in self.grid:
            under = self.grid[self.loc]
        else:
            under = "."

        if under == ".":
            return 0
        else:
            return 1

    def show(self):
        minx = min([x[0] for x in self.grid.keys()])
        miny = min([x[1] for x in self.grid.keys()])
        maxx = max([x[0] for x in self.grid.keys()])
        maxy = max([x[1] for x in self.grid.keys()])

        for y in range(miny,maxy+1):
            r = []
            for x in range(minx,maxx+1):
                g = self.grid.get( (x,y,), " ")
                r.append(g)
            print("".join(r))
                
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
        #print("pos: %s" % (pos,))
        #print("Vals: %s" % (vals,))
        instruction = vals.get(pos,0)
        opcode = instruction % 100
        pmode = instruction / 100
        if opcode == 99:
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

if args.p1:
    print("Doing part 1")

    r = Robot()
    
    g = genoutput(instructions, r)
    for o1 in g:
        o2 = next(g)
        r.handleOutput(o1,o2)

    r.show()

    print("Painted: %s" % (len(r.grid),))
    
if args.p2:
    print("Doing part 2")
    r = Robot()

    r.grid[r.loc] = "#"
    
    g = genoutput(instructions, r)
    for o1 in g:
        o2 = next(g)
        r.handleOutput(o1,o2)

    r.show()
