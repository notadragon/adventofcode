#!/usr/bin/env python

import re,json

def addResult(acc,r,ignore):
    acc["total"] = acc.get("total",0) + r.get("total",0)
    if not ignore:
        acc["rtotal"] = acc.get("rtotal",0) + r.get("rtotal",0)

def traverse(root,ignore=False):
    out = {}
    show=""

    t = type(root)
    if t == dict:
        for v in root.values():
            if v == "red":
                ignore = True
                break
        
        for key in root:
            addResult(out,traverse(key,ignore),ignore)
            addResult(out,traverse(root[key],ignore),ignore)
    if t == int:
        show=root
        r=int(root)
        out["total"] = out.get("total",0) + r
        if not ignore:
            out["rtotal"] = out.get("rtotal",0) + r
    if t == list:
        for v in root:
            addResult(out,traverse(v,ignore),ignore)
    if t == unicode:
        show=root
            
    #print "T: %s  Ignore:%s %s" % (t,ignore,show,)

    return out

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    numberRE = re.compile("(-?\\d+)")

    count = 0
    total = 0
    for n in numberRE.findall(line):
        count += 1
        total += int(n)

    print "NumberTotal (%i) = %i" % (count,total,)

    objects = json.loads(line)
    
    output = traverse(objects)
    print "Out:%s" % (output,)
