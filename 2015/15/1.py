#!/usr/bin/env pypy

import argparse, re

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

lineRe = re.compile("(.*): capacity (-?[0-9]+), durability (-?[0-9]+), flavor (-?[0-9]+), texture (-?[0-9]+), calories (-?[0-9]+)")

ingredients = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    ingredients.append( (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)), ) )

for i in ingredients:
    print("Ingredient:%s" % (i,))

def partitions(i,total):
    if i == 1:
        yield (total,)
    else:
        for x in range(0,total+1):
            for r in partitions(i-1,total-x):
                yield (x,) + r

def score(partition):
    total = [0] * 5
    for i in range(0,len(partition)):
        if partition[i] > 0:
            ing = ingredients[i]
            for c in range(0,5):
                total[c] += partition[i] * ing[c+1]
    output = 1
    for n in range(0,4):
        c = total[n]
        if c <= 0:
            output = 0
            break
        else:
            output *= c

    #print("%s -> %s = %s" % (partition,total, output,))
    return (output,total[-1],)

if args.p1:
    print("Doing part 1")

    highest = max( [ score(p)[0] for p in partitions(len(ingredients),100) ] )
    print("Highest: %s" % (highest,))
    
if args.p2:
    print("Doing part 2")

    def filter(s):
        if s[1] == 500:
            return s[0]
        else:
            return 0

    best = max( [ filter(score(p)) for p in partitions(len(ingredients),100) ] )
    print("Best: %s" % (best,))
