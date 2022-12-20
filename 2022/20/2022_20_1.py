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

lineRe = re.compile("^-?[0-9]+$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(int(x))

#print(f"{data}")

class Link:
    def __init__(self, val):
        self.left = self
        self.right = self
        self.val = val

    def addright(self, r):
        r.right = self.right
        r.right.left = r
        
        r.left = self
        self.right = r
        return r

    def addleft(self, l):
        l.left = self.left
        l.left.right = l

        l.right = self
        self.left = l
        return l

    def remright(self):
        output = self.right
        if output == self:
            raise Exception("OOPS")
        self.right = output.right
        self.right.left = self
        output.right = output
        output.left = output
        return output

    def remleft(self):
        output = self.left
        if output == self:
            raise Exception("OOPS")
        self.left = output.left
        self.left.right = self
        output.right = output
        output.left = output
        return output

    def mix(self,val):
        target = self.left
        self.left.remright()
        
        while val > 0:
            target = target.right
            val = val - 1
        while val < 0:
            target = target.left
            val = val + 1
        target.addright(self)

    def advance(self,d):
        output = self
        while d > 0:
            output = output.right;
            d = d - 1
        while d < 0:
            output = output.left
            d = d + 1
        return output

def iterlist(l):
    cursor = l
    yield cursor
    while cursor.right != l:
        cursor = cursor.right
        yield cursor
    
def printlist(l):
    output = [f"{l.val}"]
    i = l
    while i.right != l:
        i = i.right
        output.append(f"{i.val}")
    print(",".join(output))

if args.p1:
    print("Doing part 1")

    numlinks = len(data)
    alllinks = []
    zeroval = None
    for v in data:
        l = Link(v)
        if v == 0:
            zeroval = l
        if alllinks:
            alllinks[-1].addright(l)
        alllinks.append(l)
        
    for l in alllinks:
        l.mix(l.val)

        #printlist(zeroval)

    total = 0
    for i in (1000,2000,3000):
        ival = zeroval.advance(i)
        total = total + ival.val
        print(f"z[{i}] = {ival.val}")

    print(f"Total: {total}")
        
    
if args.p2:
    print("Doing part 2")

    decryptionkey = 811589153

    numlinks = len(data)
    alllinks = []
    zeroval = None
    for v in data:
        v = v * decryptionkey
        l = Link(v)
        if v == 0:
            zeroval = l
        if alllinks:
            alllinks[-1].addright(l)
        alllinks.append(l)

    for i in range(0,10):
        for l in alllinks:
            tomix = l.val % (len(data)-1)
            l.mix(tomix)

        #printlist(zeroval)

    total = 0
    for i in (1000,2000,3000):
        ival = zeroval.advance(i)
        total = total + ival.val
        print(f"z[{i}] = {ival.val}")

    print(f"Total: {total}")
