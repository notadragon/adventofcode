#!/usr/bin/env python

import re, md5

valueRe = re.compile("value ([0-9]+) goes to bot ([0-9]+)")
giveRe = re.compile("bot ([0-9]+) gives low to (output|bot) ([0-9]+) and high to (output|bot) ([0-9]+)")

bots = {}
rules = {}

for l in open("input").readlines():
    l = l.strip()

    m = valueRe.match(l)
    if m:
        val = int(m.group(1))
        b = int(m.group(2))

        if b in bots:
            bots[b].append(val)
        else:
            bots[b] = [val,]
        continue

    m = giveRe.match(l)
    if m:
        b1 = int(m.group(1))
        lowtype = m.group(2)
        lownum = int(m.group(3))
        hightype = m.group(4)
        highnum = int(m.group(5))

        rules[b1] = (lowtype,lownum,hightype,highnum,)
        continue
    
    print l
    
print bots

outputs = {}

done = False
while not done:
    any = False
    for b,val in bots.items():
        if len(val) == 2:
            any = True
            del bots[b]
            val.sort()
            if val == [17,61]:
                print("Bot comparing 17,16: %s" % (b,))

            br = rules[b]

            lowtype = br[0]
            lownum = br[1]
            hightype = br[2]
            highnum = br[3]

            if lowtype == "output":
                print "Output %s: %s" % (lownum,val[0],)
                outputs[lownum] = val[0]
            else:
                if lownum in bots:
                    bots[lownum].append(val[0])
                else:
                    bots[lownum] = [val[0],]
                    
                
            if hightype == "output":
                print "Output %s: %s" % (highnum,val[1],)
                outputs[highnum] = val[0]
            else:
                if highnum in bots:
                    bots[highnum].append(val[1])
                else:
                    bots[highnum] = [val[1],]
                
            break

    if not any:
        print("Done")
        break


print("outputs 0-2: %s * %s * %s = %s" % (outputs[0],outputs[1],outputs[2],outputs[0] * outputs[1] * outputs[2],))
