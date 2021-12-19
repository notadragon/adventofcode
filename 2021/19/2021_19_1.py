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

lineRe = re.compile("(?:--- scanner (\d+) ---)|(?:(-?\d+),(-?\d+),(-?\d+))")

scanners = {}

scanner = None
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        scanner = int(m.group(1))
        scanners[scanner] = []
    else:
        scanners[scanner].append( ( int(m.group(2)), int(m.group(3)), int(m.group(4)), ) )

rotations = {
    "id"  : ( (  1,  0,  0),
              (  0,  1,  0),
              (  0,  0,  1), ),
    "z90" : ( (  0, -1,  0),
              (  1,  0,  0),
              (  0,  0,  1), ),
    "y90" : ( (  0,  0, -1),
              (  0,  1,  0),
              (  1,  0,  0), ),
    "x90" : ( (  1,  0,  0),
              (  0,  0, -1),
              (  0,  1,  0), ),
    }

def mmult1(m, r):
    output  = []
    for row in range(0, len(m)):
        rd = []
        for col in range(0, len(r[0])):
            rd.append( sum(( m[row][i] * r[i][col] for i in range(0,len(m[row])))) )
        output.append(tuple(rd))
    return tuple(output)

def mmult(m, r):
    return tuple((tuple(( sum(( m[row][i] * r[i][col] for i in range(0,len(m[row])))) for col in range(0, len(r[0])) )) for row in range(0, len(m))))

def madd(m, r):
    return tuple((tuple(( m[row][col] + r[row][col] for col in range(0,len(m[row])))) for row in range(0,len(m))))

def msub(m, r):
    return tuple((tuple(( m[row][col] - r[row][col] for col in range(0,len(m[row])))) for row in range(0,len(m))))

def mdistance(p1, p2):
    return sum(abs( p2[0][i] - p1[0][i] ) for i in range(0,len(p1[0])))

def makeRotations():
    output = set()

    toadd = [ rotations["id"] ]

    while toadd:
        m = toadd.pop()
        if m in output:
            continue

        output.add(m)

        for r in rotations.values():
            toadd.append(mmult(m,r))

    return list(output)

allrotations = makeRotations()

#for r in allrotations:
#    print(f"Rotations: {r}")
#print(f"Num Rotations: {len(allrotations)}")

def matches(points1, points2, rot, delta):
    overlaps = 0
    for p2 in points2:
        p2a = mmult( (p2,), rot)
        p2a = madd(p2a, delta)
        if p2a[0] in points1:
            overlaps = overlaps + 1
            continue
        #if (p2a[0][0] >= -1000 and p2a[0][0] <= 1000) or (p2a[0][1] >= -1000 and p2a[0][1] <= 1000) or (p2a[0][2] >= -1000 and p2a[0][2] <= 1000):
        #   print(f"In range but not overlapping: {p2a}")
        #   overlaps = 0
        #   break

    #print(f"{rot} + {delta} -> {overlaps}")
        
    return overlaps

def matchups(points1, points2):
    points1 = set(points1)
    points2 = set(points2)

    checked = set()
    
    for rot in allrotations:
        points2r = { mmult( (p2,), rot ) for p2 in points2 }
        
        for p2a in points2r:
            # starting point is p2
            for p1 in points1:
                delta = msub( (p1,), p2a )
                #print(f"{delta}")

                if (rot,delta) in checked:
                    continue
                checked.add( (rot,delta) )

                overlaps = matches(points1, points2, rot, delta)
                if overlaps >= 12:
                    yield (rot,delta,overlaps)
                    return

#for scanner,points in scanners.items():
#    print(f"{scanner} -> {points}")

if args.p1 or args.p2:
    print("Doing part 1")

    scannerids = list(scanners.keys())
    scannerids.sort()

    allmatchups = {
        scannerids[0] : ( None, rotations["id"], ( (0,0,0), ), rotations["id"], ( (0,0,0), ), )
    }
    tosearch = [ scannerids[0] ]
    unfound = set( scannerids[1:] )

    print(f"{scannerids[0]} -> {allmatchups[scannerids[0]]}")


    if args.input == "input":
        cheats = {
            0 : (27,),
            27 : (28,),
            28 : (30,),
            30 : (18,),
            18 : (17,20,26,),
            26 : (8,9,12,),
            12 : (35,),
            35 : (),
            9 : (23, 25, ),
            25 : (3, 10, 15, ),
            15 : (11,),
            11 : (),
            10 : (4,19,),
            19 : (),
            4 : (),
            3 : (),
            23 : (7,),
            7 : (13,),
            13 : (22,),
            22 : (32,),
            32 : (5,33,),
            33 : (2,14,),
            14 : (16,),
            16 : (),
            2 : (),
            5 : (),
            8 : (24,),
            24 : (),
            20 : (),
            17 : (31,),
            31 : (1,37,),
            37 : (6,),
            6 : (34,),
            34 : (36,),
            36 : (29,),
            29 : (),
            1 : (21,),
            21 : (),        
        }
    else:
        cheats = {}
        
        
    while tosearch and unfound:
        scannerid1 = tosearch.pop()

        scannerid1m = allmatchups[scannerid1]

        print(f"Searching: {scannerid1} Remaining: {len(unfound)}")
        
        if scannerid1 in cheats:
            tocheck = cheats[scannerid1]
        else:
            tocheck = list(unfound)
        for scannerid2 in tocheck:
            smatchups = list( matchups(scanners[scannerid1],scanners[scannerid2]) )
            if smatchups:
                smatchup = smatchups[0]

                # p1 = p2 * r2 + d2
                # p2 = p3 * r3 + d3
                # p1 = (p3 * r3 + d3) * r2 + d2 = p3 * r3 * r2 + d3 * r2 + d2

                # r2 = scannerid1m[3]
                # d2 = scannerid1m[4]
                # r3 = smatchup[0]
                # d3 = smatchup[1]
                # r13 = r3 * r2 = smatchup[0] * scannerid1m[3]
                # d13 = d3 * r2 + d2 =  smatchup[1] * scannerid1m[3] + scannerid1m[4]
                
                sm = mmult( smatchup[0] , scannerid1m[3] )
                sd = madd( mmult( smatchup[1], scannerid1m[3] ), scannerid1m[4] )

                allmatchups[ scannerid2 ] = ( scannerid1, smatchup[0], smatchup[1], sm, sd, )
                
                print(f"{scannerid1} x {scannerid2} -> {allmatchups[scannerid2]}")
                
                tosearch.append(scannerid2)
                unfound.remove(scannerid2)

    allpoints = set()
    for scannerid,points in scanners.items():
        matchup = allmatchups[scannerid]

        for p in points:
            adj = madd( mmult((p,), matchup[3]), matchup[4] )
            allpoints.add(adj)

    print(f"All points: {len(allpoints)}")

    maxd = None
    for scannerid1 in scanners.keys():
        scannerid1m = allmatchups[scannerid1]
        for scannerid2 in scanners.keys():
            scannerid2m = allmatchups[scannerid2]

            d = mdistance(scannerid1m[4], scannerid2m[4])
            if maxd == None or d > maxd:
                print(f"Largest: {scannerid1} x {scannerid2} = {d}")
                maxd = d 
        
                

