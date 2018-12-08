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

#print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile(".*")
values = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    values = [ int(s) for s in x.split(" ") ]

#print("Values (%s):%s" % (len(values),values,))

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def __repr__(self):
        return "Children:%s metadata:%s" % (self.children,self.metadata,)

    def summeta(self):
        return sum( c.summeta() for c in self.children) + sum(self.metadata)

    def value(self):
        if self.children:
            output = 0
            for m in self.metadata:
                if m >= 1 and m <= len(self.children):
                    output += self.children[m-1].value()
            return output
        else:
            return sum(self.metadata)
    
def getNode(vals,i):
    numchildren = vals[i]
    nummetadata = vals[i+1]

    i += 2
    output = Node()
    
    for q in range(0,numchildren):
        child,n = getNode(vals,i)
        i = n
        output.children.append(child)
    for q in range(0,nummetadata):
        output.metadata.append(vals[i])
        i += 1
    return (output,i)
                               
root,l = getNode(values,0)
#print("Consumed:%s/%s" % (l,len(values),))
#print("Root: %s" % (root,))

if args.p1:
    print("Doing part 1")

    print("Sum Meadata: %s" % (root.summeta(),))
    
if args.p2:
    print("Doing part 2")

    print("Value: %s" % (root.value(),))
