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

lineRe = re.compile("(deal into new stack)|(deal with increment (\d+))|(cut (-?\d+))")

instrs=[]

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        instrs.append(("new",))
    elif m.group(3):
        instrs.append(("incr",int(m.group(3)),))
    elif m.group(5):
        instrs.append(("cut",int(m.group(5)),))

#print("Instructions: %s" % (instrs,))

def shuffle(deck, instrs):
    deck = deck[:]
    for instr in instrs:
        if instr[0] == "new":
            deck.reverse()
        elif instr[0] == "incr":
            amt = instr[1]
            newdeck = [-1] * len(deck)

            pos = 0
            for i in range(0,len(deck)):
                newdeck[pos] = deck[i]
                pos = (pos + amt) % len(deck)

            deck = newdeck
            pass
        elif instr[0] == "cut":
            amt = instr[1]
            if amt < 0:
                deck = deck[amt:] + deck[0:amt]
            else:
                deck = deck[amt:] + deck[0:amt]
    return deck

def inverse(n, m):
    # return x so that n * x == 1 mod m

    # compute n ** (m-1) mod m

    p = m-2
    nn = n
    output = 1

    total = 0
    np = 1
    
    while p:
        #print("p:%s np:%s nn:%s" % (p,np,nn))
        if (p % 2) == 1:
            output = (output * nn) % m
            total = total + np

            #print("nn: %s Output: %s" % (nn,output,))
        p = p // 2
        nn = (nn * nn) % m

        np = np * 2


    output = output % m
    #print("m-2:%s total:%s n: %s n^-1: %s" % (m-2,total,n,output,))
    #if ((output * n) % m) != 1:
    #    print("OOPS")
        
    return output

print("%s" % (inverse(5,13),))

def shufflefunction(instrs, decksize, iters = 1):
    output = (1,0)

    #print("FUNC: %s" % (output,))
    if iters < 0:
        iters = -iters
        for instr in reversed(instrs):
            if instr[0] == "new":
                output = ( -output[0], -output[1] - 1 )
            elif instr[0] == "incr":
                amt = instr[1]
                invamt = inverse(amt, decksize)
                output = tuple([(invamt * c) % decksize for c in output])
            elif instr[0] == "cut":
                output = ( output[0], (output[1] + instr[1]) % decksize, )    
    else:
        for instr in instrs:
            if instr[0] == "new":
                output = ( -output[0], -output[1] - 1 )
            elif instr[0] == "incr":
                output = tuple([(instr[1] * c) % decksize for c in output])
            elif instr[0] == "cut":
                output = ( output[0], (output[1] - instr[1]) % decksize, )    
            #print("Instr:%s  FUNC: %s" % (instr,output,))
        
    powers = { 1 : output}

    n = 1
    no = output
    powers = { n : no }
    while n <= iters//2:
        n = n * 2
        no = ( (no[0] * no[0] ) % decksize, ((no[0] * no[1]) + no[1]) % decksize, )
        powers[n] = no

    rem = iters
    io = (1,0)
    total = 0
    while rem > 0:
        while rem < n:
            n = n // 2
        no = powers[n]
        io = ( (no[0] * io[0]) % decksize,((no[0] * io[1]) + no[1]) % decksize,)
        rem = rem - n
        total = total + n

    print("IO: %s" % (io,))
    return lambda x : (x * io[0] + io[1]) % decksize 

def shuffle2(deck, instrs):
    sfunc = shufflefunction(instrs,len(deck))

    output = [0] * len(deck)

    for i in range(0,len(deck)):
        output[sfunc(i)] = deck[i]

    return output

if args.p1:
    print("Doing part 1")

    
    if args.input == "input":
        dsize = 10007
    else:
        dsize = 10

    deck = list(range(0,dsize))
    deck = shuffle(deck,instrs)
    if len(deck) > 2019:
        print("2019: %s" % (deck.index(2019),))

    deck = list(range(0,dsize))
    deck = shuffle2(deck,instrs)
    if len(deck) > 2019:
        print("2019: %s" % (deck.index(2019),))

    sfunc = shufflefunction(instrs, dsize)

    npos = sfunc(2019)
    print("2019: %s" % (npos,))

if args.p2:
    print("Doing part 2")

    #print("2020: %s" % (shuffleindex(instrs,119315717514047,2020),))

    sfunc = shufflefunction(instrs, 119315717514047, -101741582076661)

    print("2020: %s" % (sfunc(2020),))
