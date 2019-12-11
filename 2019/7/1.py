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
    vals = [int(v) for v in x.split(",") ]

print("Vals: %s" % (vals,))

def params(pmode, paramtypes, pos, values):
    #print("pmode: %s paramtypes: %s pos: %s values: %s" % (pmode, paramtypes, pos, values,))
    output = []
    i = 0
    while i < len(paramtypes):
        p = values[pos + i]
        imode = pmode % 10
        itype = paramtypes[i]
        #print("i: %s pmode: %s itype: %s imode: %s p: %s" % (i,pmode,itype,imode,p,))
        if itype == 1:
            if imode == 0:
                p = values[p]
        output.append(p)
        i = i + 1
        pmode /= 10
    #print("output: %s" % (output,))
    return tuple(output)

def runprogram1(values, input):
    output = []
    pos = 0
    vals = list(values)
    while True:
        if pos >= len(vals):
            return (vals,output)
        instruction = vals[pos]
        opcode = instruction % 100
        pmode = instruction / 100
        if opcode == 99:
            return (vals,output)
        elif opcode == 1:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 + i2
            pos = pos + 4
        elif opcode == 2:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 * i2
            pos = pos + 4
        elif opcode == 3:
            (i1,) = params(pmode, (0,), pos+1, vals)
            vals[i1] = input.next()
            pos = pos + 2
        elif opcode == 4:
            (i1,) = params(pmode, (1,), pos+1, vals)
            output.append(i1)
            pos = pos + 2
        elif opcode == 5:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 != 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 6:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 == 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 7:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 < i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 8:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 == i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        else:
            print("Unknown opcode: %s" % (opcode,))
            return (vals,output)
        
if args.p1:
    print("Doing part 1")

    maxsettings = None
    maxival = 0
    
    for settings in itertools.permutations( range(0,5) ):
        ival = 0

        for s in settings:
            vs,output = runprogram1(vals, iter([s,ival]))
            ival = output[0]

        if ival > maxival:
            maxival = ival
            maxsettings = settings

    print("MaxSettings: %s" % (maxsettings,))
    print("MaxIval; %s" % (maxival,))
    
def genoutput(values, input):
    ipos = 0
    pos = 0
    vals = list(values)
    while True:
        if pos >= len(vals):
            return
        instruction = vals[pos]
        opcode = instruction % 100
        pmode = instruction / 100
        if opcode == 99:
            return
        elif opcode == 1:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 + i2
            pos = pos + 4
        elif opcode == 2:
            i1,i2,i3 = params(pmode, (1,1,0), pos+1, vals)
            vals[i3] = i1 * i2
            pos = pos + 4
        elif opcode == 3:
            (i1,) = params(pmode, (0,), pos+1, vals)
            if ipos >= len(input):
                yield None
            vals[i1] = input[ipos]
            ipos = ipos + 1
            pos = pos + 2
        elif opcode == 4:
            (i1,) = params(pmode, (1,), pos+1, vals)
            yield i1
            pos = pos + 2
        elif opcode == 5:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 != 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 6:
            (i1,i2) = params(pmode, (1,1,), pos+1, vals)
            if i1 == 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 7:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 < i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 8:
            (i1,i2,i3) = params(pmode, (1,1,0), pos+1, vals)
            if i1 == i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        else:
            print("Unknown opcode: %s" % (opcode,))
            return

if args.p2:
    print("Doing part 2")

    maxsettings = None
    maxival = 0
    
    for settings in itertools.permutations( range(5,10) ):
        ival = 0

        inputs = [None] * 5
        outputs = [0] * 5

        gens = [None] * 5

        for i in range(0,5):
            inputs[i] = [settings[i]]
            gens[i] = genoutput(vals, inputs[i])

        inputs[0].append(0)
        
        i = 0
        while True:
            if gens[i] == None:
                break
            
            j = (i + 1) % 5

            needInput = False
            for nval in gens[i]:
                if nval == None:
                    needInput = True
                    break
                else:
                    outputs[i] = nval
                    inputs[j].append(nval)

            if not needInput:
                gens[i] = None

            i = j

        #print("Settings: %s" % (settings,))
        #print("Inputs: %s" % (inputs,))
        #print("Outputs: %s" % (outputs,))
            
        if outputs[-1] > maxival:
            maxival = outputs[-1]
            maxsettings = settings

    print("MaxSettings: %s" % (maxsettings,))
    print("MaxIval; %s" % (maxival,))
    
