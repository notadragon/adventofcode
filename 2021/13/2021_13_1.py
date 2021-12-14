#!/usr/bin/env python3

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

lineRe = re.compile("(?:(\d+),(\d+))|(?:fold along (x|y)=(\d+))")
data = []
folds = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        data.append( (int(m.group(1)), int(m.group(2)), ) )
    else:
        folds.append( (m.group(3),int(m.group(4)),) )

data = set(data)
folds = tuple(folds)

def show(data):
    data = set(data)
    minx = min([d[0] for d in data])
    miny = min([d[1] for d in data])
    maxx = max([d[0] for d in data])
    maxy = max([d[1] for d in data])

    for y in range(miny,maxy+1):
        r = []
        for x in range(minx,maxx+1):
            if (x,y) in data:
                r.append("#")
            else:
                r.append(".")
        print("".join(r))

def fold(data, foldspec):
    newdata = set()
    ft = foldspec[0]
    fv = foldspec[1]
    for d in data:
        if ft == "x":
            newd = (fv - abs(fv - d[0]), d[1],)
        else:
            newd = (d[0], fv - abs(fv - d[1]),)
        newdata.add(newd)
    return newdata
            
            
        
if args.p1:
    print("Doing part 1")

    d1 = fold(data,folds[0])

    print(f"Visible: {len(d1)}")
    
if args.p2:
    print("Doing part 2")

    fd = data
    for foldspec in folds:
        fd = fold(fd,foldspec)

    # I am too lazy to do character recognition.  Read this.
    print("Read this:")
    show(fd)
