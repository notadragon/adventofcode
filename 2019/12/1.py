#!/usr/bin/env pypy

import argparse, re, itertools, collections, math, functools

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

lineRe = re.compile("<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>")

coords = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    coords.append( list( int(c) for c in m.groups()) )

print("Coords: %s" % (coords,))

def show(moons):
    for m in moons:
        print("pos=<x=%s, y=%s, z=%x>, vel=<x=%s, y=%s, z=%s>" % tuple(m) )

def advance(moons):
    output = [ m[:] for m in moons ]
    
    for i,j in itertools.combinations( range(0,len(moons)), 2):
        for axis in range(0,3):
            ipos = moons[i][0+axis]
            jpos = moons[j][0+axis]

            if ipos < jpos:
                output[i][3+axis] += 1
                output[j][3+axis] -= 1
            elif ipos > jpos:
                output[i][3+axis] -= 1
                output[j][3+axis] += 1

    for m in output:
        for axis in range(0,3):
            m[0+axis] += m[3+axis]
        
                
    return output

def showenergy(moons):
    energies = []
    for m in moons:
        pe = tuple((abs(c) for c in m[0:3]))
        ke = tuple((abs(v) for v in m[3:6]))
        pot = sum(pe)
        kin = sum(ke)
        energy = pot*kin
        energies.append(energy)
        showargs = pe + (pot,) + ke + (kin,pot,kin,energy,)
        print("pot: %s + %s + %s = %s;  kin: %s + %s + %s = %s;  total: %s * %s = %s" % showargs)
    totalenergy = sum(energies)
    print("Sum of total energy: %s + %s + %s + %s = %s" % (tuple(energies) + (totalenergy,)))
        
if args.p1:
    print("Doing part 1")

    moons = [ x + [0,0,0] for x in coords ]

    for i in range(0,1000):
        moons = advance(moons)

    print("After 1000 steps:")
    show(moons)
    showenergy(moons)
        

        
if args.p2:
    print("Doing part 2")

    states = [{},{},{}]

    moons = [ x + [0,0,0] for x in coords ]

    steps = 0
    doneaxis = {}
    while True:
        for axis in range(0,3):
            if axis in doneaxis:
                continue
            at = tuple(( (m[0+axis],m[3+axis],) for m in moons ))
            if at in states[axis]:
                print("%s duplicate of %s for axis %s" % (steps, states[axis][at], axis,))
                doneaxis[axis] = (states[axis][at], steps)
                break
            states[axis][at] = steps
        if len(doneaxis) == 3:
            break
        steps = steps + 1
        moons = advance(moons)

    def gcd(a,b):
        while b:
            a,b = b, a%b
        return a
        
    def lcm(a,b):
        return a*b // gcd(a,b)

    def lcm2(numbers):
        return functools.reduce(lcm, numbers)

    print("Done: %s" % (doneaxis,))
    print("Repeat expected at: %s" % (lcm2( (a[1] for a in doneaxis.values()) ) ,))
