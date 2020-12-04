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

lineRe = re.compile("(([a-z]+):([a-z0-9]+) *)*")
data = []

for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    xl = []
    for p in x.split(" "):
        if p:
            k,v = p.split(":")
            xl.append( (k,v) )
    data.append(xl)


    
#for d in data:
#    print("%s" % (d,))

expectedfields = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid", ]


def getpassports(data):
    pp = []
    for d in data:
        if not d:
            if pp:
                yield pp
            pp = []
        else:
            pp.extend(d)
    if pp:
        yield pp

def getpassportsd(data):
    for pp in getpassports(data):
        yield { k:v for k,v in pp }
        
if args.p1:
    print("Doing part 1")


    def isvalid(ppd):
        for f in expectedfields:
            if f != "cid" and not f in ppd:
                return False
        return True

    valid = 0
    for ppd in getpassportsd(data):
        if isvalid(ppd):
            valid = valid + 1
            #print("Valid: %s" % (ppd,))
    print("Total Valid: %s" % (valid,))

if args.p2:
    print("Doing part 2")

    def isvalid(ppd):
        v = True
        for f in expectedfields:
            if f != "cid" and not f in ppd:
                return False

        numRe = re.compile("[0-9]+")
        byr = ppd["byr"]
        if len(byr) != 4 or not numRe.match(byr):
            if v: print("Bad BYR: %s" % (byr,))
            return False
        byr = int(byr)
        if byr < 1920 or byr > 2002:
            if v: print("Bad BYR Range: %s" % (byr,))
            return False

        iyr = ppd["iyr"]
        if len(iyr) != 4 or not numRe.match(iyr):
            if v: print("Bad IYR: %s" % (iyr,))
            return False
        iyr = int(iyr)
        if iyr < 2010 or iyr > 2020:
            if v: print("Bad IYR Range: %s" % (iyr,))
            return False

        eyr = ppd["eyr"]
        if len(eyr) != 4 or not numRe.match(eyr):
            return False
        eyr = int(eyr)
        if eyr < 2020 or eyr > 2030:
            return False

        hgt = ppd["hgt"]
        hgtRe = re.compile("([0-9]+)cm|([0-9]+)in")
        m = hgtRe.match(hgt)
        if not m:
            if v: print("Bad hgt: %s" % (hgt,))
            return False
        if m.group(1):
            cmhgt = int(m.group(1))
            if cmhgt < 150 or cmhgt > 193:
                if v: print("Bad hgtcm: %s" % (hgt,))
                return False
        else:
            inhgt = int(m.group(2))
            if inhgt < 59 or inhgt > 76:
                if v: print("Bad hgtin: %s" % (hgt,))
                return False

        hcl = ppd["hcl"]
        hclRe = re.compile("#[0-9a-f]{6}")
        m = hclRe.match(hcl)
        if not m:
            if v: print("Bad hcl: %s" % (hcl,))
            return False

        ecl = ppd["ecl"]
        if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            if v: print("Bad ecl: %s" % (ecl,))
            return False
        
        pid = ppd["pid"]
        if len(pid) != 9 or not numRe.match(pid):
            if v: print("Bad pid: %s" % (pid,))
            return False
        
        return True

    valid = 0
    for ppd in getpassportsd(data):
        if isvalid(ppd):
            valid = valid + 1
        print("InValid: %s" % (ppd,))
    print("Total Valid: %s" % (valid,))
