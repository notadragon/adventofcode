#!/usr/bin/env pypy

import argparse, re, json

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    ival = x

numberRe = re.compile("-?[0-9]+")
if args.p1:
    print("Doing part 1")

    total = sum( int(x) for x in numberRe.findall(ival) )
    print("Total: %s" % (total,))

def total(jobj):
    if isinstance(jobj,list):
        output = 0
        for c in jobj:
            output += total(c)
        return output
    elif isinstance(jobj,dict):
        if "red" in jobj.values():
            return 0
        else:
            output = 0
            for v in jobj.values():
                output += total(v)
            return output
    elif isinstance(jobj,int):
        return jobj
    else:
        return 0
                
    
if args.p2:
    print("Doing part 2")

    parsed_json = json.loads(ival)

    #print("Parsed: %s" % (parsed_json,))
    print("Total:%s" % (total(parsed_json),))

