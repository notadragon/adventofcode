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

lineRe = re.compile("(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( ( True if m.group(1) == "on" else False, (int(m.group(2)),int(m.group(3)),), (int(m.group(4)),int(m.group(5)),), (int(m.group(6)),int(m.group(7)),), ) )

#for d in data:
#    print(f"{d}")

def oncells(seq):
    oncuboids = []

    def isinside(cb1, cb2):
        for dim in range(0,3):
            if not (cb1[dim][0] >= cb2[dim][0] and cb1[dim][1] <= cb2[dim][1]):
                return False
        return True
    
    def isoverlap(cb1,cb2):
        for dim in range(0,3):
            insiderange = ( max( cb1[dim][0], cb2[dim][0] ), min(cb1[dim][1], cb2[dim][1]), )
            #print(f"{cb1[dim]} i {cb2[dim]} -> {insiderange}")
            if insiderange[0] <= insiderange[1]:
                return True
        return False
        
    
    def nonintersect(cb1, cb2):
        # sequence of cuboids that make up cb1 but do not intersect cb2

        if not isoverlap(cb1,cb2):
            #print(f"No overlap: {cb1} != {cb2}")
            yield cb1
            return

        below = (cb1[0][0], min(cb1[0][1],cb2[0][0]-1))
        if below[0] <= below[1]:
            yield ( below, cb1[1], cb1[2], )
        above = (max(cb1[0][0], cb2[0][1]+1), cb1[0][1])
        if above[0] <= above[1]:
            yield( above, cb1[1], cb1[2], )

        inside = ( max( cb1[0][0], cb2[0][0] ), min(cb1[0][1], cb2[0][1]), )
        if inside[0] > inside[1]:
            return
        
        cb1 = ( inside, cb1[1], cb1[2], )

        below = (cb1[1][0], min(cb1[1][1],cb2[1][0]-1))
        if below[0] <= below[1]:
            yield ( cb1[0], below, cb1[2], )
        above = (max(cb1[1][0], cb2[1][1]+1), cb1[1][1])
        if above[0] <= above[1]:
            yield( cb1[0], above, cb1[2], )

        inside = ( max( cb1[1][0], cb2[1][0] ), min(cb1[1][1], cb2[1][1]), )
        if inside[0] > inside[1]:
            return

        cb1 = (cb1[0], inside, cb1[2], )

        below = (cb1[2][0], min(cb1[2][1],cb2[2][0]-1))
        if below[0] <= below[1]:
            yield ( cb1[0], cb1[1], below, )
        above = (max(cb1[2][0], cb2[2][1]+1), cb1[2][1])
        if above[0] <= above[1]:
            yield( cb1[0], cb1[1], above )

        inside = ( max( cb1[2][0], cb2[2][0] ), min(cb1[2][1], cb2[2][1]), )
        if inside[0] > inside[1]:
            return

        cb1 = (cb1[0], cb1[1], inside)
        # cb1 is now intesrsection

    def cbsize(cb):
        return (cb[0][1]-cb[0][0]+1) * (cb[1][1]-cb[1][0]+1) * (cb[2][1]-cb[2][0]+1)

    for d in seq:
        #print(f"{d}")

        newcuboids = []

        changecb = d[1:]

        if d[0]:
            contained = False
            for cb in oncuboids:
                if isinside(changecb, cb):
                    # surprisingly, with my input this never happens, so this optimization is actually pointless.
                    contained = True
                    continue
                
                for newcb in nonintersect(cb,changecb):
                    newcuboids.append(newcb)
            if not contained:
                newcuboids.append(changecb)
        else:
            for cb in oncuboids:
                for newcb in nonintersect(cb,changecb):
                    newcuboids.append(newcb)
            

        oncuboids = newcuboids

        #print(f"  Remaining Cuboids: {len(newcuboids)}")
        
    size = 0
    for cb in oncuboids:
        #print(f"on: {cb}")
        size = size + (cb[0][1]-cb[0][0]+1) * (cb[1][1]-cb[1][0]+1) * (cb[2][1]-cb[2][0]+1)
        
    return size

def oncells1(seq):
    def makepartitions(seq,n):
        bottoms = set( d[n+1][0] for d in seq )
        # convert to half-open ranges
        tops = set( d[n+1][1]+1 for d in seq )

        output = bottoms.union(tops)

        output = list(output)
        output.sort()
        return tuple(output)

    partitions = ( makepartitions(seq,0), makepartitions(seq,1), makepartitions(seq,2), )

    print(f"Partitions: {partitions}")

    oncuboids = set()
    
    for d in seq:
        #print(f"{d}")

        xsplits = [d[1][0],] + [ c for c in partitions[0] if c > d[1][0] and c <= d[1][1] ] + [d[1][1]+1,]
        ysplits = [d[2][0],] + [ c for c in partitions[1] if c > d[2][0] and c <= d[2][1] ] + [d[2][1]+1,]
        zsplits = [d[3][0],] + [ c for c in partitions[2] if c > d[3][0] and c <= d[3][1] ] + [d[3][1]+1,]

        #print(f"  {xsplits}")
        #print(f"  {ysplits}")
        #print(f"  {zsplits}")

        for xi in range(0,len(xsplits)-1):
            for yi in range(0,len(ysplits)-1):
                for zi in range(0,len(zsplits)-1):
                    cb = ( (xsplits[xi],xsplits[xi+1]), (ysplits[yi],ysplits[yi+1]), (zsplits[zi],zsplits[zi+1]), )
                    if d[0]:
                        oncuboids.add(cb)
                    else:
                        oncuboids.discard(cb)

    size = 0
    for cb in oncuboids:
        #print(f"on: {cb}")
        size = size + ( cb[0][1]-cb[0][0] ) * ( cb[1][1]-cb[1][0] ) * (cb[2][1]-cb[2][0])
        
    return size

def oncells0(seq):
    onvals = set()
    for d in seq:
        for x in range(d[1][0],d[1][1]+1):
            for y in range(d[2][0],d[2][1]+1):
                for z in range(d[3][0],d[3][1]+1):
                    if d[0]:
                        onvals.add( (x,y,z) )
                    else:
                        onvals.discard( (x,y,z) )

    return len(onvals)
    
if args.p1:
    print("Doing part 1")

    def ignore(cuboid):
        for i in range(1,4):
            for e in range(0,2):
                if cuboid[i][e] < -50 or cuboid[i][e] > 50:
                    return True
        return False


    on = oncells(tuple( d for d in data if not ignore(d) ) )
    print(f"Onvals: {on}")
                        
    
if args.p2:
    print("Doing part 2")

    on = oncells(data)
    print(f"Onvals: {on}")
