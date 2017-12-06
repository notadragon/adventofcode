#!/usr/bin/env python

import re, itertools

lineRe = re.compile("(\d+)")

nums = []

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue

    nums.append(int(line))


print "Nums: %s" % (nums,)


def findsubsets(nums,total):
    for i in range(0,len(nums)):
        size = nums[i]
        if size < total:
            for rest in findsubsets(nums[i+1:],total-size):
                yield (size,) + rest
        elif size == total:
            yield (size,)

mintotal = 0
total = 0
minnum = None
for subset in findsubsets(nums,150):
    num = len(subset)

    if not minnum or num < minnum:
        minnum = num
        mintotal = 1
    elif num == minnum:
        mintotal = mintotal + 1
        
    #print "Subset: %s Size: %s" % (subset,sum(subset),)
    total = total+1

print "Total subsets: %s" % (total,)
print "Smallest (%s) subsets: %s" % (minnum,mintotal,)
