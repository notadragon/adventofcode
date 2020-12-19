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

lineRe = re.compile("^([ab]+$)|(?:(\d+): (.*))")
allrules = {}
messages = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        messages.append(x)
    else:
        ruleid = int(m.group(2))
        ruleval = []
        for rs in m.group(3).split("|"):
            rs = rs.strip()
            rulepart = []
            if rs[0] == "\"" and rs[2] == "\"":
                rulepart = rs[1]
            else:
                for r in rs.split(" "):
                    r = r.strip()
                    rulepart.append(int(r))
            ruleval.append(rulepart)
        allrules[ruleid] = ruleval

for r,rv in allrules.items():
    #print("Rule: %s:%s" % (r,rv))
    pass

def strmatchlen(message,rule):
    if len(message) < len(rule):
        return 0
    for i in range(0,len(rule)):
        r = rule[i]
        if r != "." and message[i] != r:
            return 0
    return len(rule)

def matchLen(rules,cache,rid,rule,message):
    if (message,rid) in cache:
        return cache[ (message,rid,) ]
    
    output = []
    for rpart in rule:
        if type(rpart) is str:
            mlen = strmatchlen(message,rpart)
            #print("%s %s: %s" % (message,rpart,mlen,))
            if mlen:
                output.append(mlen)
        else:
            poses = [0]
            #print("message: %s RPART: %s" % (message, rpart,))
            for prid in rpart:
                #print("  Poses: %s" % (poses,))
                newposes = []
                if type(prid) is str:
                    for p in poses:
                        rest = message[p:]
                        mlen = strmatchlen(rest,prid)
                        if mlen:
                            newposes.append(p + mlen)
                elif prid not in rules:
                    pass
                else:
                    rpartrule = rules[prid]
                    #print("  RPARTRULE: %s" % (rpartrule,))
                    for p in poses:
                        if p >= len(message):
                            continue
                        rest = message[p:]
                        ls = matchLen(rules,cache,prid,rpartrule,rest)
                        #print("  ls: %s" % (ls,))
                        for l in ls:
                            newposes.append(p + l)
                poses = newposes
            output.extend(poses)

    #print("Message: %s  Rule: %s:%s, matchlens: %s %s" % (message, rid, rule, output, "!" if len(message) in output else ""))
    cache[ (message,rid) ] = output 
    return output

def optimizeRules(rules):
    prev = rules
    output = {}

    changed = True
    while changed:
        changed = False
        literals = {}
        for rid,rule in prev.items():
            if len(rule) == 1 and type(rule[0]) is str:
                literals[rid] = rule[0]

        #print("Literals: %s" % (literals,))

        for rid,rule in prev.items():
            newrule = []
            for rpart in rule:
                if type(rpart) is str:
                    newrule.append(rpart)
                else:
                    newpart = []
                    for prid in rpart:
                        if prid in literals:
                            prid = literals[prid]
                            changed = True
                        if type(prid) is str and newpart and type(newpart[-1]) is str:
                            newpart[-1] = newpart[-1] + prid
                        else:
                            newpart.append(prid)

                    if len(newpart) == 1 and type(newpart[0]) is str:
                        newrule.append(newpart[0])
                    else:
                        newrule.append(newpart)
            if len(newrule) == 2 and newrule[0] == "a" and newrule[1] == "b":
                newrule = ["."]
                            
            output[rid] = newrule
        prev = output
                    
    return output
    
def rulesMatch(rules,cache,message):
    for rid,rule in rules.items():
        ls = matchLen(rules,cache,rid,rule,message)
        if not ls:
            continue
        if len(message) in ls:
            return True
    return False

def rulesMatch2(rules,cache,message):
    rid = 0
    rule = rules[0]
    ls = matchLen(rules,cache,rid,rule,message)
    if len(message) in ls:
            return True
    return False

if args.p1:
    print("Doing part 1")

    rules = allrules.copy()
    #print("Rules: %s" % (rules,))
    rules = optimizeRules(rules)
    #print("Optimized Rules: %s" % (rules,))


    matched = 0
    cache = {}
    for message in messages:
        v = rulesMatch2(rules,cache,message)
        #print("m: %s v: %s" % (message,v,))
        if v:
            matched += 1
    print("Matched: %s" % (matched,))
    
if args.p2:
    print("Doing part 2")

    newrules = allrules.copy()
    newrules[ 8 ] = [ [42], [42, 8] ]
    newrules[ 11 ] = [ [42, 31], [ 42, 11, 31] ]

    #print("Rules: %s" % (newrules,))
    #newrules = optimizeRules(newrules)
    #print("Optimized Rules: %s" % (newrules,))

    matched = 0
    cache = {}
    for message in messages:
        v = rulesMatch2(newrules,cache,message)
        #print("m: %s v: %s" % (message,v,))
        if v:
            matched += 1
    print("Matched: %s" % (matched,))
