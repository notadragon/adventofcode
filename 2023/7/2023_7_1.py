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

lineRe = re.compile("^([AKQJT2-9]+) ([0-9]+)$")

data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (m.group(1), int(m.group(2)), ))


def makestrengths():
    output = {}
    cards = "23456789TJQKA"
    for i in range(0,len(cards)):
        output[cards[i]] = i+2
    return output
        
strengths = makestrengths()
   
def cardval(c):
    return strengths[c]

def handtype(hand):
    cards = {}
    for c in hand:
        cards[c] = cards.get(c,0) + 1

    if len(cards) == 1:
        return (6,"five")
    elif len(cards) == 2:
        m = max(v for v in cards.values())
        if m == 4:
            return (5,"four")
        else:
            return (4,"house")
    elif len(cards) == 3:
        m = max(v for v in cards.values())
        if m == 3:
            return (3,"three")
        else:
            return (2,"twopair")
    elif len(cards) == 4:
        return (1,"pair")
    else:
        return (0,"high")

    
if args.p1:
    print("Doing part 1")

    handdata = []
    
    for hand, bid in data:

        t = handtype(hand)
        handvals = tuple( cardval(c) for c in hand) 

        handdata.append( ( t, handvals, hand, bid,) )

    handdata.sort()

    winnings = 0
    for n in range(0,len(handdata)):
        hd = handdata[n]
        rank = n + 1
        hand = hd[2]
        bid = hd[3]
        winnings = winnings + rank*bid
    print(f"Total Winnigs: {winnings}")
    
def makestrengths2():
    output = {}
    cards = "23456789TJQKA"
    for i in range(0,len(cards)):
        output[cards[i]] = i+2
    output["J"] = 0
    return output
        
strengths2 = makestrengths2()
   
def cardval2(c):
    return strengths2[c]

def handtype2(hand):
    cards = {}
    for c in hand:
        cards[c] = cards.get(c,0) + 1

    if "J" in cards:
        jokers = cards["J"]
        del cards["J"]
    else:
        jokers = 0

    if jokers == 5:
        return (6,"five")
    
    m = max(v for v in cards.values())

    if m + jokers == 5:
        return (6,"five")
    if m + jokers == 4:
        return (5,"four")
    if len(cards) == 2:
        return (4,"house")
    if m + jokers == 3:
        return (3,"three")
    if jokers == 0:
        if len(cards) == 3:
            return (2,"twopair")
        elif len(cards) == 4:
            return (1,"pair")
    else:
        return (1, "pair")    
    return (0,"high")
    
if args.p2:
    print("Doing part 2")

    handdata = []
    
    for hand, bid in data:

        t = handtype2(hand)
        handvals = tuple( cardval2(c) for c in hand) 

        handdata.append( ( t, handvals, hand, bid,) )

    handdata.sort()

    winnings = 0
    for n in range(0,len(handdata)):
        #print(f"{n+1}: {handdata[n]}")
        
        hd = handdata[n]
        rank = n + 1
        hand = hd[2]
        bid = hd[3]
        winnings = winnings + rank*bid
    print(f"Total Winnigs: {winnings}")
