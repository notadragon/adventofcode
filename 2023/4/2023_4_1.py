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

lineRe = re.compile("^Card +([0-9]+): (.*)\\|(.*)$")

cards = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))


    # Process input line
    cardid = int(m.group(1))

    winners = tuple(( int(x.strip()) for x in m.group(2).split(" ") if x.strip() ))
    mynums = tuple(( int(x.strip()) for x in m.group(3).split(" ") if x.strip() ))

    cards.append( (cardid, winners, mynums, ) )

#for card in cards:
#    print(f"{card}")

if args.p1:
    print("Doing part 1")

    total = 0
    for card in cards:
        winners = set(card[1])
        mynums = set(card[2])
        mywinners = mynums.intersection(winners)

        if mywinners:
            points = 1 << (len(mywinners)-1)
        else:
            points = 0

        total = total + points
        
        #print(f"Winners: {winners}  mynums: {mynums}  mywinners: {mywinners}  points: {points}")

    print(f"total: {total}")
        
    
if args.p2:
    print("Doing part 2")

    scores = {}
    total = {}

    for card in cards:
        winners = set(card[1])
        mynums = set(card[2])
        mywinners = mynums.intersection(winners)

        scores[card[0]] = len(mywinners)

    numcards = {}
    for card in cards:
        cardid = card[0]
        numcards[cardid] = 1

    for card in cards:
        cardid = card[0]
        score = scores[cardid]
        num = numcards[cardid]
        
        for i in range(0,score):
            toadd = cardid + i + 1
            if toadd in numcards:
                numcards[ toadd ] = numcards[toadd] + num

    total = 0
    for cardid, num in numcards.items():
        total = total + num
        #print(f"{cardid} -> {num}")

    print(f"Total: {total}")
        
