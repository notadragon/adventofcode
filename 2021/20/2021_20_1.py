#!/usr/bin/env pypy3

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

lineRe = re.compile("[\.#]+")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

enhancement = data[0]
inimage = data[1:]


def consider(imagem, loc):
    val = 0
    for delta in ( (-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1), ):
        dloc = ( loc[0] + delta[0],  loc[1] + delta[1] )
        dval = getval(imagem, dloc)
        val = val * 2 + dval
    return val

def imagemap(image):
    output = {}
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if image[y][x] == "#":
                output[ (x,y) ] = 1
    return ( 0, output )

def getval(imagem, loc):
    if loc in imagem[1]:
        return 1 - imagem[0]
    else:
        return imagem[0]

def parse(ichar):
    if ichar == "#":
        return 1
    else:
        return 0

def showchar(ival):
    if ival == 0:
        return "."
    else:
        return "#"
            
def stepImage(imagem, enhance):
    minx = min( k[0] for k in imagem[1].keys() )
    maxx = max( k[0] for k in imagem[1].keys() )
    miny = min( k[1] for k in imagem[1].keys() )
    maxy = max( k[1] for k in imagem[1].keys() )

    newimage = {}

    olddefault = imagem[0]
    if olddefault == 0:
        defaultenval = parse(enhance[0])
    else:
        defaultenval = parse(enhance[ 511 ])
    
    for y in range(miny-10, maxy+10):
        for x in range(minx-10, maxx+10):
            val = consider(imagem, (x,y))
            enval = parse(enhance[val])
            if enval != defaultenval:
                newimage[(x,y)] = enval
            #print(f"({x},{y}) -> {val} = {enhance[val]}")

    return ( defaultenval, newimage )

def show(imagem):
    minx = min( k[0] for k in imagem[1].keys() )
    maxx = max( k[0] for k in imagem[1].keys() )
    miny = min( k[1] for k in imagem[1].keys() )
    maxy = max( k[1] for k in imagem[1].keys() )

    for y in range(miny,maxy+1):
        row = []
        for x in range(minx,maxx+1):
            v = getval( imagem, (x,y) )
            row.append(showchar(v))
        print("".join(row))

if args.p1:
    print("Doing part 1")

    im = imagemap(inimage)
    show(im)
    im2 = stepImage(im, enhancement)
    show(im2)
    im3 = stepImage(im2, enhancement)
    show(im3)

    print(f"After 2 steps: {len(im3[1])}")
    
    
if args.p2:
    print("Doing part 2")

    im = imagemap(inimage)
    for i in range(0,50):
        im = stepImage(im, enhancement)
    print(f"After 50 steps: {len(im[1])}")
