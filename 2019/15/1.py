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
            print("HALTING")
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

directions = {
    1 : (0, -1),
    2 : (0, 1),
    3 : (1, 0),
    4 : (-1, 0)
    }
    
        
class Drone:
    def __init__(self):
        self.grid = { (0,0) : "." }
        self.loc = (0,0)
        self.oloc = None
        self.heading = None
        self.inputs = collections.deque()
    
    def next(self):
        if self.inputs:
            output = self.inputs.popleft()
            self.heading = directions[output]

            #print("Sending input: %s" % (output,))
            return output
        return None

    def handleOutput(self,o1):
        if not self.heading:
            raise "OOPS"

        toloc = (self.loc[0] + self.heading[0], self.loc[1] + self.heading[1])
        if o1 == 0:
            self.grid[toloc] = "#"
        elif o1 == 1:
            self.grid [toloc] = "."
            self.loc = toloc
        elif o1 == 2:
            self.grid[toloc] = "O"
            self.loc = toloc
            self.oloc = toloc

        self.heading = None

    def show(self):
        minx = min([x[0] for x in self.grid.keys()])
        miny = min([x[1] for x in self.grid.keys()])
        maxx = max([x[0] for x in self.grid.keys()])
        maxy = max([x[1] for x in self.grid.keys()])

        for y in range(miny,maxy+1):
            r = []
            for x in range(minx,maxx+1):
                g = self.grid.get( (x,y,), " ")
                if (x,y) == self.loc:
                    g = "D"
                r.append(g)
            print("".join(r))

    def fill(self, source):
        filled = set( [ source ])
        tofill = set( [ source ])
        steps = 0
        while tofill:
            #print("Tofill: %s" % (tofill,))
            nexttofill = set()
            for edge in tofill:
                for i, heading in directions.items():
                    nextloc = ( edge[0] + heading[0], edge[1] + heading[1] )
                    if nextloc in filled:
                        continue
                    if nextloc not in self.grid:
                        continue
                    if self.grid[nextloc] == "#":
                        continue
                    nexttofill.add(nextloc)
                    filled.add(nextloc)
            tofill = nexttofill
            if nexttofill:
                steps = steps + 1
        return steps
            
    def travel(self, toloc):
        if toloc == self.loc:
            return

        #print("Travelling: %s -> %s" % (self.loc,toloc,))

        paths = {self.loc : ()}
        toexplore = set([ self.loc ])
        while toloc not in paths:
            #print("Paths: %s Toexplore: %s  " % (paths,toexplore,))
            nexttoexplore = set()
            for explore in toexplore:
                explorepath = paths[explore]
                for i,heading in directions.items():
                    explorenext = ( explore[0] + heading[0], explore[1] + heading[1])
                    if explorenext in paths:
                        continue
                    if explorenext not in self.grid:
                        continue
                    if self.grid[explorenext] == "#":
                        continue
                    paths[explorenext] = explorepath + (i,)
                    nexttoexplore.add(explorenext)
            toexplore = nexttoexplore

        #print("Paths: %s Toexplore: %s  " % (paths,toexplore,))
        #print("Travelling: %s -> %s : %s" % (self.loc,toloc,paths[toloc],))
        self.inputs.extend(paths[toloc])
        
            

def mag(loc):
    return abs(loc[0]) + abs(loc[1])
    
if True:
    instr = instructions[:]

    d = Drone()

    g = genoutput(instr, d)

    unknownlocs = set([d.loc])
    while unknownlocs:
        toloc = None
        for u in unknownlocs:
            if toloc == None or mag(u) < mag(toloc):
                toloc = u
        unknownlocs.remove(toloc)

        exploredir = None
        for i,heading in directions.items():
            if ( toloc[0] + heading[0], toloc[1] + heading[1] ) not in d.grid:
                exploredir = i
                break
        if exploredir == None:
            continue

        #print(" Going to %s, exploring %s" % (toloc, exploredir,))
        unknownlocs.add(toloc)
        d.travel(toloc)
        d.inputs.append(exploredir)

        #print("Inputs: %s" % (d.inputs,))
        
        for o1 in g:
            #print("Output: %s" % (o1,))
            if o1 == None:
                break
            d.handleOutput(o1)
            
        unknownlocs.add(d.loc)

    d.travel( (0,0) )
    for o1 in g:
        if o1 == None:
            break
        d.handleOutput(o1)
        
    d.show()
    
if args.p1:
    print("Doing part 1")

    d.travel(d.oloc)
    print("Steps to oxygen (%s): %s" % (d.oloc,len(d.inputs),))
    
if args.p2:
    print("Doing part 2")

    steps = d.fill(d.oloc)
    print("Steps to fill: %s" % (steps,))
