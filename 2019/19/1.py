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

if args.p1:
    print("Doing part 1")

    grid = []

    for n in itertools.count():
        for x in range(0,n+1):
            y = n-x

            #print("x,y: %s" % ((x,y,),))

            output = list(genoutput(instructions,iter([x,y])))

            if not output or len(output) > 1:
                print("TOO MUCH OUTPUT: %s" % (output,))
                
            while len(grid) <= y:
                grid.append([])
            while len(grid[y]) <= x:
                grid[y].append(" ")
            grid[y][x] = output[0]

        #for g in grid:
        #    print("".join( [ "#" if gg == 1 else "." for gg in g] ))

        if n > 100:
            break

    total = sum( [ sum(g[0:50]) for g in grid[0:50] ])
    print("Total: %s" % (total,))

    
if args.p2:
    print("Doing part 2")

    ranges = []

    def getvalue(x,y):
        return list(genoutput(instructions,iter([x,y])))[0]

    while True:
        y = len(ranges)

        if ranges and ranges[-1]:
            minx = ranges[-1][0]
        else:
            minx = 0

        startx = None
        for x in range(minx,y*2+5):
            if getvalue(x,y):
                startx = x
                break

        if startx == None:
            ranges.append(())
        else:
            endx = startx+1
            while getvalue(endx,y):
                endx = endx + 1

            ranges.append( (startx,endx,) )
            

        #print("y:%s range:%s" % (y,ranges[-1],))

        if ranges[-1]:
            height = 0
            bottom = len(ranges)
            left = ranges[bottom-1][0]
            while ranges[bottom-height-1][1] - left >= 100:
                height = height + 1

            #if height > 0:
            #    print("  height: %s" % (height,))

            if height == 100:
                top = bottom - 100
                right = left + 100

                print("(%s,%s) -> (%s,%s)" % (left, top, left+100, bottom,))
                print("Corner: %s  Value: %s" % ( (left,top,), left * 10000 + top, ))

                for sx,sy in itertools.product(range(left,right),range(top,bottom)):
                    if not getvalue(sx,sy):
                        print("Hole??? %s" % ((sx,sy,),))
                
                break
            
