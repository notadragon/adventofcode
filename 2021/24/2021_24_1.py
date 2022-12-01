#!/usr/bin/env pypy3

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')
parser.add_argument("--pt",dest="pt",action='store_true')
parser.add_argument("--pt2",dest="pt2",action='store_true')

args = parser.parse_args()

if not args.p1 and not args.p2 and not args.pt and not args.pt2: 
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("(add|div|eql|inp|mod|mul) ([a-z])(?: (-?[a-z0-9]+))?")

instructions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(3) != None:
        instructions.append( (m.group(1), m.group(2), m.group(3), ) )
    else:
        instructions.append( (m.group(1), m.group(2), ) )

#for instr in instructions:
#    print(f"{instr}")

varindex = {
    "w" : 0,
    "x" : 1,
    "y" : 2,
    "z" : 3,
}

def runInstructions(instructions, inp):
    variables = [ 0, 0, 0, 0 ]
    ndx = 0
    
    def getval(val):
        if val in "wxyz":
            return variables[varindex[val]]
        else:
            return int(val)

    def setvar(var, val):
        variables[varindex[var]] = val
        
            
    for instr in instructions:
        if instr[0] == "inp":
            setvar(instr[1], inp[ndx])
            ndx = ndx + 1
        elif instr[0] == "add":
            setvar(instr[1], getval(instr[1]) + getval(instr[2]))
        elif instr[0] == "mul":
            setvar(instr[1], getval(instr[1]) * getval(instr[2]))
        elif instr[0] == "div":
            mul = 1
            v1 = getval(instr[1])
            v2 = getval(instr[2])
            if v1 < 0:
                v1 = -v1
                mul *= -1
            if v2 < 0:
                v2 = -v2
                mul *= -1
                
            setvar(instr[1], mul * (v1 // v2))
        elif instr[0] == "mod":
            setvar(instr[1], getval(instr[1]) % getval(instr[2]))
        elif instr[0] == "eql":
            v1 = getval(instr[1])
            v2 = getval(instr[2])
            if v1 == v2:
                setvar(instr[1],1)
            else:
                setvar(instr[1],0)

        #print(f"{instr} -> {variables}")
                
    return variables

def strmnum(mnum):
    return "".join(str(d) for d in mnum)

def decrmnum(mnum):
    output = list(mnum)

    output[-1] = output[-1] - 1
    ndx = -1
    while output[ndx] == 0:
        output[ndx] = 9
        output[ndx-1] = output[ndx-1] - 1
        ndx = ndx - 1

    return tuple(output)
        
def incrmnum(mnum):
    output = list(mnum)

    output[-1] = output[-1] + 1
    ndx = -1
    while output[ndx] == 10:
        output[ndx] = 1
        output[ndx-1] = output[ndx-1] + 1
        ndx = ndx - 1

    return tuple(output)

if False and args.p1:
    print("Doing part 1")

    mnum = (9,) * 14

    while True:
        result = runInstructions(instructions, iter(mnum) )
        #print(f"{strmnum(mnum)} -> {result}")

        zval = result[varindex["z"]]

        if zval == 0:
            print(f"{mnum} -> {result}")
            print(f"Largest number: {strmnum(mnum)}")
            break
        
        mnum = decrmnum(mnum)

        
if False and args.p2:
    print("Doing part 2")

    mnum = (1,) * 14
        
    while True:
        result = runInstructions(instructions, iter(mnum) )
        #print(f"{strmnum(mnum)} -> {result}")
        
        zval = result[varindex["z"]]

        if zval == 0:
            print(f"{mnum} -> {result}")
            print(f"Smallest number: {strmnum(mnum)}")
            break
        
        mnum = incrmnum(mnum)


if args.pt:
    print("Doing testing")

    mnum = (9,9,9,9,9,7,9,5,9,1,9,4,5,6)
    mnum = (1,9,9,9,9,7,9,5,9,1,9,4,5,1)

    #mnum = (1,) * 14

    while True:
        result = runInstructions(instructions, mnum )
        print(f"{strmnum(mnum)} -> {result}")
        
        print(f"{mnum} -> {result}")
        print(f"Number: {strmnum(mnum)}")
        break
        
        nmnum = incrmnum(mnum)

        if nmnum[-6] != mnum[-6]:
            print(f"{strmnum(mnum)} -> {result}")
        
        mnum = nmnum

def analyze(instructions):
    expectedInstructions = (
        ( "inp","w", ),
        ( "mul", "x", "0", ),
        ( "add", "x", "z", ),
        ( "mod", "x", "26", ),
        ( "div", "z", "Z", ),  # z offset
        ( "add", "x", "X", ),  # x offset
        ( "eql", "x", "w", ),
        ( "eql", "x", "0", ),
        ( "mul", "y", "0", ),
        ( "add", "y", "25", ),
        ( "mul", "y", "x", ),
        ( "add", "y", "1", ),
        ( "mul", "z", "y", ),
        ( "mul", "y", "0", ),
        ( "add", "y", "w", ),
        ( "add", "y", "Y", ),  # y offset
        ( "mul", "y", "x", ),
        ( "add", "z", "y", ),
        )

    offsets = []

    for i in range(0, len(instructions), len(expectedInstructions)):
        ioffsets = {}
        for j in range(0,len(expectedInstructions)):
            expected = expectedInstructions[j]
            found = instructions[i+j]

            if expected[0] != found[0]:
                print(f"Unexpected instruction {i+j}: {found[0]} != {expected[0]}")
            if expected[1] != found[1]:
                print(f"Unexpected argument 1 at instruction {i+j}: {found[1]} != {expected[1]}")
            if len(expected) != len(found):
                print(f"Unexpected argument count at instruction {i+j}: {len(found)} != {len(expected)}")
            if len(found) > 2:
                if expected[2] in "XYZ":
                    ioffsets[expected[2]] = int(found[2])
                elif expected[2] != found[2]:
                    print(f"Unexpected argument 2 at instruction {i+j}: {found[2]} != {expected[2]}")
        offsets.append(ioffsets)

    if len(offsets) != 14:
        print(f"Unexpected number of blocks: {len(offsets)}")

    equalities = {}
    zstack = []
    for i in range(0,len(offsets)):
        offset = offsets[i]
        #print(f"{offset}")

        if zstack:
            xval = (zstack[-1][0], zstack[-1][1] + offset["X"], )
        else:
            xval = (-1, offset["X"], )

        # when z==26 we just ensure that the x comparison holds
        if offset["Z"] == 26:
            # dividing, xval comparison must be true.
            equalities[i] = xval
            if xval[1] > 0:
                print(f"I{i} = I{xval[0]} + {xval[1]}")
            elif xval[1] < 0:
                print(f"I{i} = I{xval[0]} - {abs(xval[1])}")
            else:
                print(f"I{i} = I{xval[0]}")

            zstack.pop()
        else:
            #print(f"No equality?: {xval}")

            yval = (i, offset["Y"])
            zstack.append(yval)
            
    return equalities

def genFromEqualities(equalities, reverse):
    
    def genRest( prevtuple, equalities):
        if len(prevtuple) == 14:
            yield prevtuple
            return

        index = len(prevtuple)
        if index in equalities:
            equality = equalities[index]
            val = prevtuple[equality[0]] + equality[1]

            if val >= 1 and val <= 9:
                for t in genRest( prevtuple + (val,), equalities):
                    yield t
            
        else:
            if reverse:
                r = range(9,0,-1)
            else:
                r = range(1,10)
            for d in r:
                for t in genRest( prevtuple + (d,), equalities):
                    yield t

    for t in genRest( (), equalities):
        yield t

if args.p1 or args.p2:
    analysis = analyze(instructions)

    print("Doing part 1")

    for n in genFromEqualities(analysis, True):
        result = runInstructions(instructions, n )
        print(f"{strmnum(n)} -> {result}")
        break
    
    print("Doing part 2")
        

    for n in genFromEqualities(analysis, False):
        result = runInstructions(instructions, n )
        print(f"{strmnum(n)} -> {result}")
        break



def optimize(instructions):
    # peform the following optimizatinos to benefit range analysis
    #  'mul q 0' instructions move backwards as long as previous instruction does not use q
    #  'inp q' gets

    newinstructions = []

    # inp does not use existing value of the variable, set it to 0 before input so that set can move up.
    for instr in instructions:
        if instr[0] == "inp":
            newinstructions.append( ( "mul", instr[1], "0" ) )
        newinstructions.append(instr)

    # move up any variable clears to right after their value is used
    for ndx in range(0,len(newinstructions)):
        instr = newinstructions[ndx]
        if instr[0] == "mul" and instr[2] == "0":
            var = instr[1]
            tondx = ndx
            while tondx > 0 and not var in newinstructions[tondx-1]:
                newinstructions[tondx-1],newinstructions[tondx] = newinstructions[tondx],newinstructions[tondx-1]
                tondx = tondx - 1

    for ndx in range(0,len(newinstructions)):
        instr = newinstructions[ndx]
        if instr[0] == "inp":
            var = instr[1]
            tondx = ndx
            while tondx < len(newinstructions)-1 and not var in newinstructions[tondx+1]:
                newinstructions[tondx+1],newinstructions[tondx] = newinstructions[tondx],newinstructions[tondx+1]
                tondx = tondx + 1

    # setting to 0 at start is pointless
    while newinstructions[0][0] == "mul" and newinstructions[0][2] == "0":
        newinstructions = newinstructions[1:]
    
    return tuple(newinstructions)

def addinterval(vals, interval):
    yielded = False
    for v in vals:
        if yielded or v[1] < interval[0]-1:
            yield v
        elif v[0] > interval[1]+1:
            yielded = True
            yield interval
            yield v
        else:
            interval = ( min(interval[0],v[0]), max(interval[1],v[1]) )

    if not yielded:
        yield interval
        

class VRange:
    def __init__(self):
        self.vals = ()

    def add(self,v):
        return self.addRange(v,v)

    def addRange(self,b,e):
        output = VRange()
        output.vals = tuple(addinterval(self.vals,(b,e)))

        return output

    def __str__(self):
        if len(self.vals) > 10:
            return str(self.vals[0:10]) + "..."
        else:
            return str(self.vals)


    def __repr__(self):
        if len(self.vals) > 10:
            return str(self.vals[0:10]) + "..."
        else:
            return str(self.vals)

    def isZero(self):
        return self.vals == ( (0,0) )
        
    def isOne(self):
        return self.vals == ( (1,1) )
        
    def addop(self,other):
        if self.isZero():
            return other
        elif other.isZero():
            return self
        
        output = VRange()
        for i1 in self.vals:
            for i2 in other.vals:
                output = output.addRange( i1[0] + i2[0], i1[1] + i2[1] )
        return output

    def mulop(self,other):
        if self.isZero() or other.isZero():
            return VRange().add(0)
        output = VRange()
        for i1 in self.vals:
            for a in range(i1[0],i1[1]+1):
                for i2 in other.vals:
                    for b in range(i2[0],i2[1]+1):
                        output = output.add(a*b)
        return output

    def modop(self,other):
        output = VRange()
        for i1 in self.vals:
            for a in range(i1[0],i1[1]+1):
                for i2 in other.vals:
                    for b in range(i2[0],i2[1]+1):
                        output = output.add(a%b)
        return output

    def divop(self,other):
        if other.isOne():
            return self
        output = VRange()
        for i1 in self.vals:
            for v1 in range(i1[0],i1[1]+1):
                for i2 in other.vals:
                    for v2 in range(i2[0],i2[1]+1):
                        mul = 1
                        if v1 < 0:
                            mul *= -1
                        if v2 < 0:
                            mul *= -1
                        output = output.add( mul * (abs(v1) // abs(v2)) )
        return output

    def eqlop(self,other):
        if self.vals == other.vals:
            return VRange().add(1)

        n1 = 0
        n2 = 0
        while n1 < len(self.vals) and n2 < len(other.vals):
            i1 = self.vals[n1]
            i2 = other.vals[n2]
            if i1[1] < i2[0]:
                n1 = n1 + 1
                continue
            if i2[1] < i1[0]:
                n2 = n2 + 1
                continue

            return VRange().addRange(0,1)

        return VRange().add(0)


def testRanges():
    v = VRange()
    print(f"{v}")

    v = v.add(1)
    print(f"{v}")

    v = v.add(2)
    print(f"{v}")

    v = v.add(4)
    print(f"{v}")

    v = v.add(6)
    print(f"{v}")

    v = v.add(3)
    print(f"{v}")

    v = v.addRange(0,7)
    print(f"{v}")

    v = v.addRange(-4,-2)
    print(f"{v}")

    v2 = VRange().addRange(0,4)
    v3 = VRange().addRange(2,4)
    v4 = v2.addop(v3)
    print(f"{v2} + {v3} = {v4}")
    
            
def vranges(instructions):
    variables = [ VRange().add(0), VRange().add(0), VRange().add(0), VRange().add(0) ]
    ndx = 0
    
    def getval(val):
        if val in "wxyz":
            return variables[varindex[val]]
        else:
            return VRange().add(int(val))

    def setvar(var, val):
        variables[varindex[var]] = val
            
    for instr in instructions:
        if instr[0] == "inp":
            setvar(instr[1], VRange().addRange(1,9))
            ndx = ndx + 1
        elif instr[0] == "add":
            setvar(instr[1], getval(instr[1]).addop(getval(instr[2])))
        elif instr[0] == "mul":
            setvar(instr[1], getval(instr[1]).mulop(getval(instr[2])))
        elif instr[0] == "div":
            setvar(instr[1], getval(instr[1]).divop(getval(instr[2])))
        elif instr[0] == "mod":
            setvar(instr[1], getval(instr[1]).modop(getval(instr[2])))
        elif instr[0] == "eql":
            setvar(instr[1], getval(instr[1]).eqlop(getval(instr[2])))

        yield ( instr, tuple(variables) )
                
    return variables
    

if args.pt2:
    print("Doing testing 2")

    testRanges()
    
    optinstructions = optimize(instructions)

    for instr,variables in vranges(optinstructions):
        print(f"{instr} -> {variables}")
