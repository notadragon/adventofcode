#!/usr/bin/env python

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

streams = []

for x in open(args.input).readlines():
    x = x.strip()

    streams.append(x)

def groupfind(s,ndx,depth):
    while ndx < len(s):
        start = ndx
        if s[ndx] == '<':
            ndx = ndx + 1
            while ndx < len(s) and s[ndx] != '>':
                ndx = ndx + 1
            ndx = ndx + 1
            yield ('<',start,ndx,s[start:ndx])
            if ndx < len(s) and s[ndx] == ',':
                ndx = ndx + 1
                continue
            else:
                return
        elif s[ndx] == '{':
            ndx = ndx + 1
            for d in groupfind(s,ndx,depth+1):
                ndx = d[2]
                yield d
            if s[ndx] == '}':
                ndx = ndx + 1
                yield ('g',start,ndx,s[start:ndx],depth)
            if ndx < len(s) and s[ndx] == ',':
                ndx = ndx + 1
                continue
            else:
                return
        else:
            return
    
if args.p1:
    print "Doing part 1"

    for s in streams:
        print "in:%s" % (s,)

        skipRe = re.compile("\\!.")
        s = skipRe.sub("",s)

        score = 0
        for d in groupfind(s,0,1):
            print "  %s" % (d,)
            if d[0] == 'g':
                score = score + d[4]
        print "Score: %s" % (score,)
    
if args.p2:
    print "Doing part 2"

    for s in streams:
        print "in:%s" % (s,)

        skipRe = re.compile("\\!.")
        s = skipRe.sub("",s)

        score = 0
        for d in groupfind(s,0,1):
            print "  %s" % (d,)
            if d[0] == '<':
                score = score + len(d[3]) - 2
        print "Score: %s" % (score,)
        
