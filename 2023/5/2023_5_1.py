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

seeds = []
types = set()
maps = {}

seedsRe = re.compile("seeds: ([0-9 ]*)")
mapRe = re.compile("(.*)-to-(.*) map:")
mapdataRe = re.compile("[0-9 ]*")

mapkey = None
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = seedsRe.match(x)
    if m:
        seeds = tuple(( int(i) for i in m.group(1).split(" ") ))
        continue

    m = mapRe.match(x)
    if m:
        mapkey = ( m.group(1), m.group(2) )
        types.add(m.group(1))
        types.add(m.group(2))
        maps[mapkey] = []
        maps[ (mapkey[1], mapkey[0]) ] = []
        continue

    m = mapdataRe.match(x)
    if m:
        md = tuple(( int(i) for i in x.split(" ") ))
        maps[mapkey].append(md)

        maps[ (mapkey[1], mapkey[0]) ].append( ( md[1], md[0], md[2],) )
        continue
        
        
    print("Invalid line: %s" % (x,))
    
#print(f"Seeds: {seeds}")
#for mk,data in maps.items():
#    print(f"Map Key: {mk}")
#    for d in data:
#        print(f"  {d}")

def genpath():
    found = set()
    found.add("seed")

    while len(found) < len(types):
        for fromtype,totype in maps.keys():
            if fromtype in found and not totype in found:
                yield (fromtype,totype)
                found.add(totype)

            if totype in found and not fromtype in found:
                yield (totype,fromtype)
                found.add(fromtype)

        
mappath = list( genpath() )
print(f"Path: {mappath}")

if args.p1:
    print("Doing part 1")

    def mapval( fromtype, totype, fromid):
        if (fromtype,totype) in maps:
            mappings = maps[ (fromtype,totype) ]
            for md in mappings:
                if fromid >= md[1] and fromid < md[1] + md[2]:
                    return md[0] + (fromid - md[1])
            return fromid
        
        return None


    def genmappings( vals ):

        for pair in mappath:
            val = vals[pair[0]]
            vals[pair[1]] = mapval( pair[0], pair[1], val)
        
        return vals

    minlocation = None
    for s in seeds:
        #toid = mapval( "seed", "soil", s)
        #print(f"Seed number {s} corresponds to soil number {toid}")

        ms = genmappings( { "seed" : s } )

        #print(f"{s}: -> {ms}")

        if minlocation == None or ms["location"] < minlocation:
            minlocation = ms["location"]

    print(f"Min Location: {minlocation}")
        
if args.p2:
    print("Doing part 2")

    def sortranges(rs):
        rs = list(rs)
        rs.sort()

        def gen():
            prev = None

            for r in rs:
                if prev and prev[0] + prev[1] >= r[0]:
                    prev = (prev[0], max(prev[0] + prev[1], r[0] + r[1]) - prev[0])
                else:
                    if prev:
                        yield prev
                    prev = r
            if prev:
                yield prev

        return tuple(gen())
        

    ranges = {}
    ranges["seed"] = sortranges( ( (seeds[n], seeds[n+1]) for n in range(0,len(seeds),2)) )


    def maprange(fromtype, totype, rs):
        if (fromtype,totype) in maps:
            
            mappings = maps[ (fromtype, totype) ]

            tomap = rs
            for md in mappings:
                rem = []

                mbegin = md[1]
                mend = md[1] + md[2]

                for r in tomap:
                    splitup = []
                    
                    begin = r[0]
                    end = r[0] + r[1]

                    if begin < mbegin:
                        b = begin
                        e = min(end, mbegin)
                        splitup.append( (b,e-b) )
                        rem.append( (b,e-b) )
                        begin = mbegin

                    if end > mend:
                        b = max(mend, begin)
                        e = end
                        splitup.append( (b,e-b) )
                        rem.append( (b,e-b) )
                        end = mend

                    if end > begin:
                        splitup.append( (begin, end-begin) )
                        
                        yield ( md[0] + (begin-mbegin), end-begin )

                    #print(f"MD: {md}  r: {r} -> {splitup}")

                tomap = rem
                if not tomap:
                    break
                    
            for r in tomap:
                yield r
                

    for pair in mappath:
        fromrs = ranges[pair[0]]

        #print(f"{pair[0]} -> {fromrs}")

        tors = sortranges(maprange( pair[0], pair[1], fromrs ))

        ranges[pair[1]] = tors

        #print(f"{pair[1]} -> {tors}")
        

    locations = ranges["location"]
    #print(f"Locations: {locations}")

    print(f"MinLocation: {locations[0][0]}")
