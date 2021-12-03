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

lineRe = re.compile("\d+")
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

#for x in data:
#    print(x)

if args.p1:
    print("Doing part 1")

    counts = [0] * len(data[0])
    for x in data:
        for i in range(0,len(x)):
            if x[i] == "1":
                counts[i] = counts[i] + 1

    gbits = []
    ebits = []
    for i in range(0,len(counts)):
        ones = counts[i]
        zeroes = len(data) - ones
        if ones > zeroes:
            gbits.append( "1" )
            ebits.append( "0" )
        else:
            gbits.append( "0" )
            ebits.append( "1" )

    gamma = "".join(gbits)
    epsilon = "".join(ebits)
    print("Gamma: %s = %s" % (gamma,int(gamma,2)))
    print("Epsilon: %s = %s" % (epsilon,int(epsilon,2)))

    power = int(gamma, 2) * int(epsilon, 2)
    print("Power: %s" % (power,))
    
if args.p2:
    print("Doing part 2")

    def oxygenRating(numbers, ndx):
        ones = len([x[ndx] for x in numbers if x[ndx] == "1"])
        zeroes = len(numbers) - ones
        if ones >= zeroes: return "1"
        return "0"

    def co2scrubberRating(numbers, ndx):
        ones = len([x[ndx] for x in numbers if x[ndx] == "1"])
        zeroes = len(numbers) - ones
        if ones < zeroes: return "1"
        return "0"

    def consider(numbers, fun):
        ndx = 0
        while len(numbers) > 1:
            newnumbers = []

            criteria = fun(numbers,ndx)

            numbers = [ x for x in numbers if x[ndx] == criteria ]

            ndx = ndx + 1

        return numbers[0]


    orating = consider(data, oxygenRating)
    crating = consider(data, co2scrubberRating)

    print(f"Orating: {orating} = {int(orating,2)}")
    print(f"Crating: {crating} = {int(crating,2)}")
    print(f"Life support rating: {int(orating,2) * int(crating,2)}")
        
