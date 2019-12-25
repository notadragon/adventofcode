#!/usr/bin/env pypy

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

lineRe = re.compile("To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).")

row = None
column = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    row = int(m.group(1))
    column = int(m.group(2))

print("Row: %s  Column: %s" % (row,column,))

def gencode():
    output = 20151125
    while True:
        yield output

        output = (output * 252533) % 33554393

def locations():
    for i in itertools.count(1):
        for x in range(0,i):
            y = i-x-1
            yield (x + 1, y + 1)
        
if args.p1:
    print("Doing part 1")

    for loc,code in itertools.izip(locations(),gencode()):
        if loc[0] == column and loc[1] == row:
            print("loc:%s code:%s" % (loc,code,))
            break
    
if args.p2:
    print("Doing part 2")
