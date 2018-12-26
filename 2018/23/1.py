#!/usr/bin/env pypy

import argparse, re, itertools, collections, heapq

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

lineRe = re.compile("pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=(-?[0-9]+)")

stars = []
origin = (0,0,0)

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    stars.append( (int(m.group(4)),int(m.group(1)),int(m.group(2)), int(m.group(3)), ) )

stars.sort()

def mdistance(l1,l2):
    return abs(l1[0] - l2[0]) + abs(l1[1] - l2[1]) + abs(l1[2] - l2[2])

def sdistance(s1,s2):
    return abs(s1[1] - s2[1]) + abs(s1[2] - s2[2]) + abs(s1[3] - s2[3])

#for star in stars:
#    print("Star: %s" % (star,))

    
if args.p1:
    print("Doing part 1")
    strongest = stars[-1]
    reachable = sum([ 1 for s in stars if sdistance(s,strongest) <= strongest[0] ])

    print("Strongest: %s" % (strongest,))
    print("Reachable: %s" % (reachable,))

def inrange(loc):

    return sum([ 1 for s in stars if mdistance(loc,s[1:]) <= s[0] ])

def numpart(total,size):
    if size == 1:
        yield (total,)
    else:
        for i in range(0,total+1):
            for rest in numpart(total-i,size-1):
                yield (i,) + rest

def border(star):
    for d1,d2,d3 in numpart(star[0],3):
        yield ( star[0] - d1, star[1] - d2, star[2] - d3, )
        yield ( star[0] - d1, star[1] - d2, star[2] + d3, )
        yield ( star[0] - d1, star[1] + d2, star[2] - d3, )
        yield ( star[0] - d1, star[1] + d2, star[2] + d3, )
        yield ( star[0] + d1, star[1] - d2, star[2] - d3, )
        yield ( star[0] + d1, star[1] - d2, star[2] + d3, )
        yield ( star[0] + d1, star[1] + d2, star[2] - d3, )
        yield ( star[0] + d1, star[1] + d2, star[2] + d3, )
        
if False:
    print("Doing part 2")

    most = None
    best = None

    dstars = []
    for n,star in enumerate(stars):
        #print("Star[%d]: %s" % (n,star,))

        r = star[0]
        starbest = None
        for loc in [
                ( star[1] - r, star[2], star[3], ),
                ( star[1] + r, star[2], star[3], ),
                ( star[1], star[2] + r, star[3], ),
                ( star[1], star[2] - r, star[3], ),
                ( star[1], star[2], star[3] + r, ),
                ( star[1], star[2], star[3] - r, ),
        ]:
            numstars = inrange(loc)
            md = mdistance( origin, loc )
            if not starbest or numstars > starbest[1] or md < starbest[0]:
                starbest = (md,numstars,)
                
            if not most or numstars > most:
                most = numstars
                best = set()
                best = loc
                print("Best: %s, %s distance: %s" % (best,most,mdistance( origin, best),))
            elif numstars == most:
                if mdistance( origin, loc) < mdistance( origin, best):
                    best = loc
                    #print("Best: %s, %s" % (best,most,))


        dstars.append( (starbest,n,star,) )
                    
    print("Corner Sweep Done")

    dstars.sort()
    for d,n,star in dstars:
        # walk the border of the star's range
        print("Star[%d]: %s" % (n,star,))
        for loc in border(star):
            numstars = inrange(loc)
            if not most or numstars > most:
                most = numstars
                best = set()
                best = loc
                print("Best: %s, %s distance: %s" % (best,most,mdistance( origin, best),))
            elif numstars == most:
                if mdistance( origin, loc) < mdistance( origin, best):
                    best = loc
                    #print("Best: %s, %s" % (best,most,))

    print("Best: %s, %s distance: %s" % (best,most,mdistance( origin, best),))

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a,b)

def genregions(dfunc):
    regionborders = []

    for n,star in enumerate(stars):
        m = dfunc(star)
        regionborders.append( (m - star[0], 1, n, ) )
        regionborders.append( (m + star[0] + 1, -1, n, ) )

    regionborders.sort()

    regions = []
    numstars = 0
    for b1,b2 in pairwise(regionborders):
        numstars += b1[1]
        if b2[0] > b1[0]:
            regions.append( ( b1[0], b2[0], numstars ) )

    return regions

if False:
    print("Doing part 2")

    mregions = genregions( lambda x : mdistance( origin, s[1:]) )

    maxr = None
    for m in mregions:
        if not maxr or m[2] > maxr[2]:
            maxr = m

    print("Max Region:%s" % (maxr,))

def inbox(m, size, loc):
    return m[0] >= loc[0] and m[1] >= loc[1] and m[2] >= loc[2] and m[0] < loc[0] + size and m[1] < loc[1] + size and m[2] < loc[2] + size

def buildcorners( size, loc):
    yield (loc[0], loc[1], loc[2],)
    yield (loc[0], loc[1] + size-1, loc[2],)
    yield (loc[0], loc[1], loc[2] + size-1,)
    yield (loc[0], loc[1] + size-1, loc[2] + size-1,)
    yield (loc[0] + size-1, loc[1], loc[2],)
    yield (loc[0] + size-1, loc[1] + size-1, loc[2],)
    yield (loc[0] + size-1, loc[1], loc[2] + size-1,)
    yield (loc[0] + size-1, loc[1] + size-1, loc[2] + size-1,)

def starpoints( star ):
    r = star[0]
    yield ( star[1] - r, star[2], star[3] )
    yield ( star[1] + r, star[2], star[3] )
    yield ( star[1], star[2] - r, star[3] )
    yield ( star[1], star[2] + r, star[3] )
    yield ( star[1], star[2], star[3] - r )
    yield ( star[1], star[2], star[3] + r )

def rangedist(x,low,hi):
    if x < low:
        return low-x
    elif x > hi:
        return x-hi
    else:
        return 0
    
    
def buildregion( size, loc):
    # return (numstars, distance from origin, size, loc, )

    rloc = (loc[0]+size-1,loc[1]+size-1,loc[2]+size-1,)
    
    numstars = 0
    for s in stars:
        sdist = sum([ rangedist( s[i+1], loc[i], rloc[i]) for i in range(0,len(loc)) ])
        if sdist <= s[0]:
            numstars += 1

    if inbox( origin, size, loc):
        d = 0
    else:
        d = min( [ mdistance(origin,d) for d in buildcorners(size,loc) ] )
            
    return ( -numstars, d, size, loc, )

if args.p2:
    print("Doing part 2")

    minx = min( [s[1] - s[0] for s in stars] )
    maxx = max( [s[1] + s[0] for s in stars] )
    miny = min( [s[2] - s[0] for s in stars] )
    maxy = max( [s[2] + s[0] for s in stars] )
    minz = min( [s[3] - s[0] for s in stars] )
    maxz = max( [s[3] + s[0] for s in stars] )

    box = ( (minx,miny,minz), (maxx, maxy, maxz) )
    print("Bounds: %s" % (box,))

    regionsize = 1 << max(abs(minx),abs(miny),abs(minz),abs(maxx),abs(maxy),abs(maxz)).bit_length() + 1
    regions = [ buildregion( regionsize * 2, (-regionsize, -regionsize, -regionsize) ) ]

    print("Starting Regions; %s" % (regions,))

    while True:
        region = heapq.heappop(regions)
        print("Checking Region: %s/%s" % (region,len(regions),))

        if region[2] == 1:
            print("Final Region: %s" % (region,))
            break

        loc = region[3]
        size = region[2]
        newsize = size / 2

        for l in [ (loc[0],         loc[1],         loc[2],),
                   (loc[0],         loc[1]+newsize, loc[2],),
                   (loc[0],         loc[1],         loc[2]+newsize,),
                   (loc[0],         loc[1]+newsize, loc[2]+newsize,),
                   (loc[0]+newsize, loc[1],         loc[2],),
                   (loc[0]+newsize, loc[1]+newsize, loc[2],),
                   (loc[0]+newsize, loc[1],         loc[2]+newsize,),
                   (loc[0]+newsize, loc[1]+newsize, loc[2]+newsize,), ]:
            r = buildregion(newsize, l)
            if r and r[0] != 0:
                heapq.heappush(regions, buildregion( newsize,l) )
