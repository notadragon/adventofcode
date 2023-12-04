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

lineRe = re.compile("^[\.\*#\+\$\-@\&/%0-9=]*$")

grid = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    grid.append(x)

#for g in grid:
#    print(g)

def adjacents(loc):
    for delta in ( (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), ):
        yield (loc[0] + delta[0], loc[1] + delta[1],)

        
gcontents = {}
for y in range(0,len(grid)):
    row = grid[y]
    for x in range(0,len(row)):
        if row[x] != ".":
            gcontents[ (x,y) ] = row[x]

def getcontents(loc):
    return gcontents.get(loc, ".")

        
if args.p1:
    print("Doing part 1")


    total = 0
    for loc,val in gcontents.items():
        if val.isdigit() and not getcontents( (loc[0]-1,loc[1]) ).isdigit():

            num = []
            nloc = loc
            nlocs = set()
            while nloc in gcontents and gcontents[nloc].isdigit():
                nlocs.add(nloc)
                num.append( gcontents[nloc] )
                nloc = ( nloc[0] + 1, nloc[1] )

            num = int( "".join(num) )

            syms = {}
            
            for nloc in nlocs:
               for adj in adjacents(nloc):
                   adjv = getcontents( adj )
                   if adjv != "." and not adjv.isdigit():
                     syms[adj] = adjv
            
            #print(f"NUMBER AT {loc}: {num}  adj: {syms}")
            
            if syms:
                total = total + num

    print(f"Total: {total}")

            
    
    
if args.p2:
    print("Doing part 2")

    nums = {}
    
    for loc,val in gcontents.items():
        if val.isdigit() and not getcontents( (loc[0]-1,loc[1]) ).isdigit():

            num = []
            nloc = loc
            nlocs = set()
            while nloc in gcontents and gcontents[nloc].isdigit():
                nlocs.add(nloc)
                num.append( gcontents[nloc] )
                nloc = ( nloc[0] + 1, nloc[1] )

            num = int( "".join(num) )

            for nloc in nlocs:
                nums[ nloc ] = (loc, num)


    total = 0
    for loc,val in gcontents.items():
        if val == "*":
            adjnums = set()
            for adj in adjacents(loc):
                if adj in nums:
                    adjnum = nums[adj]
                    adjnums.add( nums[adj] )

            if len(adjnums) == 2:
                ratio = 1
                for n in ( an[1] for an in adjnums ):
                    ratio = ratio * n

                total = total + ratio
                print(f"GEAR? {loc} -> {adjnums} ratio: {ratio} ")
                
    print(f"total: {total}")
